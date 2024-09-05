from typing import List
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from app.api.schemas.user import UserCreate, UserUpdate, UserInDBBase
from app.api.schemas.role import RoleInDBBase
from app.database.models import User, UserRoleAssociation, Role, UserPosAssociation
from app.api.utils.auth import get_password_hash
from app.api.crud.role import get_role


def get_user_by_identification(*, db: Session, identification: str) -> User:
    return db.query(User).filter(User.identification == identification).first()


def create_user(*, db: Session, user: UserCreate) -> User:
    try:
        if not get_role(db=db, role_id=user.role_id):
            raise HTTPException(
                status_code=400, detail=f"Role {user.role_id} not found"
            )

        user_exists = get_user_by_identification(
            db=db, identification=user.identification
        )
        if user_exists:
            raise HTTPException(
                status_code=400, detail="Identification already registered"
            )

        hashed_password = get_password_hash(password=user.password)
        db_user = User(
            identification=user.identification,
            name=user.name,
            password=hashed_password,
            phone=user.phone,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        user_role_association = UserRoleAssociation(
            user_id=db_user.id,
            role_id=user.role_id,
        )
        db.add(user_role_association)
        db.commit()
        db.refresh(db_user)

        return db_user
    except SQLAlchemyError as e:
        db.rollback()
        raise e


def get_user(*, db: Session, user_id: int) -> UserInDBBase:
    result = (
        db.query(User)
        .filter(User.id == user_id)
        .options(
            selectinload(User.user_role_associations).selectinload(
                UserRoleAssociation.role
            )
        )
        .first()
    )
    return result


def get_users(*, db: Session, skip: int = 0, limit: int = 10) -> List[UserInDBBase]:
    return db.query(User).offset(skip).limit(limit).all()


# def update_user(*, db: Session, user_id: int, user: UserUpdate) -> User:
#     try:
#         db_user = db.query(User).filter(User.id == user_id).first()
#         if db_user is None:
#             return None
#         if user.password:
#             user.password = get_password_hash(user.password)
#         for key, value in user.model_dump(exclude_unset=True).items():
#             setattr(db_user, key, value)
#         db.commit()
#         db.refresh(db_user)
#         return db_user
#     except SQLAlchemyError as e:
#         db.rollback()
#         raise e


def delete_user(*, db: Session, user_id: int) -> bool:
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user is None:
            return False

        db.query(UserPosAssociation).filter(
            UserPosAssociation.user_id == user_id
        ).delete()
        db.query(UserRoleAssociation).filter(
            UserRoleAssociation.user_id == user_id
        ).delete()

        db.delete(db_user)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        raise e
