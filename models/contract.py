from datetime import datetime

from sqlalchemy import (
    Column,
    Date,
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


# SQLAlchemy Entity
class ContractDB(Base):  # Base from .base or declarative_base()
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    commercial_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    total_amount = Column(Float, nullable=False)
    remaining_amount = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    is_signed = Column(Boolean, default=False)

    def __init__(
        self,
        id: int,
        client_id: int,  # informations_client: str,
        commercial_id: str,
        total_amount: float,
        remaining_amount: float,
        created_at: DateTime,
        is_signed: bool,
    ):
        self.id = id
        self.client_id = client_id
        # self.informations_client = informations_client
        self.commercial_id = commercial_id
        self.remaining_amount = remaining_amount
        self.total_amount = total_amount
        self.created_at = created_at
        if isinstance(created_at, str):
            self.created_at = datetime.strptime(created_at, "%Y-%m-%d").date()
        else:
            self.created_at = created_at
        self.is_signed = is_signed
