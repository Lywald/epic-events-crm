from datetime import date, datetime


class Event:
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

    def to_dict(self):
        return {
            "id": self.id,
            "contract_id": self.contract_id,
            "client_name": self.client_name,
            "client_contact": self.client_contact,
            "event_date_start": self.event_date_start,
            "event_date_end": self.event_date_end,
            "support_contact": self.support_contact,
            "location": self.location,
            "attendees": self.attendees,
            "notes": self.notes,
        }