import json
with open('config/config.json', encoding='utf-8') as f:
    config_json = json.load(f)
def main(mode = "all", command = "default", *kwargs):
    if mode == "all":
        return[json.dumps(config_json["commands"], ensure_ascii=False,indent=2)]
    elif mode == "show":
        try:
            return[json.dumps(config_json["commands"][command], ensure_ascii=False,indent=2)]
        except:
            return["Команды не существует."]
    else:
        return["Неправильный режим."]