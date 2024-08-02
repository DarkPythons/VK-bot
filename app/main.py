import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from config import BaseSettingApp
from utils import SendingMessageUser
from database.db import create_table,drop_table,get_session #type:ignore
from text import hello_user_text,help_user_text,no_command_search_text, wiki_start_text,exit_all_process_text,no_exit_text #type: ignore
from database.orm import UsersOrm
from handlers import handler_wiki, handler_weather

user_orm = UsersOrm(get_session())


setting_app = BaseSettingApp()

authorise = vk_api.VkApi(token=setting_app.TOKEN_BOT)
longpoll = VkLongPoll(authorise)

send_func = SendingMessageUser(authorise)

create_table()

try:
    #Прослушивание сообщений от бота
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            sender_messages = event.text
            sender_id = event.user_id

            user_from_orm = user_orm.get_user_from_db(sender_id)
            if not user_from_orm:
                user_orm.create_user_in_db(sender_id)
                user_from_orm = user_orm.get_user_from_db(sender_id)
            user_from_db = user_from_orm['Users']
            print(user_from_db)
            #Если пользователь не в ожидании запроса ввода
            if not user_from_db.in_process:
                if sender_messages.lower() in ['старт', 'привет', 'hello', '/start']:
                    send_func.send_sticker(sender_id, 21)
                    send_func.write_message_hello(sender_id, hello_user_text)
                
                elif sender_messages.lower() in ['/help', 'помощь', 'help']:
                    send_func.write_message_help(sender_id, help_user_text)

                elif sender_messages.lower() in ['/wiki', 'вики', 'информация из wiki']:
                    send_func.wiki_start_text(sender_id,  wiki_start_text)
                    user_orm.update_status_user_wiki(sender_id, status=True)

                elif sender_messages.lower() in ['/weathers', 'информация о погоде', '/weather', 'погода']:
                    pass


                elif sender_messages.lower() in ['/stop', 'отмена']:
                    """Если пользователь нажал кнопку отмена, но он не находится в режиме ввода"""
                    send_func.write_message_all_exit(sender_id, no_exit_text)

                else:
                    send_func.write_message_no_search(sender_id, no_command_search_text)

            #Если пользователь находится в статусе запроса ввода
            else:
                if sender_messages.lower() in ['/stop', 'отмена']:
                    """Если пользователь нажал кнопку отмена, в любом режиме ввода"""
                    user_orm.update_full_process(sender_id, full_status=False)
                    send_func.write_message_all_exit(sender_id, exit_all_process_text)
                #Если пользователь в запросе ввода Wiki данных
                elif user_from_db.in_process_wiki:
                    handler_wiki(send_func=send_func, sender_id=sender_id, sender_messages=sender_messages)
                #Если пользователь в запросе ввода города для получения погоды
                elif user_from_db.in_process_weather:
                    handler_weather(send_func=send_func, sender_id=sender_id, sender_messages=sender_messages)



                #Если пользователь в запросе ввода числа
                elif user_from_db.in_process_number:
                    pass

except Exception as error:
    print('Ошибка приложения: ' + str(error))
finally:
    drop_table()