from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session


from capstone_main.crud import get_movies_by_id
from capstone_main.models import Rating as RatingModel
from capstone_main.schemas import Rating as RatingSchema, RatingCreate
from capstone_main.utils import average_rating
from capstone_main.log  import get_logger

logger = get_logger("rating_crud")


def get_ratings(db:Session, movie_id:int):
    db_movies = get_movies_by_id(db, movie_id)
    if not db_movies:
        logger.warning("Movie is not found")
        raise HTTPException(status_code=404, detail="Movie not found")
    db_ratings = db.query(RatingModel).filter(RatingModel.movie_id == movie_id).all()
    average_rating = sum(rating.rating for rating in db_ratings)/len(db_ratings) if db_ratings else 0
    return average_rating



def create_rating(db:Session, ratingPayload:RatingCreate, movie_id:int, user_id:int| None = None) -> float: 
    db_movies = get_movies_by_id(db, movie_id)
    if not db_movies:
        logger.warning("Movie is not found")
        raise HTTPException(status_code=404, detail="Movie not found")
    db_rating = db.query(RatingModel).filter(RatingModel.movie_id == movie_id, RatingModel.user_id == user_id).first()
    
    if db_rating:
        logger.warning("This movie has already been rated")
        raise HTTPException(status_code=400, detail="You have already rated this movie")
    db_rating = RatingModel(
        **ratingPayload.model_dump(),
        movie_id=movie_id,
        user_id=user_id,
    )
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating





