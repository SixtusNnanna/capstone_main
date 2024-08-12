from typing import List

from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from capstone_main.auth import (
    get_current_user,
    authenticate_user,
    create_access_token,
    create_user,
    oath2_scheme,
    get_user_by_username
)
from capstone_main.comment_crud import create_movie_comment, get_comments, get_comment_by_id
from capstone_main.crud import (
    create_movies,
    get_movies,
    get_movies_by_id,
    edit_movie,
    get_movies_by_id_and_user_id,
    delete_movie
)



from capstone_main.database import get_db, Base, engine
from capstone_main.models import User as UserModel, Movie as MoviesModel
from capstone_main.ratingcrud import create_rating, get_ratings
from capstone_main.reply_crud import create_reply, get_replies
from capstone_main.schemas import (
    MovieUpate,
    User as UserSchema,
    UserCreate,
    Movie as MovieSchema,
    MovieCreate,
    CommentCreate,
    Comment as CommentSchema,
    ReplyCreate,
    RatingCreate,
    Rating as RatingSchema
)

from capstone_main.models import Rating as RatingModel


from capstone_main.utils import credentials_exception, not_found

from capstone_main.log import get_logger

logger = get_logger("capstone_main")

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/signup", status_code=status.HTTP_201_CREATED, tags=["USER"])
def signup(user:UserCreate, db:Session=Depends(get_db)):
    db_user = get_user_by_username(user.username, db)
    if db_user:
        logger.exception("user {user.username} already exists")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="User already exists")
    db_user = create_user(user, db)

    access_token = create_access_token(db_user.username)
    logger.info("user and access token created successfully")
    return {"access_token": access_token, "token_type": "bearer", "username":db_user.username}


@app.post("/login", tags=["USER"] )
def login(form_data: OAuth2PasswordRequestForm = Depends(), db:Session=Depends(get_db)):
   db_user = authenticate_user(form_data.username, form_data.password, db)
   if  not db_user:
       logger.exception("Invalid credentials")
       raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
   access_token = create_access_token(db_user.username)
   logger.info("User has been authenticated and authorized")
   return {"access_token": access_token, "token_type": "bearer", "username": db_user.username}
    
    
@app.get("/Movies/", tags=["MOVIE"], response_model=List[MovieSchema])
def get_all_movies(db:Session=Depends(get_db), skip:int=0, limit:int=10):
    logger.info("Movies retrieved")
    return get_movies(db=db, skip=skip, limit=limit)


@app.get("/movie/{movie_id}", tags=["MOVIE"], response_model=MovieSchema)
def get_movie_by_id(movie_id: int, db: Session=Depends(get_db)):
    id_movie =  get_movies_by_id(db, movie_id)
    logger.info("Movie %s retriveed succesfully", id_movie)
    return id_movie
    
    
@app.post('/movies/create', status_code=status.HTTP_201_CREATED, tags=["MOVIE"])
def create_movie (moviePayload:MovieCreate, db: Session=Depends(get_db), user : UserSchema=Depends(get_current_user)):
    new_movies =  create_movies(db, moviePayload, user.id)
    logger.info("Movie %s created successfully", new_movies)
    return{
        "message": "Movie created successfully",
        "data": new_movies
    }


@app.put('/movies/{movie_id}', status_code=status.HTTP_200_OK, tags=["MOVIE"])
def update_movie (movie_id:int, moviePayload:MovieUpate, db: Session=Depends(get_db), user : UserSchema=Depends(get_current_user)):
    db_movie = get_movies_by_id_and_user_id(db, movie_id, user.id)
    if db_movie is None:
        logger.warning("Movie is not found")
        raise HTTPException(
            status_code=404,
            detail="Movie not found or User is not allowed to fetch this movie"
        )
    edited = edit_movie(db, movie_id, moviePayload, user.id)
    logger.info("Movie is Updated successfully")
    return {
        "message": "Movie Updated successfully",
        "data": edited
    }

@app.delete('/movies/{movie_id}', status_code=status.HTTP_200_OK, tags=["MOVIE"])
def delete__movie (movie_id:int, db: Session=Depends(get_db), user : UserSchema=Depends(get_current_user)):
    db_movie = get_movies_by_id_and_user_id(db, movie_id, user.id)
    if db_movie is None:
        logger.warning("Movie is not found or user  access denied")
        raise HTTPException(
            status_code=404,
            detail="Movie not found or User is not allowed to fetch this movie"
        )
    logger.info("Movie  deleted successfully")
    deleted_movie = delete_movie(db, movie_id, user.id)
    return{
        "message": "Movie deleted successfully",
    }


@app.post("/movies/{movie_id}/create_comment", tags=["COMMENT"])
def create_comment(movie_id: int, comment: CommentCreate, db: Session = Depends(get_db), user: UserSchema = Depends(get_current_user)):
    new_comment = create_movie_comment(movie_id, db, comment, user.id)
    logger.info("User added comment for a movie with id %s", movie_id)
    return {
        "message": "Comment created successfully",
        "data": new_comment
    }


@app.get("/movies/{movie_id}/comments", tags=["COMMENT"], response_model=List[CommentSchema])
def get_comments_of_a_movie(movie_id: int, db: Session = Depends(get_db)):
    movie_comments = get_comments(db, movie_id)
    logger.info("List of comments for movie %s retrieved successfully", movie_id)
    return movie_comments


@app.post("/comments/{comment_id}/comments", tags=["NESTED COMMENTS"])
def create_nested_comment(comment_id: int, reply: ReplyCreate, db: Session = Depends(get_db), user: UserSchema = Depends(get_current_user)):
    db_comment = get_comment_by_id(db, comment_id)
    if db_comment is None:
        logger.warning("Comment with id of  %s is  not found", comment_id)
        raise not_found
    logger.info("User added a reply to a comment with id %s", comment_id)
    new_reply = create_reply(db=db, reply_payload=reply, comment_id=comment_id, movie_id=db_comment.movie_id, user_id=user.id)

    return{
        "message": "Reply created successfully",
        "data": new_reply
    }


@app.post("/movie/{movie_id}/create_rating", tags=["RATING"])
def create_movie_rating(movie_id: int, rating: RatingCreate, db: Session = Depends(get_db), user: UserSchema = Depends(get_current_user)):
    rate = create_rating(db, rating, movie_id, user.id)
    logger.info("User rated movie %s successfully", movie_id)
    return {
        "message": "Rating created successfully",
        "data": rate
    }


@app.get("/movie/rating/{movie_id}", tags=["RATING"], status_code=status.HTTP_200_OK)
def get_movie_rating( movie_id:int,  db:Session=Depends(get_db)):
   average_ratting = get_ratings(db, movie_id)
   logger.info("Rating for movie %s retrieved successfully", movie_id)
   return {
       "message": "Average rating for movie retrieved successfully",
       "data": average_ratting
   }








