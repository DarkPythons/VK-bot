from loguru import logger

class BaseLoggings:
    def __init__(self, *, 
        file:str, rotation:str, level:str,          
        format:str="{time} {level} {message}", 
        seriallize:bool=False):

        logger.add(file, format=format, level=level, rotation=rotation, 
                compression='zip',serialize=seriallize)
    
    #Уровень лога расположен от самого лёгкого до самого критичного
    def debug(self, message):
        logger.debug(message)
    def info(self, message):
        logger.info(message)
    def warning(self, message):
        logger.warning(message)
    def error(self, message):
        logger.critical(message)
    def critical(self, message):
        logger.critical(message)

#Настройка, куда будут идти все логи
logs = BaseLoggings(file='logs/log_app/log_app.log', rotation='100 MB', level='DEBUG')
#Куда будут идти только логи об ошибках и выше
logs_except = BaseLoggings(file='logs/log_app/log_app_ex.log', rotation='100 MB', level='ERROR')