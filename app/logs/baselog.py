"""Модуль для настроек логирования приложения"""

from loguru import logger

class BaseLoggings:
    def __init__(self, *, 
        file:str, rotation:str, level:str,          
        format:str="{time} {level} {message}", 
        seriallize:bool=False):
        """
        Инициализация базовых настроек для логирования
        >file - файл, куда будут помещены все логи.
        >rotation - параметр, при котором определяется причина обновления
        файла логов (может быть вес файла или время).
        >level - начиная с какого уровня отлавливать логи.
        >format - формат записи логов в файл.
        >seriallize - сериализация данных, если будет True, логи
        будут записываться в формате json, но и расширение нужно json.
        >>>см. https://loguru.readthedocs.io/en/stable/overview.html
        """
        logger.add(file, format=format, level=level, rotation=rotation, 
                compression='zip',serialize=seriallize)
    
    def debug(self, message):
        """Меньший уровень лога, в основном для отлаживания программы на уровне
        проектирования"""
        logger.debug(message)
    def info(self, message):
        """Подходит для пометки основной информации об приложении"""
        logger.info(message)
    def warning(self, message):
        """Лог, на который стоит обратить внимание"""
        logger.warning(message)
    def error(self, message):
        """Сообщение об возникшей ошибке приложения"""
        logger.error(message)
    def critical(self, message):
        """Критическая ошибка, которая влияет на жизнь программы"""
        logger.critical(message)

#Настройка, куда будут идти все логи
logs = BaseLoggings(file='logs/log_app/log_app.log', rotation='100 MB', level='DEBUG')
#Куда будут идти только логи об ошибках и выше
logs_except = BaseLoggings(file='logs/log_app/log_app_ex.log', rotation='100 MB', level='ERROR')