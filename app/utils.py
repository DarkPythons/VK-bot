from vk_api.utils import get_random_id
import wikipedia
import requests
import datetime

from keyboards import keyboard_hello,keyboard_no_command,keyboard_exit
from text import code_smile, no_found_city_text, exceptionn_500_text
from config import BaseConnectSettingsAPI

connect_setting = BaseConnectSettingsAPI()

wikipedia.set_lang('ru')


class SendingMessageUser:
    def __init__(self, authorise):
        self.authorise = authorise

    def write_message(self, sender_id, message):
        """Функция отправки сообщений"""
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



    def write_message_all_exit(self, sender_id, message):
        """Если пользователь ввел Отмена или /stop"""
        self.authorise.method('messages.send', {'user_id' : sender_id, 'message' : message, "random_id" : get_random_id(), 'keyboard' : keyboard_hello.get_keyboard()})
    



    #Объеденить три функции в одну (DRY)
    def wiki_start_message(self, sender_id, message):
        """Если пользователь захотел получить информацию из Wiki"""
        self.authorise.method('messages.send', {'user_id' : sender_id, 'message' : message, "random_id" : get_random_id(), 'keyboard' : keyboard_exit.get_keyboard()})

    def weather_start_message(self, sender_id, message):
        """Если пользователь захотел получить информацию о погоде"""
        self.authorise.method('messages.send', {'user_id' : sender_id, 'message' : message, "random_id" : get_random_id(), 'keyboard' : keyboard_exit.get_keyboard()})

    def number_start_message(self, sender_id, message):
        """Если пользователь захотел получить интересный факт о числе"""
        self.authorise.method('messages.send', {
            'user_id' : sender_id, 'message' : message,
            'random_id' : get_random_id(), 'keyboard' : keyboard_exit.get_keyboard()
        })

def get_info_from_wiki(search_text):
    """Функци получения информации из Wiki по заданному слову"""
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
        

def smile_for_weather(weather_street):
    """В зависимости от уличной погоды функция выбирает смайлик"""
    if weather_street in code_smile:
        return code_smile[weather_street]
    else:
        return "Смайлика нет :("
    
def get_full_response_text(json_response):
    """Преобразование ответа от API погоды из json в текст"""
    time_sunrise = datetime.datetime.fromtimestamp(json_response['sys']['sunrise'])
    time_sunset = datetime.datetime.fromtimestamp(json_response['sys']['sunset'])
    time_day = time_sunset - time_sunrise
    itog_response = f"""
    Полученная информация:
    Город: {json_response['name']}
    Температура: {json_response['main']['temp']} °C
    Влажность: {json_response['main']['humidity']} %
    Давление: {json_response['main']['pressure']} мм рт. ст.
    Скорость ветра: {json_response['wind']['speed']} м/с
    Время восхода солнца: {time_sunrise}
    Время заказа солнца: {time_sunset}
    Продолжительность дня: {time_day}
    Погода на улице: {smile_for_weather(json_response['weather'][0]['main'])}
    """
    return itog_response

def info_from_api_weather(search_text):
    """Функция получения информации о погоде из API"""
    try:
        city = search_text
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&lang=ru&units=metric&appid={connect_setting.TOKEN_WEATHER}'
        response = requests.get(url, headers=connect_setting.headers)
        if response.status_code in [200,201]:
            text_response = get_full_response_text(response.json())
            return {'status' : 200, 'content' : text_response}
        elif response.status_code == 404:
            return {'status' : 404, 'content' : no_found_city_text}
        return {"status" : 500, 'content' : exceptionn_500_text}
    except ValueError as Error:
        print(Error)
        return {"status" : 500, 'content' : exceptionn_500_text}