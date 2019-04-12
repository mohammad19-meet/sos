from model import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()


def auth_user(username, password):
    session = DBSession()
    user = session.query(Student).filter_by(username = username, password= password).first()
    print(user)
    return user

def add_user(username,password,role):
    user_object = User(username=username,
    password=password,
    role=role)
    session.add(user_object)
    session.commit()

# add_user("user", "pass", 0)