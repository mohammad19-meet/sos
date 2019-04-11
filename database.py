from model import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



from sqlalchemy.pool import SingletonThreadPool
from sqlalchemy.pool import StaticPool

engine = create_engine('sqlite:///blog.db',
    connect_args={'check_same_thread': False},
    poolclass=StaticPool, echo=True)
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

def create_blog(name, author, date, short_desc, photo, long_desc, bio, pers_photo, bfile):
    blog_object = Blog(
        name = name,
        author = author,
        date = date,
        short_desc = short_desc,
        photo = photo,
        long_desc = long_desc,
        bio = bio,
        pers_photo = pers_photo,
        bfile = bfile
    )
    session.add(blog_object)
    session.commit()


def get_all_blogs():
    blogs = session.query(Blog).all()
    return blogs

def one_blog(id):
    blog = session.query(Blog).filter_by(id = id).first()
    return blog

def create_hotel(name, hotel_date, hotel_desc, price, hotel_photo):
    hotel_object = Hotel(
    	name = name,
    	hotel_date = hotel_date,
    	hotel_desc = hotel_desc,
    	price = price,
    	hotel_photo = hotel_photo
    )
    session.add(hotel_object)
    session.commit()

def get_all_hotels():
	hotels = session.query(Hotel).all()
	return hotels

def get_one_hotel(id):
	hotel = session.query(Hotel).filter_by(id = id).first()
	return hotel

# create_hotel("Hotel?Trivago","29", "anything really", 877886866000000, "https://wallpapercave.com/wp/wp38040.jpg")