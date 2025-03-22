from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table, DateTime, Boolean, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime


Base = declarative_base()

user_tag_association = Table(
    'user_tag_association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

place_tag_association = Table(
    'place_tag_association',
    Base.metadata,
    Column('place_id', Integer, ForeignKey('places.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(100))
    # name = Column(String(100))
    
    preferences = relationship("Tag",
                               secondary=user_tag_association,
                               back_populates="users")
    visits = relationship("Visit", back_populates="user")
    
    def __repr__(self):
        return f"<User {self.username}, name - {self.name}>"


class Place(Base):
    __tablename__ = 'places'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    photo = Column(Text)  # URL or path to photo
    description = Column(Text)
    
    tags = relationship("Tag",
                        secondary=place_tag_association,
                        back_populates="places")
    visits = relationship("Visit", back_populates="place")
    
    def __repr__(self):
        return f"<Place {self.name}>"


class Tag(Base):
    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    
    users = relationship("User",
                         secondary=user_tag_association,
                         back_populates="preferences")
    places = relationship("Place",
                          secondary=place_tag_association,
                          back_populates="tags")
    
    def __repr__(self):
        return f"<Tag {self.name}>"


class Visit(Base):
    __tablename__ = 'visits'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    place_id = Column(Integer, ForeignKey('places.id'))
    visited_at = Column(DateTime, default=datetime.now)
    rating = Column(Integer)
    
    user = relationship("User", back_populates="visits")
    place = relationship("Place", back_populates="visits")
    
    def __repr__(self):
        return f"<Visit user_id={self.user_id} place_id={self.place_id}>"


class Moderator(Base):
    __tablename__ = 'moderators'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(200), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Moderator {self.username}>"
