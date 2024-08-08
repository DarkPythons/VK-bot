from utils import get_info_from_wiki, info_from_api_weather,info_from_api_numbers, SendingMessageUser
from text import group_remined_text,succes_added_note_text,bad_added_note_text
from database.orm import NotesOrm


def handler_wiki(*, send_func, sender_id, sending_text):
    """Обработчик запроса к функции запроса Wiki, по ключевым словам"""
    total_info_from_wiki = get_info_from_wiki(sending_text)
    #Контент ответа будет зависеть от статуса ответа API
    send_func.write_message(sender_id, total_info_from_wiki['content'])


def handler_weather(*, send_func,sender_id:int,sending_text:str):
    """Обработчик запроса к функции получения погоды, по названию города"""
    info_from_weather = info_from_api_weather(sending_text)
    #Контент ответа будет зависеть от статуса ответа API
    send_func.write_message(sender_id, info_from_weather['content'])


def handler_number(*, send_func, sender_id:int, sending_text:str):
    """Обработчик запроса к функции получения информации об числе"""
    info_from_numbers = info_from_api_numbers(sending_text)
    #Контент ответа будет зависеть от статуса ответа API
    send_func.write_message(sender_id, info_from_numbers['content'])

def handler_mailing(*,send_func,sending_text:str,list_user:list):
    """Обработчик запроса к рассылке определенного текста"""
    if sending_text.lower() == 'рассылка напоминания':
        sending_text = group_remined_text
    for one_user_id in list_user:
        send_func.write_message(one_user_id, sending_text)

def handler_writing_notes(*, send_func:SendingMessageUser, sender_id:int, sending_text:str,note_orm:NotesOrm):
    """Обработчик запроса на добавление заметки пользователем"""
    try:
        text_note = sending_text
        note_orm.add_note_user_orm(sender_id, text_note)
        send_func.write_message(sender_id, succes_added_note_text)
    except Exception as error:
        print(error)
        send_func.write_message(sender_id, bad_added_note_text)