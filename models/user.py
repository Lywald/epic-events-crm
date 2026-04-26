from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    String,
    func,
)
from sqlalchemy.orm import relationship
from typing import Optional
from .base import Base


# SQLAchemy Entity
class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    name = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    role = Column(String(50), default="user")

    def __init__(
        self,
        id: Optional[int] = None,
        email: str = "",
        password: str = "",
        name: str = "Anonymous",
        # affiliation: str = "", permissions: str = ""):
        role: str = "",
        created_at: DateTime = None,
    ):
        self.id = id
        self.email = email
        self.password = password
        self.name = name
        self.role = role
        self.created_at = created_at
