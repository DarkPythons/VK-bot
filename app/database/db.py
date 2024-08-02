from .models import Base, engine
from sqlalchemy.orm import Session


def create_table():
    Base.metadata.create_all(engine)

def drop_table():
    Base.metadata.drop_all(engine)

def get_session():
    #with Session(engine) as session:
    #    yield session
    return Session(engine)