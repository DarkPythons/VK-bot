import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from config import BaseSettingApp
from utils import SendingMessageUser
from text import hello_user #type: ignore

setting_app = BaseSettingApp()

authorise = vk_api.VkApi(token=setting_app.TOKEN_BOT)
longpoll = VkLongPoll(authorise)

send_func = SendingMessageUser(authorise)

#Прослушивание сообщений от бота
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        sender_messages = event.text
        sender_id = event.user_id

        if sender_messages.lower() in ['старт', 'привет', 'hello', '/start']:
            send_func.send_sticker(sender_id, 21)
            send_func.write_message_hello(sender_id, hello_user)
        

    