from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.models import Comment as CommentModel
from app.schemas import Comment as CommentSchema, CommentCreate, User as UserSchema
from app.crud import get_movies_by_id
from app.log import get_logger



logger = get_logger("comment_crud")



def create_movie_comment(movie_id:int, db:Session, comment:CommentCreate, user_id:int|None=None):
    db_movie = get_movies_by_id(db, movie_id)
    if not db_movie:
        logger.warning("Movie is not found")
        raise HTTPException(status_code=404, detail="Movie not found")
    db_comment = CommentModel (
        **comment.model_dump(),
        movie_id=movie_id,
        user_id=user_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_comments(db:Session, movie_id:int, skip:int=0, limit:int=10):
    db_movie = get_movies_by_id(db, movie_id)
    if not db_movie:
        logger.warning("Movie is not found")
        raise HTTPException(status_code=404, detail="Movie not found")
    db_comment = db.query(CommentModel).filter(CommentModel.movie_id == movie_id).offset(skip).limit(limit).all()
    return db_comment



def get_comment_by_id(db:Session, comment_id:int):
    return db.query(CommentModel).filter(CommentModel.id == comment_id).first()