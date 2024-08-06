from utils import get_info_from_wiki, info_from_api_weather


def handler_wiki(*, send_func, sender_id, sender_messages):
    """Обработчик запроса к функции запроса Wiki, по ключевым словам"""
    total_info_from_wiki = get_info_from_wiki(sender_messages)
    if total_info_from_wiki['status'] == 200:
        send_func.write_message(sender_id, total_info_from_wiki['content'])
    elif total_info_from_wiki['status'] == 301:
        send_func.write_message(sender_id, "По вашему запросу было найдено несколько возможных значений, уточните ваш запрос: " + total_info_from_wiki['content'])
    else:
        send_func.write_message(sender_id, 'По вашему запросу нет совпадений.')

def handler_weather(*, send_func,sender_id:int,sender_messages:str):
    """Обработчик запроса к функции запроса погоды, по названию города"""
    info_from_weather = info_from_api_weather(sender_messages)
    if info_from_weather['status'] == 200:
        send_func.write_message(sender_id, info_from_weather['content'])
    elif info_from_weather['status'] == 404:
        send_func.write_message(sender_id, info_from_weather['content'])
    else:
        send_func.write_message(sender_id, info_from_weather['content'])