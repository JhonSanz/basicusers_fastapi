from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from app.database.connection import get_db
from app.api.crud import menu as crud_menu
from app.api.schemas.menu import MenuInDBBase
from app.api.schemas.user import UserInDBBase
from app.api.schemas.base import StandardResponse, std_response
from app.api.crud.auth import get_user_with_permission

router = APIRouter()


@router.get(
    "/menu/",
    response_model=StandardResponse[List[MenuInDBBase]],
)
def get_menu_by_user_role(
    db: Session = Depends(get_db),
    current_user: UserInDBBase = Depends(get_user_with_permission("menu.can_read")),
):
    """
    Retrieve menu given user role.
    """
    try:
        menu = crud_menu.get_menu(db=db)
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
        data=menu,
    )
