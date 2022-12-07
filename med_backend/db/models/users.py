from pydantic import EmailStr
from sqlalchemy import Boolean, Column, Integer, String

from med_backend.db.base import Base


class UserScheme(Base):
    """Class to store base info about users"""

    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True)
    username: str = Column(String, unique=True, index=True)
    email: EmailStr = Column(String, unique=True, index=True)
    fullname: str = Column(String)
    hashed_password: str = Column(String)
    disabled: bool = Column(Boolean, default=False)
