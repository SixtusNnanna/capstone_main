import os
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from passlib.context import CryptContext
from dotenv import load_dotenv

from capstone_main.schemas import User as UserSchema, UserCreate
from capstone_main.models import User as UserModel
from capstone_main.database import get_db
from capstone_main.log import get_logger

load_dotenv()

logger = get_logger("auth")


pwd_context = CryptContext(schemes=["bcrypt"])
oath2_scheme = OAuth2PasswordBearer(tokenUrl="login")


ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 15
SECRET_KEY =  os.getenv("SECRET_KEY")


def get_user_by_username(username:str, db:Session):
    db_user = db.query(UserModel).filter(UserModel.username == username).first()
    if db_user is None:
        logger.warning("User not found")
        return None
    logger.info("user %s has been found", username)
    return db_user


def authenticate_user(username:str, password:str, db:Session):
    db_user = get_user_by_username(username, db)
    if not db_user or not  pwd_context.verify(password, db_user.hashed_password):
        logger.warning("Invalid username or password")
        return False
    return db_user






def create_user(user: UserCreate, db:Session):
    hashed_password = pwd_context.hash(user.password)
    db_user = UserModel(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



def create_access_token(username:str, expire_delta:timedelta|None = None):
    to_encode = {"sub":username}
    if expire_delta:
        logger.error("Token has expired")
        expire = datetime.utcnow() + timedelta(seconds=expire_delta)
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)   
    to_encode.update({"exp": expire})
    logger.info("Token has been created")  
    return jwt.encode(to_encode, SECRET_KEY, ALGORITHM)


def get_current_user(db:Session =Depends(get_db), token:str= Depends(oath2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    logger.info("Attempting to decode access token")
    try:
        logger.info("Access token has been decoded")  
        payload = jwt.decode(token,SECRET_KEY,ALGORITHM)
        username:str = payload.get('sub')
        if username is None:
            logger.error("invalid credentials")
            raise credentials_exception
    except JWTError:
        logger.exception("JWT Error")
        raise credentials_exception
    user = get_user_by_username(username, db)
    if user is None:
        logger.error("User not found")
        raise credentials_exception
    return user
