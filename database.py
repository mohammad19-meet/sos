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

