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
    user: Mapped["User"] = relationship("User", back_populates="posasociations")
    pos: Mapped["Pos"] = relationship("Pos", back_populates="userasociations")


class Pos(Base):
    __tablename__ = "pos"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    rut: Mapped[str] = mapped_column(String(100), unique=True)
    url: Mapped[str] = mapped_column(String(100), nullable=True)
    address: Mapped[str] = mapped_column(String(300))
    userasociations: Mapped[List["UserPosAssociation"]] = relationship(
        "UserPosAssociation", back_populates="pos"
    )


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    identification: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))
    password: Mapped[str] = mapped_column(String(300))
    phone: Mapped[str] = mapped_column(String(300))
    posasociations: Mapped[List["UserPosAssociation"]] = relationship(
        "UserPosAssociation", back_populates="user"
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
