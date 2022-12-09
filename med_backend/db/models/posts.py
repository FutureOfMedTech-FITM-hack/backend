from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from med_backend.db.base import Base
from med_backend.db.models.users import UserScheme


class PostScheme(Base):
    __tablename__ = "posts"

    id: int = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        unique=True,
        index=True,
    )
    name: str = Column(String, nullable=False)
    description: str = Column(String, nullable=True)

    # creator
    user_id: int = Column(Integer, ForeignKey(UserScheme.id), primary_key=True)
    user: UserScheme = relationship("UserScheme", foreign_keys="PostScheme.user_id")
