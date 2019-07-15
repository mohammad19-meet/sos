from model import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()


def auth_user(username, password):
    session = DBSession()
    user = session.query(User).filter_by(username = username, password= password).first()
    print(user)
    return user

def add_user(username,password,role):
    user_object = User(username=username,
    password=password,
    role=role)
    session.add(user_object)
    session.commit()

def add_story(name, title, the_story):
	summary=the_story[0:20]
	story_object= Story(name=name, title=title, the_story=the_story, summary=summary)
	session.add(story_object)
	session.commit()

def story_by_name(name):
	session = DBSession()
	stories= session.query(Story).filter_by(name=name).all()
	return stories




# add_user("user", "pass", 0)