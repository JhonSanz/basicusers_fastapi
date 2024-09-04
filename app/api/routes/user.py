from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app.database.connection import get_db
from app.api.crud import user as crud_user
from app.api.schemas.user import User, UserCreate, UserUpdate, UserBase

router = APIRouter()


@router.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.

    - **user**: UserCreate schema with the details of the new user (shown above).

    Returns the created user.
    """
    return crud_user.create_user(db=db, user=user)


@router.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a user by their ID.

    - **user_id**: ID of the user to retrieve.

    Returns the user with the specified ID, or raises a 404 error if the user is not found.
    """
    db_user = crud_user.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/users/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieve a list of users with pagination.

    - **skip**: Number of users to skip for pagination (default is 0).
    - **limit**: Maximum number of users to return (default is 10).

    Returns a list of users.
    """
    users = crud_user.get_users(db=db, skip=skip, limit=limit)
    return users


@router.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    """
    Update an existing user by their ID.

    - **user_id**: ID of the user to update.
    - **user**: UserUpdate schema with the updated details (shown above).

    Returns the updated user, or raises a 404 error if the user is not found.
    """
    db_user = crud_user.update_user(db=db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/users/{user_id}", response_model=bool)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user by their ID.

    - **user_id**: ID of the user to delete.

    Returns `True` if the user was successfully deleted, or raises a 404 error if the user is not found.
    """
    success = crud_user.delete_user(db=db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return success
