from fastapi import HTTPException, status



credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Action is not allowed",
        headers={"WWW-Authenticate": "Bearer"},
    )


not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Movie not found"
)


def invalid_rating(value: float):
    if value <= 0 or value > 10:
        error = "Invalid rating"
    return error



def average_rating(ratings):
    average_rating = sum(rating.value for rating in ratings) / len(ratings)
    return average_rating
    


def model_to_dict(model_instance):
    return {c.key: getattr(model_instance, c.key) for c in inspect(model_instance).mapper.column_attrs}

    


