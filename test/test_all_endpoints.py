from typing import Literal

import pytest
import warnings


from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from capstone_main.main import app
from capstone_main.database import Base, get_db
from capstone_main.schemas import MovieCreate, CommentCreate, ReplyCreate, RatingCreate




SQLALCHEMY_DATABASE_URL = "sqlite:///"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

movie_data = {
    "title": "Test Movie",
    "release_date": "2023-01-01",
    "description": "A test movie",
    "duration": 120
}

updated_movie_data = {
    "title": "Updated Movie",
    "release_date": "2023-01-01",
    "description": "Updated movie description",
    "duration": 100
}

comment_data = {
    "content": "Great movie!"
}

reply_data = {
    "content": "I agree!"
}

rating_data = {
    "rating": 5
}



@pytest.fixture(scope="module")
def test_client():
    return TestClient(app)


@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


#USER TESTS

@pytest.mark.parametrize("username, password, email", [("username", "password", "email@example.com")])
def test_signup(test_client: TestClient, setup_database: None, username: Literal['username'], password: Literal['password'], email: Literal['email@example.com']):
    response = test_client.post("/signup", json={"username": username, "password": password, "email": email})
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == username


@pytest.mark.parametrize("username, password ,email", [("username", "password", "email")])
def test_login(test_client: TestClient, setup_database: None, username: Literal['username'], password: Literal['password'], email: Literal['email']):
    response = test_client.post("/signup", json={"username": username, "password": password, "email": email})
    assert response.status_code == 400
    
    response = test_client.post("/login", data={"username": username, "password": password})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

#MOVIES TESTS

