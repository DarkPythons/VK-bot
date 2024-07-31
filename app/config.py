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

class BaseSettingApp(BaseConfigSettingInFile):
    TOKEN_BOT:str = Field(min_length=5, max_length=500)
    