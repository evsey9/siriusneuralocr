import time
import datetime
import random
import vk_api
import script
from threading import Thread
from vk_api.longpoll import VkLongPoll, VkEventType
import json
with open('config/config.json', encoding='utf-8') as f:
    config_json = json.load(f)
group_token = config_json['group_token']
owner_id = config_json['owner_id']
responses = {k.lower(): v for k, v in config_json["responses"].items()}
vk_session = vk_api.VkApi(token = group_token)
vk_session._auth_token()
convos =  vk_session.method('messages.getConversations')
pinglist = []
for i in convos['items']:
    pinglist.append(i['conversation']['peer']['id'])

def write_msg(user_id, s):
    vk_session.method('messages.send', {'user_id':user_id, 'message':s})
def random_range(num1 = "1024", num2 = "0", amount = "1", *kwargs):
    try:
        num1 = int(num1)
        num2 = int(num2)
        amount = int(amount)
    except:
        return("Введите аргументы как цифры.")
    randarray = ""
    for i in range(amount):
        if num2 > num1:
            randarray = randarray + " " + str(random.randint(num1,num2))
        else:
            randarray = randarray + " " + str(random.randint(num2,num1))
    return randarray
def exec_py():
    return(script.main())
def config(option = "default", key = "default", value = "default", *kwargs):
    if option == "default":
        return("Введите аргументы.")
    elif option == "show":
        return(json.dumps(config_json["changeable_config"],ensure_ascii=False))
    elif option == "show_full":
        return (json.dumps(config_json, ensure_ascii=False))
    elif option == "change":
        if value == "default":
            return("Введите значение.")
        if key in config_json["changeable_config"]:
            try:
                print(key.find("bool"))
                if key.find("bool") == 0:
                    if value == "true" or value == "false":
                        if value == "true":
                            value = True
                        else:
                            value = False
                    else:
                        return("Введите true или false.")
                elif key.find("int") == 0:
                    try:
                        value = int(value)
                    except:
                        return("Введите число.")
                config_json["changeable_config"][key] = value
                return("Настройки изменены.")
            except:
                return("Аргументы неправильны.")
        else:
            return("Ключа не существует.")
    elif option == "save":
        with open('config/config.json', encoding='utf-8', mode='w') as f:
            json.dump(config_json,f, ensure_ascii=False, indent=4)
            return("Настройки сохранены.")
    else:
        return ("Введите правильную опцию.")
def help(mode = "all", command = "default", *kwargs):
    if mode == "all":
        return(json.dumps(config_json["commands"], ensure_ascii=False,indent=2))
    elif mode == "show":
        try:
            return(json.dumps(config_json["commands"][command], ensure_ascii=False,indent=2))
        except:
            return("Команды не существует.")
    else:
        return("Неправильный режим.")
def shutdown():
    quit()
class ResponseThread(Thread):
    def __init__(self):
        Thread.__init__(self)
    def run(self):
        longpoll = VkLongPoll(vk_session)
        while True:
            for event in longpoll.listen():
                print(event)
                if event.type == VkEventType.MESSAGE_NEW:
                    print('Новое сообщение:')
                    if event.from_me:
                        print('От меня для: ', end='')
                    elif event.to_me:
                        if event.text.lower() in list(responses.keys()) and config_json["changeable_config"]["bool_responses_on"] == True:
                            write_msg(event.user_id, responses[event.text.lower()])
                        elif event.text[0] == config_json["com_symbol"]:
                            print("COMMAND")
                            command = event.text[1:].split()
                            print(command[0])
                            if command[0] in list(config_json["commands"].keys()):
                                if event.user_id in owner_id or config_json["commands"][command[0]["public"]]:
                                    write_msg(event.user_id,globals()[config_json["commands"][command[0]]["func"]](*command[1:]))
                                else:
                                    write_msg(event.user_id, "Команда не доступна для пользователей.")
                            #elif command[0] in list(config_json["public_commands"].keys()):
                            #    write_msg(event.user_id, globals()[config_json["public_commands"][command[0]]](*command[1:]))
                            else:
                                write_msg(event.user_id, "Команда не найдена.")
                            #if event.text[1:] in list(config_json["commands"].keys()):

                        else:
                            write_msg(event.user_id, event.text)
                        print('Для меня от: ', end='')
                    if event.from_user:
                        print(event.user_id)

                    elif event.from_chat:
                        print(event.user_id, 'в беседе', event.chat_id)
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
    t = 5
    def __init__(self):
        Thread.__init__(self)
    def run(self):
        while True:
            print("Testing.")
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
