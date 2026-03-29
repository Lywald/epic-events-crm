from datetime import date, datetime


class Contract:
    """Contrats conçus par Epic Events"""
    def __init__(self, id: int, informations_client: str,
                 commercial_name: str, montant_total: float,
                 montant_restant: float, creation_date: date,
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