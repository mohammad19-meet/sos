from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

# Write your classes here :
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    color=Column(String)
    picture=Column(String)
    price=Column(Integer)
    tag=Column(String)
    amount_av=Column(Integer)
    info=Column(String)


class Story(Base):
    __tablename__ = "stories"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    story=Column(String)
    name=Column(String)
    age=Column(Integer)
    gender=Column(String)
    place=Column(String)
    summery=Column(String)

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    time=Column(String)
    date=Column(String)
    place=Column(String)
    info=Column(String)
    picture=Column(String)
    is_coming=Column(Boolean)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String, unique=True)
    password = Column(String)
    role = Column(Integer)
