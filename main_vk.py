import time
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import json
with open('config/vkdata.json') as f:
    vkdata = json.load(f)
group_token = vkdata['group_token']
owner_id = vkdata['owner_id']
vk_session = vk_api.VkApi(token = group_token)
vk_session._auth_token()
def write_msg(user_id, s):
    vk_session.method('messages.send', {'user_id':user_id, 'message':s})
#values = {'out':0, 'count':100, 'time_offset':60}
#vk_session.method('messages.getHistory', values)



def main():
    """ Пример использования longpoll
        https://vk.com/dev/using_longpoll
        https://vk.com/dev/using_longpoll_2
    """

    #login, password = 'python@vk.com', 'mypassword'
    #vk_session = vk_api.VkApi(login, password)

    #try:
    #    vk_session.auth(token_only=True)
    #except vk_api.AuthError as error_msg:
    #    print(error_msg)
    #    return '''

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():

        if event.type == VkEventType.MESSAGE_NEW:
            print('Новое сообщение:')

            if event.from_me:
                print('От меня для: ', end='')
            elif event.to_me:
                print('Для меня от: ', end='')
                write_msg(event.user_id, event.text)

            if event.from_user:
                print(event.user_id)

                #write_msg(event.user_id, '')
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


if __name__ == '__main__':
    #write_msg(owner_id, "aaa")
    main()
