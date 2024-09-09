from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import APIRouter, Depends, HTTPException, status
from app.database.connection import get_db
from app.api.crud import user as crud_user
from app.api.schemas.user import UserCreate, UserUpdate, UserInDBBase
from app.api.schemas.base import StandardResponse, std_response
from app.api.utils.exceptions import (
    RoleNotFoundException,
    UserAlreadyExistsException,
    UserDoesNotExistException,
)
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/users/", response_model=StandardResponse[UserInDBBase])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.

    - **user**: UserCreate schema with the details of the new user (shown above).

    Returns the created user.
    """
    db_user = None
    try:
        db_user = crud_user.create_user(db=db, user=user)
    except RoleNotFoundException as e:
        return std_response(
            status_code=status.HTTP_404_NOT_FOUND, ok=False, msg=str(e), data=None
        )
    except UserAlreadyExistsException as e:
        return std_response(
            status_code=status.HTTP_400_BAD_REQUEST, ok=False, msg=str(e), data=None
        )
    except SQLAlchemyError as e:
        return std_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            ok=False,
            msg=f"Database error, {str(e)}",
            data=None,
        )
    except Exception as e:
        print(e)
        return std_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            ok=False,
            msg=f"An unexpected error occurred",
            data=None,
        )
    return std_response(
        status_code=status.HTTP_201_CREATED,
        ok=True,
        msg="User created successfully.",
        data=db_user,
    )


@router.get("/users/{user_id}", response_model=StandardResponse[UserInDBBase])
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a user by their ID.

    - **user_id**: ID of the user to retrieve.

    Returns the user with the specified ID, or raises a 404 error if the user is not found.
    """
    try:
        db_user = crud_user.get_user(db=db, user_id=user_id)
    except UserDoesNotExistException:
        return std_response(
            status_code=status.HTTP_404_NOT_FOUND,
            ok=False,
            msg="User not found",
            data=None,
        )
    except Exception:
        return std_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            ok=False,
            msg=f"An unexpected error occurred",
            data=None,
        )
    return std_response(
        status_code=status.HTTP_200_OK,
        ok=True,
        msg="",
        data=db_user,
    )


# @router.get("/users/", response_model=List[UserInDBBase])
@router.get("/users/", response_model=StandardResponse[List[UserInDBBase]])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieve a list of users with pagination.

    - **skip**: Number of users to skip for pagination (default is 0).
    - **limit**: Maximum number of users to return (default is 10).

    Returns a list of users.
    """
    try:
        users = crud_user.get_users(db=db, skip=skip, limit=limit)
    except Exception:
        return std_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            ok=False,
            msg=f"An unexpected error occurred",
            data=None,
        )
    return std_response(
        status_code=status.HTTP_200_OK,
        ok=True,
        msg="",
        data=users,
    )


@router.put("/users/{user_id}", response_model=UserInDBBase)
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


@router.delete("/users/{user_id}", response_model=StandardResponse[UserInDBBase])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user by their ID.

    - **user_id**: ID of the user to delete.

    Returns `True` if the user was successfully deleted, or raises a 404 error if the user is not found.
    """
    try:
        crud_user.delete_user(db=db, user_id=user_id)
    except UserDoesNotExistException as e:
        return std_response(
            status_code=status.HTTP_404_NOT_FOUND,
            ok=False,
            msg="User not found",
            data=None,
        )
    except SQLAlchemyError as e:
        return std_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            ok=False,
            msg=f"Database error, {str(e)}",
            data=None,
        )
    except Exception as e:
        print(e)
        return std_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            ok=False,
            msg=f"An unexpected error occurred",
            data=None,
        )
    return std_response(
        status_code=status.HTTP_200_OK,
        ok=True,
        msg="",
        data=None,
    )
