from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from models.user import UserDB
from models.contract import ContractDB
from models.event import EventDB
from models.client import ClientDB
import bcrypt
import sys
import os
from dotenv import load_dotenv

load_dotenv()

def create_user(session, name, email, password, role='admin'):
    """Create a new user with hashed password."""
    # bcrypt.hashpw returns bytes, we store as string
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    user = UserDB(name=name, email=email, password=hashed, role=role)
    session.add(user)
    session.commit()
    print(f"✅ User '{name}' ({role}) created successfully with email: {email}")

#if __name__ == "__main__":
def db_create_admin():
    db_path = "epiceventsDB.db"
    engine = create_engine(f"sqlite:///{db_path}", echo=False)
    
    # Create tables
    Base.metadata.create_all(engine)
    print(f"✅ Database tables created/verified in {db_path}")
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Load admin credentials from .env (set once and done)
        admin_email = os.getenv("ADMIN_EMAIL", "admin@epicevents.com")
        admin_password = os.getenv("ADMIN_PASSWORD")
        if not admin_password:
            print("❌ Error: ADMIN_PASSWORD must be set in .env file")
            sys.exit(1)
        
        # Create first admin user using env vars
        # create_user() handles hashing internally
        create_user(
            session=session,
            name="Admin",
            email=admin_email,
            password=admin_password,
            role="admin"
        )
        
        # You can add more users here
        # create_user(session, "John Doe", "john@example.com", "password123")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    finally:
        session.close()
    
    print("🎉 First user setup completed!")
