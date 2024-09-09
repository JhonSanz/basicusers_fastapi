from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from app.database.connection import get_db
from app.api.crud import role as crud_roles
from app.api.schemas.role import RoleInDBBase
from app.api.schemas.base import StandardResponse, std_response

router = APIRouter()


@router.get("/roles/", response_model=StandardResponse[List[RoleInDBBase]])
def read_roles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieve a list of roles with pagination.

    - **skip**: Number of roles to skip for pagination (default is 0).
    - **limit**: Maximum number of roles to return (default is 10).

    Returns a list of roles.
    """
    try:
        roles = crud_roles.get_roles(db=db, skip=skip, limit=limit)
    except Exception as e:
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
        data=roles,
    )