#НЕ УДЯЛЙТЕ/ПЕРЕМЕЩАЙТЕ/ПЕРЕИМЕНОВЫВАЙТЕ ЭТОТ ФАЙЛ ТАК КАК ЭТО ВЫЗОВЕТ СБОИ В РАБОТЕ БОТА.
import json
with open('config/config.json', encoding='utf-8') as f:
    config_json = json.load(f)
def main(option = "default", key = "default", value = "default", *kwargs):
    global config_json
    if option == "default":
        return["Введите аргументы."]
    elif option == "show":
        return[json.dumps(config_json["changeable_config"],ensure_ascii=False,indent=4)]
    elif option == "show_full":
        return[json.dumps(config_json, ensure_ascii=False,indent=4)]
    elif option == "change":
        if key == "default":
            return["Введите ключ."]
        if key in config_json["changeable_config"]:
            try:
                if value == "default":
                    return ["Введите значение."]
                print(key.find("bool"))
                if key.find("bool") == 0:
                    if value == "true" or value == "false":
                        if value == "true":
                            value = True
                        else:
                            value = False
                    else:
                        return["Введите true или false."]
                elif key.find("int") == 0:
                    try:
                        value = int(value)
                    except:
                        return["Введите число."]
                config_json["changeable_config"][key] = value
                return["Настройки изменены."]
            except:
                return["Аргументы неправильны."]
        else:
            return["Ключа не существует."]
    elif option == "save":
        with open('config/config.json', encoding='utf-8', mode='w') as f:
            json.dump(config_json,f, ensure_ascii=False, indent=4)
            return["Настройки сохранены."]
    elif option == "reload":
        with open('config/config.json', encoding='utf-8') as f:
            config_json = json.load(f)
    else:
        return ["Введите правильную опцию."]