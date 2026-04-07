from sqlalchemy.orm import Session
from models.user import User, UserDB
from database.database import Database


class ManagingUser:
    ###Functions to manage users
    
    def __init__(self):
        self.db = Database()

    """Functions to create user with a password"""
    def CreateUser(self, user_item: UserDB):
        engine = self.db.LoginDatabase(username="Admin", password="admin123")
        with Session(engine) as session:
            session.add(user_item)
            session.commit()
            return True
        return False

    def DeleteUser(self, user_id: int):
        engine = self.db.LoginDatabase(username="Admin", password="admin123")
        with Session(engine) as session:
            usr = session.get(UserDB, 4)
            session.delete(usr)
            session.commit()
            return True
        return False

    def LoginUser(self, email, password_hash):
        """Login if the password_hash is the same than in db"""
        return 
