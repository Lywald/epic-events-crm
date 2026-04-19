from datetime import datetime, date

from sqlalchemy import Column, Integer, Float, Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.orm import relationship
from typing import Optional
from .base import Base


class EventDB(Base):
    """Evenements organisés par Epic Events"""
    def __init__(self, id: int, contract_id: int, 
                 client_name: str, client_contact: str,
                 event_date_start: date, event_date_end: date,
                 support_contact: str, location: str,
                 attendees: int, notes: str):
        self.id = id
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

    