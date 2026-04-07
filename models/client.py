from datetime import date, datetime


class Client:
    """Clients de Epic Events"""
    def __init__(self, full_name: str, email: str, 
                 telephone: str, enterprise: str,
                 creation_date: date, last_contact: date,
                 commercial_name: str):
        self.full_name = full_name
        self.email = email
        self.telephone = telephone
        self.enterprise = enterprise
        if isinstance(creation_date, str):
            self.creation_date = datetime.strptime(creation_date, "%Y-%m-%d").date()
        else:
            self.creation_date = creation_date
        self.last_contact = last_contact
        self.commercial_name = commercial_name

    def to_dict(self):
        """Convert client info to a dictionary."""
        return {
            "full_name": self.full_name,
            "email": self.email,
            "telephone": self.telephone,
            "enteprise": self.enterprise,
            "creation_date": self.creation_date.isoformat(),
            "last_contact": self.last_contact.isoformat(),
            "commercial_name": self.commercial_name,
        }