from datetime import datetime

from sqlalchemy import Column, Date, Integer, Float, Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.orm import relationship
from typing import Optional
from .base import Base

'''
# Business Model
class Contract:
    """Contrats conçus par Epic Events"""
    def __init__(self, id: int, informations_client: str,
                 commercial_name: str, montant_total: float,
                 montant_restant: float, creation_date: DateTime,
                 signed: bool):
        self.id = id
        self.informations_client = informations_client
        self.commercial_name = commercial_name
        self.montant_total = montant_total
        self.montant_restant = montant_restant
        self.creation_date = creation_date
        if isinstance(creation_date, str):
            self.creation_date = datetime.strptime(creation_date, "%Y-%m-%d").date()
        else:
            self.creation_date = creation_date
        self.signed = signed

    def to_dict(self):
        """Convert contract info to a dictionary."""
        return {
            "id": self.id,
            "informations_client": self.informations_client,
            "commercial_name": self.commercial_name,
            "montant_total": self.montant_total,
            "montant_restant": self.montant_restant,
            "creation_date": self.creation_date,
            "signed": self.signed
        }
    '''

# SQLAlchemy Entity
class ContractDB(Base):  # Base from .base or declarative_base()
    __tablename__ = "contracts"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    #informations_client = Column(String, nullable=False)
    commercial_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    total_amount = Column(Float, nullable=False)
    remaining_amount = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)    
    is_signed = Column(Boolean, default=False)
    
    def __init__(self, id: int, client_id: int,#informations_client: str,
                 commercial_id: str, total_amount: float,
                 remaining_amount: float, created_at: DateTime,
                 is_signed: bool):
        self.id = id
        self.client_id = client_id
        #self.informations_client = informations_client
        self.commercial_id = commercial_id
        self.remaining_amount = remaining_amount
        self.total_amount = total_amount
        self.created_at = created_at
        if isinstance(created_at, str):
            self.created_at = datetime.strptime(created_at, "%Y-%m-%d").date()
        else:
            self.created_at = created_at
        self.is_signed = is_signed

    ''' @classmethod
    def loadContractDB(cls, contract: Contract):
        """Equivalent to UserDB.loadUserDB()"""
        return cls(
            id=contract.id,
            #informations_client=contract.informations_client,
            commercial_id=contract.commercial_id,
            remaining_amount=contract.remaining_amount,
            total_amount=contract.total_amount,
            created_at=contract.created_at,
            is_signed=contract.is_signed
        ) """'''