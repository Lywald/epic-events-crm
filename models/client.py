from datetime import datetime, date

from sqlalchemy import Column, Integer, Float, Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.orm import relationship
from typing import Optional
from .base import Base

class ClientDB(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=True)
    company_name = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)    
    updated_at = Column(DateTime, server_default=func.now(), nullable=False)    
    commercial_id = Column(Integer, nullable=True)

    """Clients de Epic Events"""
    def __init__(self, full_name: str, email: str, 
                 phone: str, company_name: str,
                 created_at: date, updated_at: date,
                 commercial_id: Integer):
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.company_name = company_name
        if isinstance(created_at, str):
            self.created_at = datetime.strptime(created_at, "%Y-%m-%d").date()
        else:
            self.created_at = created_at
        if isinstance(updated_at, str):
            self.updated_at = datetime.strptime(updated_at, "%Y-%m-%d").date()
        else:
            self.updated_at = updated_at
        self.commercial_id = commercial_id

    