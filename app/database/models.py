from sqlalchemy import (
    Integer,
    String,
    Float,
    DateTime,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import relationship, mapped_column, relationship, Mapped
from typing import List
from .connection import Base


class UserPosAssociation(Base):
    __tablename__ = "user_pos"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    pos_id: Mapped[int] = mapped_column(ForeignKey("pos.id"))
    user: Mapped["User"] = relationship("User", back_populates="userasociations")
    pos: Mapped["Pos"] = relationship("Pos", back_populates="posasociations")


class UserRoleAssociation(Base):
    __tablename__ = "user_role_association"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"))

    user: Mapped["User"] = relationship("User", back_populates="user_role_associations")
    role: Mapped["Role"] = relationship("Role", back_populates="user_role_associations")


class RolePermissionAssociation(Base):
    __tablename__ = "permission_role_association"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"))
    permission_id: Mapped[int] = mapped_column(ForeignKey("permission.id"))
    role: Mapped["Role"] = relationship(
        "Role", back_populates="role_permission_associations"
    )
    permission: Mapped["Role"] = relationship(
        "Permission", back_populates="role_permission_associations"
    )


class Pos(Base):
    __tablename__ = "pos"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    rut: Mapped[str] = mapped_column(String(100), unique=True)
    url: Mapped[str] = mapped_column(String(100), nullable=True)
    address: Mapped[str] = mapped_column(String(300))
    posasociations: Mapped[List["UserPosAssociation"]] = relationship(
        "UserPosAssociation", back_populates="pos"
    )


class Role(Base):
    __tablename__ = "role"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    user_role_associations: Mapped[List["UserRoleAssociation"]] = relationship(
        "UserRoleAssociation", back_populates="role"
    )
    role_permission_associations: Mapped[List["RolePermissionAssociation"]] = (
        relationship("RolePermissionAssociation", back_populates="role")
    )


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    identification: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))
    password: Mapped[str] = mapped_column(String(300))
    phone: Mapped[str] = mapped_column(String(300))
    userasociations: Mapped[List["UserPosAssociation"]] = relationship(
        "UserPosAssociation", back_populates="user"
    )
    user_role_associations: Mapped[List["UserRoleAssociation"]] = relationship(
        "UserRoleAssociation", back_populates="user"
    )

    @property
    def roles(self) -> List["Role"]:
        return [association.role for association in self.user_role_associations]


class Permission(Base):
    __tablename__ = "permission"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    role_permission_associations: Mapped[List["RolePermissionAssociation"]] = (
        relationship("RolePermissionAssociation", back_populates="permission")
    )


# class Media(Base):
#     __tablename__ = "media"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     url: Mapped[str] = mapped_column(String(100))


# class CompanyMedia(Base):
#     __tablename__ = "companymedia"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     company_id: Mapped[int] = mapped_column(Integer, ForeignKey("company.id"))
#     company: Mapped["Company"] = relationship("Company", back_populates="companymedia")
#     media_id: Mapped[int] = mapped_column(Integer, ForeignKey("media.id"))
#     media: Mapped["Media"] = relationship("Media", back_populates="companymedia")
