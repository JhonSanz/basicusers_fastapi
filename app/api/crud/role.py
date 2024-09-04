from sqlalchemy.orm import Session
from app.database.models import Role


def get_roles(*, db: Session, skip: int = 0, limit: int = 10) -> Role:
    return db.query(Role).offset(skip).limit(limit).all()


def get_role(*, db: Session, role_id: int) -> Role:
    return db.query(Role).filter(Role.id == role_id).first()
