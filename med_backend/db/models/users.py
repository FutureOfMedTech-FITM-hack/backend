from pydantic import EmailStr
from sqlalchemy import Boolean, Column, Integer, String

from med_backend.db.base import Base


class UserScheme(Base):
    """Class to store base info about users"""

    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True)
    username: str = Column(String, unique=True, index=True, nullable=False)
    email: EmailStr = Column(String, unique=True, index=True, nullable=False)
    fullname: str = Column(String, default="")
    hashed_password: str = Column(String)
    gender: str = Column(String, default="Не выбран")
    age: int = Column(Integer, default=0)
    latest_form_result: str = Column(String, default="ok")

    is_manager: bool = Column(Boolean, default=False)
    disabled: bool = Column(Boolean, default=False)
