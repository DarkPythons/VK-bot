from sqlalchemy.orm import Session

from .models import Base, engine



def create_table():
    """Функция создания всех таблиц по мета классу"""
    Base.metadata.create_all(engine)

def drop_table():
    """Функция удаления всех таблиц по мета классу"""
    Base.metadata.drop_all(engine)

def get_session():
    """Получение сессии для базы данных"""
    return Session(engine)