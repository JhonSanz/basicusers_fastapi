from sqlalchemy.orm import Session
from app.api.utils.menu import SUPER_ADMIN_MENU, ADMIN_MENU, CLIENT_MENU
from app.api.utils.auth import SUPERADMIN, ADMIN, GUEST
from app.database.models import User


def get_menu(db: Session, current_user: User):
    roles_names = [role.name for role in current_user.roles]
    if SUPERADMIN in roles_names:
        return SUPER_ADMIN_MENU
    if ADMIN in roles_names:
        return ADMIN_MENU
    if GUEST in roles_names:
        return CLIENT_MENU
    return []