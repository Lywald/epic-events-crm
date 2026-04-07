from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import bcrypt
import sys

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(50), default='user')

def create_user(session, name, email, password, role='admin'):
    """Create a new user with hashed password."""
    # bcrypt.hashpw returns bytes, we store as string
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    user = User(name=name, email=email, password=hashed, role=role)
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
        # Create first admin user (change these values as needed)
        create_user(
            session=session,
            name="Admin",
            email="admin@epicevents.com",
            password="admin123",
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
