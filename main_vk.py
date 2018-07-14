import time
import datetime
import os
import vk_api
from scripts import *
from threading import Thread
from vk_api.longpoll import VkLongPoll, VkEventType
import json
with open('config/config.json', encoding='utf-8') as f:
    config_json = json.load(f)
group_token = config_json['group_token']
owner_id = config_json['owner_id']
responses = {k.lower(): v for k, v in config_json["responses"].items()}
vk = vk_api.VkApi(token = group_token)
vk._auth_token()
convos =  vk.method('messages.getConversations')
pinglist = []
for i in convos['items']:
    pinglist.append(i['conversation']['peer']['id'])

def write_msg(user_id, s, *kwargs):
    print(user_id,s,kwargs)
    try:
        vk.method('messages.send', {'user_id':user_id, 'message':s})
        if kwargs:
            attachments = ""
            for i in kwargs:
                vkphoto = vk_api.VkUpload(vk).photo_messages(photos=i)
                os.remove(i)
                print(vkphoto)
            vk.method('messages.send', {'user_id': user_id, 'attachment': attachments})
    except:
        vk.method('messages.send', {'user_id':user_id, 'message':'Произошла ошибка при посылке сообщения. Попробуйте ещё раз.'})




class ResponseThread(Thread):
    def __init__(self):
        Thread.__init__(self)
    def run(self):
        global config_json
        longpoll = VkLongPoll(vk)
        while True:
            for event in longpoll.listen():
                print(event)
                if event.type == VkEventType.MESSAGE_NEW:
                    print('Новое сообщение:')
                    if event.from_me:
                        print('От меня для: ', end='')
                    elif event.to_me:
                        message = ""
                        cmd = ""
                        if event.text.lower() in list(responses.keys()) and config_json["changeable_config"]["bool_responses_on"] == True:
                            write_msg(event.user_id,responses[event.text.lower()])
                        elif event.text == config_json["com_symbol"] + "config reload" and event.user_id in owner_id:
                            with open('config/config.json', encoding='utf-8') as f:
                                config_json = json.load(f)
                            command = event.text[1:].split()
                            print(command)
                            cmd = config_json["commands"][command[0]]["func"]
                            print(cmd)
                            getattr(globals()["config"], "main")("reload")
                            write_msg(event.user_id, "Конфигурация обновлена.")
                        elif event.text[0] == config_json["com_symbol"]:
                            print("COMMAND")
                            command = event.text[1:].split()
                            print(command[0])
                            if command[0] in list(config_json["commands"].keys()):
                                if event.user_id in owner_id or config_json["commands"][command[0]["public"]]:
                                    cmd = config_json["commands"][command[0]]["func"]
                                    cmdvalue = list(getattr(globals()[cmd],"main")(*command[1:]))
                                    cmdvalue.insert(0,event.user_id)
                                    write_msg(*cmdvalue)
                                else:
                                    write_msg(event.user_id, "Команда не доступна для пользователей.")
                            else:
                                write_msg(event.user_id, "Команда не найдена.")
                        else:
                            write_msg(event.user_id, event.text)
                        print('Для меня от: ', end='')
                    if event.from_user:
                        print(event.user_id)
                    elif event.from_group:
                        print('группы', event.group_id)
                    print('Текст: ', event.text)
                    print()
                    if (event):
                        print(event)

                elif event.type == VkEventType.USER_TYPING:
                    print('Печатает ', end='')

                    if event.from_user:
                        print(event.user_id)
                    elif event.from_group:
                        print('администратор группы', event.group_id)

                elif event.type == VkEventType.USER_TYPING_IN_CHAT:
                    print('Печатает ', event.user_id, 'в беседе', event.chat_id)

                elif event.type == VkEventType.USER_ONLINE:
                    print('Пользователь', event.user_id, 'онлайн', event.platform)

                elif event.type == VkEventType.USER_OFFLINE:
                    print('Пользователь', event.user_id, 'оффлайн', event.offline_type)

                else:
                    print(event.type, event.raw[1:])
class TimeThread(Thread):
    #Пишет сообщения всем кто писал раннее боту в 3 часа ночи. Не знаю зачем.
    t = 5
    def __init__(self):
        Thread.__init__(self)
    def run(self):
        while True:
            #print("Testing.")
            now = datetime.datetime.now()
            print(now.hour)
            if now.hour >= 3 and now.hour <= 4 and self.t > 0 and config_json["changeable_config"]["bool_defense_mode"]:
                print("Предупреждаем об угрозе...")
                for i in pinglist:
                    write_msg(i,"Всегда будь готов! Ты не знаешь когда могут аттаковать родину мать. Ты должен быть готов даже если тебя будят в 3 часа ночи.")
                self.t -= 1
            if now.hour > 4:
                self.t = 5
            time.sleep(30)

def main():
    """ Пример использования longpoll
        https://vk.com/dev/using_longpoll
        https://vk.com/dev/using_longpoll_2
    """

    print("START")
    thread1 = ResponseThread()
    thread1.start()
    #thread2 = TimeThread()
    #thread2.start()

if __name__ == '__main__':
    #write_msg(owner_id, "aaa")
    main()
