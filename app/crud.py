from typing import List

from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.schemas import(
     Movie as MovieSchema, MovieCreate, 
     MovieUpate, Comment as CommentSchema, 
     Reply as ReplySchema)
from app.models import (
    Movie as MovieModel,
    Rating as RatingModel,
)
from app.log import get_logger


logger = get_logger("crud")

def get_movies(db:Session, skip:int=0, limit:int=10):
    db_movies = db.query(MovieModel).offset(skip).limit(limit).all()
    movies = []
    for db_movie in db_movies:
        ratings = db.query(RatingModel).filter(RatingModel.movie_id == db_movie.id).all()
        average_rating = sum(rating.rating for rating in ratings) / len(ratings) if ratings else 0
        logger.info(" Average rating for db_movies")
        movie_data = {
            **jsonable_encoder(db_movie),
            "average_rating": average_rating,
            "comments": db_movie.comments,
        }
        movies.append(movie_data)


    return movies
    
    
def get_movies_by_id( db:Session,movie_id:int):
    db_movies = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not db_movies:
        logger.warning("Movie is not found")
        raise HTTPException(status_code=404, detail="Movie not found")
    ratings = db.query(RatingModel).filter(RatingModel.movie_id == movie_id).all()
    average_rating = sum(rating.rating for rating in ratings) / len(ratings) if ratings else 0
    movie_data = {
            **jsonable_encoder(db_movies),
            "average_rating": average_rating,
            "comments": db_movies.comments,
        }
    return movie_data

    
def get_movies_by_id_and_user_id( db:Session, movie_id:int, user_id:int):
    return db.query(MovieModel).filter(MovieModel.id == movie_id, MovieModel.user_id == user_id).first()


def create_movies(db: Session, movie_paylaod:MovieCreate, user_id:int|None=None):
    db_movie = MovieModel (
        **movie_paylaod.model_dump(),
        user_id=user_id
    )
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


def edit_movie(db: Session, movie_id:int, movie_paylad:MovieUpate, user_id:int|None=None):
    movie = get_movies_by_id_and_user_id( db, movie_id, user_id)
    if not movie:
        logger.warning("Movie not found or User is not allow to edit this movie")
        raise HTTPException(status_code=404, detail="Movie not found or User cannot fetch this movie")
    movie_payload_to_dict = movie_paylad.model_dump(exclude_unset= True)

    for k, v in movie_payload_to_dict.items():
        setattr(movie, k,v)

    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie


def delete_movie(db: Session, movie_id: int, user_id: int | None = None):
    movie = get_movies_by_id_and_user_id(db, movie_id, user_id)
    if movie is None:
        logger.warning("Movie not found or User cannot fetch this movie")
        return None
    db.query(RatingModel).filter(RatingModel.movie_id == movie_id).delete(synchronize_session=False)
    db.delete(movie)
    db.commit()

 