
# MOVIE LISTING API
## CAPSTONE PROJECT BY SIXTUS NNANNA OMEJE

This API is my third/last term project in altschool.

## Table of Contents

1. [Installation](#installation)
2. [API Endpoints](#api-endpoints)
3. [Testing](#configuration)

## Installation

### Prerequisites

- Python 3.9 upto the lates version(Download from (#python.org))
- DEPENDECIES (`pip install -r requirement.txt` to install all dependencies)

### Steps

1. **Clone the repository:**

    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Create a virtaul enviroment and install the dependecies**

    ```sh
    python3 -m venv venv
    ```

     ```sh
    pip3 install -r requirements.txt
    ```

3. **Run the application: Go a step back from the root directory and run:**

    ```
   uvicorn app:main.app --reload
    ```

4. **The application will be available at:**

    ```
    http://localhost:8000 
    ```
5. **The swagger documentation will be available at:**

    ```
    http://localhost:8000/docs
    ```

## API Endpoints
### I have 12 Api endpoints

1. **Signup-For signing up new users, its avaialable at :**
    ```
    http://localhost:8000/docs#/USER/signup_signup_post
    ```
2. **login-For authentication and authorisation of users, its avaialable at :**
    ```
    http://localhost:8000/docs#/USER//login_login_post
    ```
3. **Get Movies - this end points get the total number of movies avaialable:**
    ```
    http://localhost:8000/docs#/MOVIE/get__movies_Movies__get
    ```

4. **Get Movie by Id - GET movie/{movie_id}  avaialable at:**
    ```
    http://localhost:8000/docs#/MOVIE/get_movie_by_id_movie__movie_id__get
    ```

5. **Create Movie: POST /movies/create :**
    ```
    http://localhost:8000/docs#/MOVIE/create_movie_movies_create_post
    ```

6. **Update Movie PUT movies/{movie_id} :**
    ```
    http://localhost:8000/docs#/MOVIE/update_movie_movies__movie_id__put
    ```

7. **Delete Post: DELETE movies/{movie_id}**
    ```
    http://localhost:8000/docs#/MOVIE/delete__movie_movies__movie_id__delete
    ```

8. **Adding comment to a movie : POST "/movies/{movie_id}/create_comment",**
    ```
    http://localhost:8000/docs#/COMMENT/create_comment_movies__movie_id__create_comment_post
    ```

9. **Getting comments of a movie using movie id : GET /movies/{movie_id}/comments**
    ```
    http://localhost:8000/docs#/COMMENT/get_comments_of_a_movie_movies__movie_id__comments_get
    ```
10. **Adding Nested comment to a comment: POST /comments/{comment_id}/comments**
    ```
    http://localhost:8000/docs#/NESTED%20COMMENTS/create_nested_comment_comments__comment_id__comments_post
    ```
11. **Rating a movie: POST /movie/{movie_id}/create_rating:**
    ```
    http://localhost:8000/docs#/RATING/create_movie_rating_movie__movie_id__create_rating_post
    ```

12. **GET Rating of a movie : GET /movie/rating/{movie_id}**
    ```
    http://localhost:8000/docs#/RATING/get_movie_rating_movie_rating__movie_id__get
    ```


### Environment Variables

"db_url" = Database Url
ALGORITHM = Algorthing for creating access token
SECRET_KEY = Secret Key for creating access token

Create a `.env` file in the root directory and add your environment variables:

## Testing


### Steps

1. **CD into the root directory**
    ```
    cd capstone_main
    ```


1. **Run pytest on your terminal**
    ```
    pytest
    
    ```