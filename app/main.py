import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from config import BaseSettingApp

setting_app = BaseSettingApp()

authorise = vk_api.VkApi(token=setting_app.TOKEN_BOT)
longpoll = VkLongPoll(authorise)


#Прослушивание сообщений от бота
for event in longpoll.listen():
    pass