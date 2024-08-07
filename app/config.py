from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class BaseConfigSettingInFile(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        #Чувствительность к регистрку
        case_sensitive=True
    )

class BaseSettingsDataBase(BaseConfigSettingInFile):
    DB_URL:str = Field(min_length=3, max_length=100, default='database.db')
    ECHO_QUERY_SQL:bool = Field(default=False)

class BaseSettingApp(BaseConfigSettingInFile):
    TOKEN_BOT:str = Field(min_length=5, max_length=500)
    PROGRAM_IN_DEBUG:bool = Field(default=True)
    

#Здесь может быть любой headers, главное валидный для requests
headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"
    }

class BaseConnectSettingsAPI(BaseConfigSettingInFile):
    headers:dict = Field(default=headers)
    #Этот токен можно получить, пройдя легкую регистрацию: https://openweathermap.org/
    TOKEN_WEATHER:str = Field(min_length=3, max_length=400)
    