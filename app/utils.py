
from vk_api.utils import get_random_id



class SendingMessageUser:
    def __init__(self, authorise):
        self.authorise = authorise

    def write_message(self, sender_id, message):
        self.authorise.method('messages.send', {'user_id' : sender_id, 'message' : message, 'random_id' : get_random_id()})

    def send_sticker(self, sender_id, sticker_number):
        """Функция для отправления стикера пользователю по айди стикера"""
        try:
            self.authorise.method('messages.send', {'user_id' : sender_id, 'sticker_id' : sticker_number, 'random_id' : get_random_id()})
            return True
        except:
            return False


