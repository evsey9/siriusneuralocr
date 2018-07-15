# Импортируем модули для работы с JSON и логами.
import json
import logging

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request
app = Flask(__name__)
from scripts import *
with open('config/config.json', encoding='utf-8') as f:
    config_json = json.load(f)
#with open('config/yandex_data.json', encoding='utf-8') as f:
#    yandex_data = json.load(f)
logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}

# Задаем параметры приложения Flask.
@app.route("/", methods=['POST'])

def main():
# Функция получает тело запроса и возвращает ответ.
    logging.info('Request: %r', request.json)

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )

# Функция для непосредственной обработки диалога.
def handle_dialog(req, res):
    message = ""
    cmd = ""
    user_id = req['session']['user_id']

    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.

        sessionStorage[user_id] = {
            'suggests': [
                "random",
                "facerec",
                "help",
            ]
        }

        res['response']['text'] = config_json["greet"]
        res['response']['buttons'] = get_suggests(user_id)
        return

    # Обрабатываем ответ пользователя.
    command = req['request']['original_utterance'].split()
    if command[0] in list(config_json["commands"].keys()) and config_json["commands"][command[0]["public"]]:
        cmd = config_json["commands"][command[0]]["func"]
        cmdvalue = list(getattr(globals()[cmd], "main")(*command[1:]))
        res['response']['text'] = str(cmdvalue)
        return
    #if req['request']['original_utterance'].lower() in [
    #    'ладно',
    #    'куплю',
    #    'покупаю',
    #    'хорошо',
    #]:
    #    # Пользователь согласился, прощаемся.
    #    res['response']['text'] = 'Слона можно найти на Яндекс.Маркете!'
    #    return

    # Если нет, то убеждаем его купить слона!
    #res['response']['text'] = 'Все говорят "%s", а ты купи слона!' % (
    #    req['request']['original_utterance']
    #)
    res['response']['buttons'] = get_suggests(user_id)

# Функция возвращает две подсказки для ответа.
def get_suggests(user_id):
    session = sessionStorage[user_id]

    # Выбираем две первые подсказки из массива.
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests']
    ]

    # Убираем первую подсказку, чтобы подсказки менялись каждый раз.
    #session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session

    # Если осталась только одна подсказка, предлагаем подсказку
    # со ссылкой на Яндекс.Маркет.
    #if len(suggests) < 2:
    #    suggests.append({
    #        "title": "Ладно",
    #        "url": "https://market.yandex.ru/search?text=слон",
    #        "hide": True
    #    })

    return suggests