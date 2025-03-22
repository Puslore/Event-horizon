from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from os import getenv


DATABASE_URL = getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

Base = declarative_base()
Base.query = Session.query_property()


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


def init_db():
    from database.models import User, Place, Tag, Visit, Moderator
    Base.metadata.create_all(bind=engine)
