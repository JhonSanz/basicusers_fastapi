from sqlalchemy.orm import Session
from app.database.models import Role
from app.api.schemas.role import RoleInDBBase
from app.api.schemas.user import UserInDBBase
from app.api.utils.exceptions import RoleNotFoundException
from app.api.utils.decorators import validate_res_model_pydantic
from pydantic_core import ValidationError



@validate_res_model_pydantic(RoleInDBBase)
def get_roles(*, db: Session, skip: int = 0, limit: int = 10) -> RoleInDBBase:
    result = db.query(Role).offset(skip).limit(limit).all()
    if result is None:
        raise RoleNotFoundException("Role does not exist")

    return result


@validate_res_model_pydantic(RoleInDBBase)
def get_role(*, db: Session, role_id: int) -> RoleInDBBase:
    result = db.query(Role).filter(Role.id == role_id).first()
    if result is None:
        raise RoleNotFoundException("Role does not exist")

    return result

