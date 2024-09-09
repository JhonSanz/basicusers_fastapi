from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database.models import Role, Permission, RolePermissionAssociation
from app.database.connection import engine, Base


def create_role_if_not_exists(session: Session, role_name: str) -> Role:
    role = session.execute(select(Role).filter_by(name=role_name)).scalars().first()
    if not role:
        role = Role(name=role_name)
        session.add(role)
        session.commit()
    return role


def create_permission_if_not_exists(
    session: Session, permission_name: str
) -> Permission:
    permission = (
        session.execute(select(Permission).filter_by(name=permission_name))
        .scalars()
        .first()
    )
    if not permission:
        permission = Permission(name=permission_name)
        session.add(permission)
        session.commit()
    return permission


def seed_roles(session: Session):
    roles = ["superadmin", "admin", "guest"]
    role_objects = {role: create_role_if_not_exists(session, role) for role in roles}
    return role_objects


def seed_permissions(session: Session):
    entities = ["payment", "debt", "role"]
    actions = ["read", "create", "update", "delete"]
    permissions = [
        f"{entity}.can_{action}" for entity in entities for action in actions
    ]
    permission_objects = {
        perm: create_permission_if_not_exists(session, perm) for perm in permissions
    }
    return permission_objects


if __name__ == "__main__":
    with Session(engine) as session:
        seed_roles(session)
        seed_permissions(session)


# def associate_role_permission(session: Session, role: Role, permission: Permission):
#     association_exists = (
#         session.execute(
#             select(RolePermissionAssociation).filter_by(
#                 role_id=role.id, permission_id=permission.id
#             )
#         )
#         .scalars()
#         .first()
#     )

#     if not association_exists:
#         association = RolePermissionAssociation(
#             role_id=role.id, permission_id=permission.id
#         )
#         session.add(association)
#         session.commit()


# def seed_role_permissions(session: Session, role_objects, permission_objects):
#     # Asignar todos los permisos a superadmin
#     for permission in permission_objects.values():
#         associate_role_permission(session, role_objects["superadmin"], permission)

#     # Asignar permisos específicos a admin
#     admin_permissions = ["payment.can_read", "payment.can_create", "debt.can_read"]
#     for perm in admin_permissions:
#         associate_role_permission(
#             session, role_objects["admin"], permission_objects[perm]
#         )

#     # Asignar permisos específicos a guest
#     guest_permissions = ["payment.can_read", "debt.can_read"]
#     for perm in guest_permissions:
#         associate_role_permission(
#             session, role_objects["guest"], permission_objects[perm]
#         )


# def seed_roles_and_permissions(session: Session):
#     role_objects = seed_roles(session)
#     permission_objects = seed_permissions(session)
#     seed_role_permissions(session, role_objects, permission_objects)


# if __name__ == "__main__":
#     Base.metadata.create_all(engine)
#     with Session(engine) as session:
#         seed_roles_and_permissions(session)
