from utils import (get_info_from_wiki, info_from_api_weather,
    info_from_api_numbers, SendingMessageUser, 
    confirm_response)
import re

from keyboards import KeyBoard
from text import Text
from database.orm import NotesOrm, UsersOrm

keyboard = KeyBoard()
text = Text()

def handler_wiki(*, 
        send_func: SendingMessageUser, 
        sender_id:int, 
        sending_text:str
    ):
    """Обработчик запроса к функции запроса Wiki, по ключевым словам"""
    total_info_from_wiki = get_info_from_wiki(sending_text)
    #Контент ответа будет зависеть от статуса ответа API
    send_func.write_message(sender_id, total_info_from_wiki['content'])


def handler_weather(*, 
        send_func:SendingMessageUser,
        sender_id:int,
        sending_text:str
    ):
    """Обработчик запроса к функции получения погоды, по названию города"""
    info_from_weather = info_from_api_weather(sending_text)
    #Контент ответа будет зависеть от статуса ответа API
    send_func.write_message(sender_id, info_from_weather['content'])


def handler_number(*, 
        send_func:SendingMessageUser, 
        sender_id:int, 
        sending_text:str
    ):
    """Обработчик запроса к функции получения информации об числе"""
    info_from_numbers = info_from_api_numbers(sending_text)
    #Контент ответа будет зависеть от статуса ответа API
    send_func.write_message(sender_id, info_from_numbers['content'])


def handler_mailing(*,
        send_func:SendingMessageUser,
        sending_text:str,
        list_user:list
    ):
    """Обработчик запроса к рассылке определенного текста"""
    if sending_text.lower() == 'рассылка напоминания':
        sending_text = text.group_remined
    for one_user_id in list_user:
        send_func.write_message(one_user_id, sending_text)

def handler_writing_notes(*, 
        send_func:SendingMessageUser, 
        sender_id:int, 
        sending_text:str,
        note_orm:NotesOrm
    ):
    """Обработчик запроса на добавление заметки пользователем"""
    try:
        text_note = sending_text
        note_orm.add_note_user_orm(sender_id, text_note)
        send_func.write_message(sender_id, text.succes_added_note)
    except Exception as error:
        send_func.write_message(sender_id, text.bad_added_note)

def handler_show_notes(*, 
        send_func:SendingMessageUser, 
        sender_id:int,
        note_orm:NotesOrm
    ):
    """Обработчик запроса на получение всех заметок человека"""

    list_notes_user = note_orm.get_user_notes_orm(sender_id)
    confirm_text_sending = confirm_response(list_notes_user, "Список ваших заметок:\n")
    send_func.write_message_add_keyboard(
        sender_id,
        confirm_text_sending, 
        keyboard.keyboard_notes
    )
    
def handler_start_deleted_notes(*, 
        send_func: SendingMessageUser, 
        sender_id:int, 
        note_orm:NotesOrm,
        user_orm:UsersOrm
    ):
    """Обработчик запроса, когда пользователь хочет удалить свои заметки"""
    list_notes_user = note_orm.get_user_notes_orm(sender_id)
    if len(list_notes_user) > 0:
        send_func.write_message(sender_id, text.notes_start_delete)
        confirm_text_sending = confirm_response(list_notes_user, "Список ваших заметок:\n")
        send_func.write_message_add_keyboard(
            sender_id, 
            confirm_text_sending, 
            keyboard.keyboard_stopped_input
            )
        user_orm.update_status_delete_notes(sender_id, status=True)
    else:
        send_func.write_message_add_keyboard(
            sender_id, 
            "У вас пока нет заметок, нажмите кнопку 'Добавить заметку' на кнопках", 
            keyboard.keyboard_notes
        )


def handler_deleted_notes(*,
        send_func:SendingMessageUser,
        sender_id:int,
        sending_text:str,
        note_orm:NotesOrm,
        user_orm:UsersOrm
    ):

    """Обработчик запроса на удаление заметки пользователем"""
    regular = re.search(r"\b([0-9]+)\b", sending_text)
    if regular:
        list_notes_user = note_orm.get_user_full_notes_orm(user_id=sender_id)
        id_notes_del = int(regular.group())
        if id_notes_del <= len(list_notes_user) and id_notes_del > 0:
            #Удаление записи
            info_by_delete_note = list_notes_user[id_notes_del-1]
            note_orm.delete_note_from_orm(note_id=info_by_delete_note['id'])
            send_func.write_message(
                sender_id, 
                f'Вы успешно удалили заметку с id: {id_notes_del}'
                )
            user_orm.update_status_delete_notes(sender_id, status=False)
            send_func.write_message_add_keyboard(
                sender_id, 
                text.notes_start, 
                keyboard.keyboard_notes
                )
        else:
            #Если человек ввёл некоректное число для удаления заметки
            send_func.write_message(sender_id, text.no_valid_number_notes)
    else:
        #Если человек ввел неправильный формат для удаления заметки
        send_func.write_message(sender_id, text.no_valid_del_notes)
