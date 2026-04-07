from datetime import datetime

from sqlalchemy import Column, Integer, Float, Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.orm import relationship
from typing import Optional
from .base import Base


# Business Model
class User:
    def __init__(self, id: Optional[int] = None, 
                 email: str = "", password: str = "",
                 name: str  = "Anonymous", 
                 #affiliation: str = "", permissions: str = ""):
                 role: str = "", created_at: DateTime = None):
        self.id = id
        self.email = email
        self.password = password
        #self.employee_number = employee_number
        self.name = name
        #self.affiliation = affiliation
        #self.permissions = permissions
        self.role = role
        self.created_at = created_at

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "password_hash": self.password_hash,
            #"employee_number": self.employee_number,
            "name": self.name,
            #"affiliation": self.affiliation,
            #"permissions": self.permissions
            "created_at": self.created_at,
            "role": self.role
        }
    
    
# SQLAchemy Entity
class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    #employee_number = Column(Integer, nullable=True)
    name = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)    
    #affiliation = Column(String, nullable=False)
    #permissions = Column(String, nullable=False)
    
    @classmethod
    def loadUserDB(cls, usr: User):
        return cls(
            id=usr.id,
            email=usr.email,
            password=usr.password,
            #employee_number=usr.employee_number,
            name=usr.name,
            #affiliation=usr.affiliation,
            #permissions=usr.permissions
            created_at=usr.created_at
        )

