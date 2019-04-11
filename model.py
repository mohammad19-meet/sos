from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

# Write your classes here :
class Blog(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    author = Column(String)
    date = Column(String)
    short_desc = Column(String)
    photo = Column(String)
    long_desc = Column(String)
    bio = Column(String)
    pers_photo = Column(String)
    bfile = Column(String)


class Hotel(Base):
    __tablename__ = "hotels"
    id = Column(Integer, primary_key= True)
    name = Column(String)
    hotel_date = Column(String)
    hotel_desc = Column(String)
    price = Column(Integer)
    hotel_photo = Column(String)
