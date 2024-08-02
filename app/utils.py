from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
import wikipedia
wikipedia.set_lang('ru')

keyboard_hello = VkKeyboard(one_time=True)
keyboard_hello.add_button('Информация из Wiki', color=VkKeyboardColor.POSITIVE)
keyboard_hello.add_line()
keyboard_hello.add_button('Получить интереный факт', color=VkKeyboardColor.POSITIVE)
keyboard_hello.add_line()
keyboard_hello.add_button('Заметки', color=VkKeyboardColor.POSITIVE)
keyboard_hello.add_line()
keyboard_hello.add_button('Информация о погоде', color=VkKeyboardColor.POSITIVE)
keyboard_hello.add_line()
keyboard_hello.add_openlink_button('GitHub проекта', 'https://github.com/VoblaSuperFish/VkBot')


keyboard_no_command = VkKeyboard(one_time=True)
keyboard_no_command.add_button('Помощь', color=VkKeyboardColor.POSITIVE)
keyboard_no_command.add_line()
#Ссылка поддержки может быть любой
keyboard_no_command.add_openlink_button('Поддержка', link='https://github.com/VoblaSuperFish/VkBot')

keyboard_exit = VkKeyboard(one_time=False)
keyboard_exit.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)



class SendingMessageUser:
    def __init__(self, authorise):
        self.authorise = authorise

    def write_message(self, sender_id, message):
        self.authorise.method(
            'messages.send', 
            {'user_id' : sender_id, 'message' : message, 'random_id' : get_random_id()}
            )

    def send_sticker(self, sender_id, sticker_number):
        """Функция для отправления стикера пользователю по айди стикера"""
        try:
            self.authorise.method('messages.send', {'user_id' : sender_id, 'sticker_id' : sticker_number, 'random_id' : get_random_id()})
            return True
        except:
            return False


    def write_message_hello(self, sender_id, message):
        """Функция для приветствия пользователя + добавление кнопок"""
        self.authorise.method('messages.send', {'user_id' : sender_id, 'message' : message, 'random_id' : get_random_id(), 'keyboard' : keyboard_hello.get_keyboard()})

    def write_message_help(self, sender_id, message):
        """Функция для отображения помощи пользователю"""
        self.authorise.method('messages.send', {'user_id' : sender_id, 'message' : message, "random_id" : get_random_id(), 'keyboard' : keyboard_hello.get_keyboard()})

    def write_message_no_search(self, sender_id, message):
        """Если пользователь ввел команду, которой пока нет у бота"""
        self.authorise.method('messages.send', {'user_id' : sender_id, 'message' : message, "random_id" : get_random_id(), 'keyboard' : keyboard_no_command.get_keyboard()})

    def wiki_start_text(self, sender_id, message):
        """Если пользователь захотел получить информацию из Wiki"""
        self.authorise.method('messages.send', {'user_id' : sender_id, 'message' : message, "random_id" : get_random_id(), 'keyboard' : keyboard_exit.get_keyboard()})

    def write_message_all_exit(self, sender_id, message):
        """Если пользователь ввел Отмена или /stop"""
        self.authorise.method('messages.send', {'user_id' : sender_id, 'message' : message, "random_id" : get_random_id(), 'keyboard' : keyboard_hello.get_keyboard()})



def get_info_from_wiki(search_text):
    try:
        #Получение страницы в википедии по запросу
        full_content = wikipedia.page(search_text)
        response = full_content.content[:300] + "...\n" + "Ссылка на статью: " + full_content.url
        return {'status' : 200, 'content' : response}
    except:
        search_list = wikipedia.search(search_text, results=5)
        if len(search_list) > 0:   
            #Возвращаем строку возможныx значений, которые имел ввиду пользователь
            return {'status' : 301, 'content' : ", ".join(search_list)}
        return {'status' : 404, 'content' : None}
        