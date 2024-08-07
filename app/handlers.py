from utils import get_info_from_wiki, info_from_api_weather,info_from_api_numbers
from text import group_remined_text

def handler_wiki(*, send_func, sender_id, sender_messages):
    """Обработчик запроса к функции запроса Wiki, по ключевым словам"""
    total_info_from_wiki = get_info_from_wiki(sender_messages)
    #Контент ответа будет зависеть от статуса ответа API
    send_func.write_message(sender_id, total_info_from_wiki['content'])


def handler_weather(*, send_func,sender_id:int,sender_messages:str):
    """Обработчик запроса к функции получения погоды, по названию города"""
    info_from_weather = info_from_api_weather(sender_messages)
    #Контент ответа будет зависеть от статуса ответа API
    send_func.write_message(sender_id, info_from_weather['content'])


def handler_number(*, send_func, sender_id:int, sender_messages:str):
    """Обработчик запроса к функции получения информации об числе"""
    info_from_numbers = info_from_api_numbers(sender_messages)
    #Контент ответа будет зависеть от статуса ответа API
    send_func.write_message(sender_id, info_from_numbers['content'])

def handler_mailing(*,send_func,sending_text:str,list_user:list):
    """Обработчик запроса к рассылке определенного текста"""
    if sending_text.lower() == 'рассылка напоминания':
        sending_text = group_remined_text
    for one_user_id in list_user:
        send_func.write_message(one_user_id, sending_text)
