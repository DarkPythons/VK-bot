from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey, String, Integer, Boolean, create_engine
from config import BaseSettingsDataBase

db_setting = BaseSettingsDataBase()

URL_DATABASE_SQLITE = "sqlite:///" + db_setting.DB_URL

engine = create_engine(URL_DATABASE_SQLITE, echo=db_setting.ECHO_QUERY_SQL)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    vk_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    in_process: Mapped[bool] = mapped_column(default=False, nullable=False)

    def __repr__(self) -> str:
        return f"Users(vk_id: {self.vk_id})"
    

