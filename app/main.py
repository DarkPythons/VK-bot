import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from config import BaseSettingApp
from utils import SendingMessageUser
from database.db import create_table,drop_table,get_session #type:ignore
from text import (
    hello_user_text,help_user_text,no_command_search_text, 
    wiki_start_text,exit_all_process_text,no_exit_text,
    weather_start_text,number_start_text,mailing_start_text,
    after_mailing_text,notes_start_text,notes_start_add_text,
    stopped_write_or_delete_text,no_input_message_text,
    limit_warning_text
    ) #type: ignore
from database.orm import UsersOrm, NotesOrm
from handlers import (
    handler_wiki, handler_weather, handler_number,
    handler_mailing,handler_writing_notes,
    handler_show_notes,handler_start_deleted_notes,
    handler_deleted_notes
)


user_orm = UsersOrm(get_session())
note_orm = NotesOrm(get_session())

setting_app = BaseSettingApp()

authorise = vk_api.VkApi(token=setting_app.TOKEN_BOT)
longpoll = VkLongPoll(authorise)

send_func = SendingMessageUser(authorise)

try:
    create_table()
except Exception as Error:
    print('Ошибка создания базы данных: ' + str(Error))

try:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            sending_text = event.text
            sender_id = event.user_id
            #Остановка программы (только если бот в режиме разработки)
            if sending_text == '/debug_stop':
                if setting_app.PROGRAM_IN_DEBUG:
                    raise Exception

            user_from_orm = user_orm.get_user_from_db(sender_id)
            if not user_from_orm:
                user_orm.create_user_in_db(sender_id)
                user_from_orm = user_orm.get_user_from_db(sender_id)
            user_from_db = user_from_orm['Users']
            #Если пользователь не в ожидании запроса ввода
            if not user_from_db.in_process:
                if sending_text.lower() in ['старт', 'привет', 'hello', '/start']:
                    send_func.send_sticker(sender_id, 21)
                    send_func.write_message_hello(sender_id, hello_user_text)
                
                elif sending_text.lower() in ['/help', 'помощь', 'help']:
                    send_func.write_message_help(sender_id, help_user_text)

                elif sending_text.lower() in ['/wiki', 'вики', 'информация из wiki']:
                    send_func.wiki_start_message(sender_id,  wiki_start_text)
                    user_orm.update_status_user_wiki(sender_id, status=True)

                elif sending_text.lower() in ['/weathers', 'информация о погоде', '/weather', 'погода']:
                    send_func.weather_start_message(sender_id, weather_start_text)
                    user_orm.update_status_user_weather(sender_id, status=True)

                elif sending_text.lower() in ['/numbers', "получить интереный факт", '/number']:
                    """Если пользователь захотел получить интересный факт о числе"""
                    send_func.number_start_message(sender_id, number_start_text)
                    user_orm.update_status_user_number(sender_id, status=True)

                elif sending_text.lower() == '/sends':
                    if user_from_db.is_superuser:
                        """Если пользователь захотел сделать рассылку + является супер пользователем"""
                        send_func.mailing_start_message(sender_id, mailing_start_text)
                        user_orm.update_status_mailing_before(sender_id, status=True)
                    else:
                        send_func.write_message_hello(sender_id, 'У вас нет прав на использование этой команды.')
                elif sending_text.lower() in ['/notes', 'заметки']:
                    """Если пользователь захотел получить информацию о заметках"""
                    send_func.write_notes_base_message(sender_id, notes_start_text)

                elif sending_text.lower() in ['добавить заметку', '/add_notes']:
                    """Если пользователь захотел добавить заметку"""
                    send_func.write_notes_and_stopped_key(sender_id, notes_start_add_text)
                    user_orm.update_status_add_notes(sender_id, status=True)

                elif sending_text.lower() in ['получить свои заметки', '/show_notes']:
                    """Если пользователь захотел получить свои заметки"""
                    handler_show_notes(send_func=send_func, sender_id=sender_id, note_orm=note_orm)
                
                elif sending_text.lower() in ['удалить заметки', '/delete_notes']:
                    """Если пользователь захотел удалить свои заметки"""
                    handler_start_deleted_notes(
                        send_func=send_func,
                        sender_id=sender_id,
                        note_orm=note_orm,
                        user_orm=user_orm,)
                    
                elif sending_text.lower() in ['/stop', 'отмена']:
                    """Если пользователь нажал кнопку отмена, но он не находится в режиме ввода"""
                    send_func.write_message_all_exit(sender_id, no_exit_text)

                elif sending_text.lower() in ['/stop_input', 'остановить ввод']:
                    """Если пользователь захотел выйти из режима ввода, когда он в нём не находился"""
                    send_func.write_message(sender_id, no_input_message_text)

                else:
                    """Если команда, которую ввел человек не найдена"""
                    send_func.write_message_no_search(sender_id, no_command_search_text)

            #Если пользователь находится в статусе запроса ввода
            else:
                if sending_text.lower() in ['/stop', 'отмена']:
                    """Если пользователь нажал кнопку отмена, в любом режиме ввода"""
                    user_orm.update_full_process(sender_id, full_status=False)
                    send_func.write_message_all_exit(sender_id, exit_all_process_text)

                elif sending_text.lower() in ['/stop_input', 'остановить ввод']:
                    """Если пользователь остановил ввод на добавление или удаление заметок"""
                    user_orm.update_full_process(sender_id, full_status=False)
                    send_func.write_notes_base_message(sender_id, stopped_write_or_delete_text)

                elif user_from_db.in_process_wiki:
                    """Если пользователь в запросе ввода Wiki данных"""
                    handler_wiki(send_func=send_func, sender_id=sender_id, sending_text=sending_text)
                
                elif user_from_db.in_process_weather:
                    """Если пользователь в запросе ввода города для получения погоды"""
                    handler_weather(send_func=send_func, sender_id=sender_id, sending_text=sending_text)

                elif user_from_db.in_process_number:
                    """Если пользователь в запросе воода цифры для получения факта"""
                    handler_number(send_func=send_func, sender_id=sender_id, sending_text=sending_text)

                elif user_from_db.in_process_mailing:
                    """Если пользователь ввел сообщение для рассылки"""
                    list_users_id = user_orm.get_list_vk_id()
                    handler_mailing(send_func=send_func, sending_text=sending_text, list_user=list_users_id)
                    user_orm.update_status_mailing_after(user_id=sender_id, status=False)
                    send_func.write_message(sender_id, after_mailing_text)

                elif user_from_db.in_process_create_note:
                    """Если пользователь ввел заметку, которую нужно добавить"""
                    if len(sending_text) <= 150:
                        handler_writing_notes(send_func=send_func, sender_id=sender_id,sending_text=sending_text, note_orm=note_orm)
                    else:
                        send_func.write_message(sender_id, limit_warning_text)
                
                elif user_from_db.in_process_delete_note:
                    """Если пользователь находится в режиме ожидания ввода номеров заметок
                    для их удаления из базы.
                    """
                    handler_deleted_notes(send_func=send_func, sender_id=sender_id, sending_text=sending_text,note_orm=note_orm)


except Exception as error:
    print('Ошибка приложения: ' + str(error))
finally:
    """Удаление таблиц базы данных, если приложение в режиме разработки"""
    if setting_app.PROGRAM_IN_DEBUG:
        drop_table()