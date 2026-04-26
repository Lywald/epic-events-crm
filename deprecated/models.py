"""
Epic Events CRM — SQLAlchemy models + DB initialisation
Run:  python models.py
Creates epiceventsDB.db with all tables and one seed gestion user.
"""

from datetime import datetime
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    Text,
    ForeignKey,
    Enum,
)
from sqlalchemy.orm import declarative_base, relationship, Session
import bcrypt
import enum

DATABASE_URL = "sqlite:///epiceventsDB.db"
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()


class RoleEnum(str, enum.Enum):
    gestion = "gestion"
    commercial = "commercial"
    support = "support"


class User(Base):
    """Collaborateur Epic Events."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String(255), nullable=False)  # bcrypt hash
    role = Column(Enum(RoleEnum), nullable=False)

    # Relations
    clients = relationship(
        "Client", back_populates="commercial", foreign_keys="Client.commercial_id"
    )
    contracts = relationship(
        "Contract", back_populates="commercial", foreign_keys="Contract.commercial_id"
    )
    events = relationship(
        "Event",
        back_populates="support_contact",
        foreign_keys="Event.support_contact_id",
    )

    def set_password(self, plain: str) -> None:
        self.password = bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()

    def check_password(self, plain: str) -> bool:
        return bcrypt.checkpw(plain.encode(), self.password.encode())

    def __repr__(self):
        return f"<User {self.email} [{self.role}]>"


class Client(Base):
    """Client d'Epic Events."""

    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    phone = Column(String(30))
    company_name = Column(String(150))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Commercial responsable (département commercial)
    commercial_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    commercial = relationship(
        "User", back_populates="clients", foreign_keys=[commercial_id]
    )

    contracts = relationship("Contract", back_populates="client")

    def __repr__(self):
        return f"<Client {self.full_name}>"


class Contract(Base):
    """Contrat entre Epic Events et un client."""

    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True)
    total_amount = Column(Float, nullable=False)
    remaining_amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_signed = Column(Boolean, default=False, nullable=False)

    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    client = relationship("Client", back_populates="contracts")

    # Commercial associé au client au moment du contrat
    commercial_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    commercial = relationship(
        "User", back_populates="contracts", foreign_keys=[commercial_id]
    )

    event = relationship("Event", back_populates="contract", uselist=False)

    def __repr__(self):
        return f"<Contract #{self.id} signed={self.is_signed}>"


class Event(Base):
    """Événement organisé pour un client."""

    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    location = Column(String(300))
    attendees = Column(Integer, default=0)
    notes = Column(Text)

    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    contract = relationship("Contract", back_populates="event")

    # Membre du département support responsable
    support_contact_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    support_contact = relationship(
        "User", back_populates="events", foreign_keys=[support_contact_id]
    )

    def __repr__(self):
        return f"<Event '{self.name}' {self.start_date:%Y-%m-%d}>"


def init_db():
    """Crée toutes les tables et insère un utilisateur gestion de démarrage."""
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        if session.query(User).filter_by(email="admin@epicevents.com").first():
            print("DB déjà initialisée — aucun seed nécessaire.")
            return

        admin = User(
            name="Admin Gestion",
            email="admin@epicevents.com",
            role=RoleEnum.gestion,
        )
        admin.set_password("ChangeMe123!")
        session.add(admin)
        session.commit()
        print(f"Utilisateur seed créé : {admin.email}  (rôle: {admin.role})")
        print("IMPORTANT : changez le mot de passe après la première connexion.")


if __name__ == "__main__":
    init_db()
