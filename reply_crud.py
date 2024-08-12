from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from capstone_main.schemas import ReplyCreate
from capstone_main.models import Reply as ReplyModel
from capstone_main.comment_crud import get_comment_by_id
from capstone_main.log import get_logger

logger = get_logger("reply_crud")


def create_reply(db:Session, reply_payload:ReplyCreate, comment_id:int, movie_id:int|None=None,  user_id:int|None=None):
    db_reply = ReplyModel(
        **reply_payload.model_dump(),
        comment_id=comment_id,
        user_id=user_id,  
    )
    
    db.add(db_reply)
    db.commit()
    db.refresh(db_reply)
    return db_reply


def get_replies(db:Session, comment_id:int, skip:int=0, limit:int=10):
    db_replies = db.query(ReplyModel).filter(ReplyModel.comment_id == comment_id).offset(skip).limit(limit).all()
    if db_replies is None:
        logger.warning("No replies found for comment_id %s", comment_id)
        raise HTTPException(status_code=404, detail="No replies found for this comment")
    return db_replies