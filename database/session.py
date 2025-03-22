from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from os import getenv
from database.models import User, Place, Tag, Visit, Moderator


DATABASE_URL = getenv('DATABASE_URL')
# DATABASE_URL = ''

engine = create_engine(DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
Base.query = Session.query_property()


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)


def create_user(id: int, username: str = None,
                           preferences: list = None,
                           visits: list = None):
    session = Session()

    try:
        new_user = User(id=id, username=username,
                                   preferences=preferences, visits=visits)

        session.add(new_user)
        session.commit()
        session.refresh()
    
    except Exception as err:
        session.rollback()
    
    finally:
        session.close()


def create_place(id: int, name: str, tags: list, description: str=None,
                            photo: str=None, visits: list=None):
    session = Session()

    try:
        new_place = Place(id=id, name=name, tags=tags,
                                    description=description,
                                    photo=photo, visits=visits)
        
        session.add(new_place)
        session.commit()
        session.refresh()
    
    except Exception as err:
        session.rollback()
    
    finally:
        session.close()


def create_tag(id: int, name: str,
                            users: list=None, places: list=None):
    session = Session()

    try:
        new_tag = Tag(id=id, name=name,
                                users=users, places=places)
        
        session.add(new_tag)
        session.commit()
        session.refresh()
    
    except Exception as err:
        session.rollback()
    
    finally:
        session.close()


def create_visit(id: int, user_id: int, place_id: int,
                            visited_at: str, rating:int):
    session = Session()

    try:
        new_visit = Visit(id=id, user_id=user_id,
                                  place_id=place_id,
                                  visited_at=visited_at, rating=rating)
        
        session.add(new_visit)
        session.commit()
        session.refresh()
    
    except Exception as err:
        session.rollback()
    
    finally:
        session.close()


def create_moderator(id: int, username: str,
                                    password_hash: str, is_active: bool,
                                    created_at: str):
    session = Session()

    try:
        new_moderator = Tag(id=id, username=username,
                                password_hash=password_hash,
                                is_active=is_active, created_at=created_at)
        
        session.add(new_moderator)
        session.commit()
        session.refresh()
    
    except Exception as err:
        session.rollback()
    
    finally:
        session.close()


def get_places(place_id: int):
    session = Session()

    try:
        places = session.query(Place).filter(Place.id == place_id)

        return places
    
    except Exception as err:
        return 'Error while getting places'

    finally:
        session.close()


def get_tags(id, from_places) -> list:
    session = Session()

    try:
        match from_places:
            case True:
                tags = session.query(Place).filter(Place.id == id).first().tags

                return tags
            
            case False:
                tags = session.query(User).filter(User.id == id).first().preferences

                return tags

    except Exception as err:
                return 'Error while getting tags'

    finally:
        session.close()


def get_visits(place_id: int):
    session = Session()

    try:
        visits = session.query(Place).filter(Place.id == place_id).visits

        return visits
    
    except Exception as err:
        return 'Error while getting visits'

    finally:
        session.close()
