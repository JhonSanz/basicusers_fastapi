from sqlalchemy.orm import Session
from app.api.utils.menu import SUPER_ADMIN, ADMIN, CLIENT

def get_menu(db: Session):
    return SUPER_ADMIN
