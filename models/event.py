from datetime import datetime, date

from sqlalchemy import Column, Integer, Float, Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.orm import relationship
from typing import Optional
from .base import Base


class EventDB(Base):
    """Evenements organisés par Epic Events"""
    __tablename__ = "events"    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    client_name = Column(String, nullable=False)
    client_contact = Column(String, nullable=True)
    event_date_start = Column(DateTime, server_default=func.now(), nullable=False)    
    event_date_end = Column(DateTime, server_default=func.now(), nullable=False)
    support_contact_id = Column(String, ForeignKey("users.id"), nullable=True)
    location = Column(String, nullable=False)
    attendees = Column(Integer, nullable=True)
    notes = Column(String, nullable=True)

    def __init__(self, id: int, name: str, contract_id: int, 
                 client_name: str, client_contact: str,
                 event_date_start: date, event_date_end: date,
                 support_contact: str, location: str,
                 attendees: int, notes: str):
        self.id = id
        self.name = name
        self.contract_id = contract_id
        self.client_name = client_name
        self.client_contact = client_contact
        if isinstance(event_date_start, str):
            self.event_date_start = datetime.strptime(event_date_start, "%Y-%m-%d").date()
        else:
            self.event_date_start = event_date_start
        if isinstance(event_date_end, str):
            self.event_date_end = datetime.strptime(event_date_end, "%Y-%m-%d").date()
        else:
            self.event_date_end = event_date_end
        self.support_contact = support_contact
        self.location = location
        self.attendees = attendees
        self.notes = notes

    