def test_get_movies(test_client: TestClient, setup_database: None):
    response = test_client.get("/Movies/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 10


@pytest.mark.parametrize("username, password", [("username", "password")])
def test_create_movie(test_client: TestClient, setup_database: None, username: Literal['username'], password: Literal['password']):
    response = test_client.post("/login", data={"username": username, "password": password})
    assert response.status_code == 200
    token = response.json()["access_token"]

    response = test_client.post("/movies/create", json=movie_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    created_movie = response.json()
    assert created_movie["message"] == "Movie created successfully"
    assert created_movie['data']['title'] == "Test Movie"
    assert isinstance(created_movie['data']["id"], int)


@pytest.mark.parametrize("username, password", [("username", "password")])
def test_get_movie_by_id(test_client: TestClient, setup_database: None, username: Literal['username'], password: Literal['password']):
    response = test_client.post("/login", data={"username": username, "password": password})
    assert response.status_code == 200
    token = response.json()["access_token"]

    response = test_client.post("/movies/create", json=movie_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    created_movie = response.json()
    movie_id = int(created_movie['data'].get("id"))

    response = test_client.get(f"/movie/{movie_id}")
    assert response.status_code == 200
    movie_data_response = response.json()
    assert movie_data_response.get("title") == "Test Movie"


@pytest.mark.parametrize("username, password", [("username", "password")])
def test_update_movie(test_client: TestClient, setup_database: None, username: Literal['username'], password: Literal['password']):
    response = test_client.post("/login", data={"username": username, "password": password})
    assert response.status_code == 200
    token = response.json()["access_token"]

    response = test_client.post("/movies/create", json=movie_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    created_movie = response.json()
    movie_id = int(created_movie['data'].get("id"))

    updated_movie_data_with_id = {
        "movie_id": movie_id,
        "title": "Updated Movie",
        "release_date": "2023-01-01",
        "description": "Updated movie description",
        "duration": 100
    }

    response = test_client.put(f"/movies/{movie_id}", json=updated_movie_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    updated_movie = response.json()
    updated_movie = response.json()
    assert updated_movie["message"] == "Movie Updated successfully"
    assert updated_movie['data']['title'] == "Updated Movie"


@pytest.mark.parametrize("username, password", [("username", "password")])
def test_delete_movie(test_client: TestClient, setup_database: None, username: Literal['username'], password: Literal['password']):
    response = test_client.post("/login", data={"username": username, "password": password})
    assert response.status_code == 200
    token = response.json()["access_token"]

    response = test_client.post("/movies/create", json=movie_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    created_movie = response.json()
    movie_id = int(created_movie['data']["id"])

    response = test_client.delete(f"/movies/{movie_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    deleted_response = response.json()
    assert deleted_response["message"] == "Movie deleted successfully"

#COMMENT TESTS

@pytest.mark.parametrize("username, password", [("username", "password")])
def test_create_comment(test_client: TestClient, setup_database: None, username: Literal['username'], password: Literal['password']):
    response = test_client.post("/login", data={"username": username, "password": password})
    assert response.status_code == 200
    token = response.json()["access_token"]


    response = test_client.post("/movies/create", json=movie_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    created_movie = response.json()
    movie_id = created_movie['data'].get("id")

    response = test_client.post(f"/movies/{movie_id}/create_comment", json=comment_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    created_comment = response.json()
    assert created_comment["message"] == "Comment created successfully"
    assert created_comment['data']['content'] == "Great movie!"


@pytest.mark.parametrize("username, password", [("username", "password")])
def test_get_comments_by_movie_id(test_client: TestClient, setup_database: None, username: Literal['username'], password: Literal['password']):
    response = test_client.post("/login", data={"username": username, "password": password})
    assert response.status_code == 200
    token = response.json()["access_token"]


    response = test_client.post("/movies/create", json=movie_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    created_movie = response.json()
    movie_id = created_movie['data'].get("id")

    response = test_client.post(f"/movies/{movie_id}/create_comment", json=comment_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    created_comment = response.json()
    comment_id = created_comment["data"].get("id")
    assert comment_id is not None

    response = test_client.get(f"/movies/{movie_id}/comments")
    assert response.status_code == 200
    comments = response.json()
    assert isinstance(comments, list)
    assert len(comments) > 0

#NESTED COMMENTS TEST

@pytest.mark.parametrize("username, password", [("username", "password")])
def test_create_nested_comment(test_client: TestClient, setup_database: None, username: Literal['username'], password: Literal['password']):
    response = test_client.post("/login", data={"username": username, "password": password})
    assert response.status_code == 200
    token = response.json()["access_token"]

    response = test_client.post("/movies/create", json=movie_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    created_movie = response.json()
    movie_id = created_movie['data'].get("id")

    response = test_client.post(f"/movies/{movie_id}/create_comment", json=comment_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    created_comment = response.json()
    comment_id = created_comment["data"].get("id")


    response = test_client.post(f"/comments/{comment_id}/comments", json =reply_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    created_reply = response.json()
    assert created_reply["message"] == "Reply created successfully"
    assert created_reply['data']['content'] == "I agree!"


    #RATING TEST


@pytest.mark.parametrize("username, password", [("username", "password")])
def test_create_movie_rating(test_client: TestClient, setup_database: None, username: Literal['username'], password: Literal['password']):
    response = test_client.post("/login", data={"username": username, "password": password})
    assert response.status_code == 200
    token = response.json()["access_token"]

    response = test_client.post("/movies/create", json=movie_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    created_movie = response.json()
    movie_id = created_movie['data'].get("id")

    response = test_client.post(f"/movie/{movie_id}/create_rating", json=rating_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    created_rating = response.json()
    assert created_rating["message"] == "Rating created successfully"
    assert created_rating['data']['rating'] == 5



@pytest.mark.parametrize("username, password", [("username", "password")])
def test_get_movie_rating(test_client: TestClient, setup_database: None, username: Literal['username'], password: Literal['password']):
    response = test_client.post("/login", data={"username": username, "password": password})
    assert response.status_code == 200
    token = response.json()["access_token"]

    response = test_client.post("/movies/create", json=movie_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    created_movie = response.json()
    movie_id = created_movie['data'].get("id")

    response = test_client.get(f"/movie/rating/{movie_id}")
    assert response.status_code == 200
    rating_data_response = response.json()
    assert rating_data_response["message"] ==  "Average rating for movie retrieved successfully"
 
