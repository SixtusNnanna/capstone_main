from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime,Text, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.database import Base



class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    movies = relationship("Movie", back_populates="user")
    ratings = relationship("Rating", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    replies = relationship("Reply", back_populates="user")



class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    title = Column(String, index=True)
    release_date = Column(DateTime, default=datetime.now())
    description = Column(Text)
    duration = Column(Integer)
    user_id  = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="movies")
    ratings = relationship("Rating", back_populates="movie", uselist=False, cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="movie")
   


class Rating(Base):
    __tablename__ = 'ratings'
    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Float)
    movie_id = Column(Integer, ForeignKey("movies.id"),)
    user_id = Column(Integer, ForeignKey("users.id"))

    movie = relationship("Movie", back_populates="ratings")
    user = relationship("User", back_populates="ratings")


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.now())

    movie_id = Column(Integer, ForeignKey("movies.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    movie = relationship("Movie", back_populates="comments")
    user = relationship("User", back_populates="comments")
    replies = relationship("Reply", back_populates="comment")



class Reply(Base):
    __tablename__ ='replies'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.now())

    comment_id = Column(Integer, ForeignKey("comments.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    comment = relationship("Comment", back_populates="replies")
    user = relationship("User", back_populates="replies")
   

