from model import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



from sqlalchemy.pool import SingletonThreadPool
from sqlalchemy.pool import StaticPool

engine = create_engine('sqlite:///sos.db',
    connect_args={'check_same_thread': False},
    poolclass=StaticPool, echo=True)
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

def auth_user(user_username, user_password):
    session = DBSession()
    user = session.query(Student).filter_by(username = user_username, password= user_password).first()
    print(user)
    return user