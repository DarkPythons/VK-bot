from sqlalchemy import select, insert, update, delete
from.models import Users
from sqlalchemy.orm import Session

class UsersOrm:
    def __init__(self, session: Session):
        self.session = session
    
    def create_user_in_db(self, sender_id):
        """Добавление пользователя в базу данных"""
        object_user = Users(
            vk_id = sender_id,
            #Все остольные параметры стоят по умолчанию
        )
        self.session.add(object_user)
        self.session.commit()
    
    def get_user_from_db(self, user_id):
        """Получение информации о пользователе по его id"""
        query = select(Users).where(Users.vk_id == user_id)
        result = self.session.execute(query)
        return result.mappings().first()

    def update_status_user_wiki(self, user_id, *, status: bool):
        """Обновление статуса пользователя, на ожидание ввода Wiki запроса"""
        query = update(Users).values(in_process=True, in_process_wiki=status).where(Users.vk_id == user_id) 
        self.session.execute(query)
        self.session.commit()

    def update_status_user_weather(self, user_id:int, *, status: bool):
        """Обновление статуса пользователя, на ожидание ввода города для получения погоды"""
        query = update(Users).values(in_process=True, in_process_weather=status).where(Users.vk_id == user_id)
        self.session.execute(query)
        self.session.commit()

    def update_full_process(self, user_id, *, full_status: bool):
        """Обновление всех статусов ожидания ввода от пользователя, в основном используется
        при команде /stop или ввода Отмена"""
        query = update(Users).values(
        in_process=full_status,
        in_process_wiki=full_status,
        in_process_weather=full_status,
        in_process_number=full_status,
        in_process_create_note=full_status,
        in_process_delete_note=full_status,
        ).where(Users.vk_id == user_id)
        self.session.execute(query)
        self.session.commit()