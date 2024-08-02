from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field





class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str



class User(UserBase):
    pass 

    model_config = ConfigDict(from_attributes=True)



class RatingBase(BaseModel):
    rating: float = Field(None, title="Movie Rating", ge=0, le=10, description="The rating of the movie from 0 to 10")


class RatingCreate(RatingBase):
    pass


class Rating(RatingBase):

    model_config = ConfigDict(from_attributes=True)


class MovieBase(BaseModel):
    title: str
    description: str
    duration: int = Field(..., title="Movie Duration", ge=0, description="The duration of the movie in minutes")


class MovieCreate(MovieBase):
    pass


class MovieUpate(MovieBase):
    title: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[int] = None


class Movie(MovieBase):
    user_id: int 
    release_date: datetime = datetime.now()
    average_rating :  Optional[float] = None
    comments :List["Comment"] = []

   
    model_config = ConfigDict(from_attributes=True)



class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
   
    pass 


class Comment(CommentBase):
    id:int
    user_id: int 
    created_at: datetime = datetime.now()
    replies: List["Reply"] = []

    model_config = ConfigDict(from_attributes=True)





class ReplyBase(BaseModel):
    content: str


class ReplyCreate(ReplyBase):
    pass


class Reply(ReplyBase):
    user_id: int 
    created_at: datetime = datetime.now()


    model_config = ConfigDict(from_attributes=True)






