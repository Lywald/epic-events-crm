from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models.user import UserDB

class Database:
    def __init__(self):
        self.engine = None
        self.loggedin = False
        return
    
    def LoginDatabase(self, username: str, password: str):
        self.loggedin = True
        if self.engine is None:
            self.engine = create_engine("sqlite:///epiceventsDB.db", echo=True)
        return self.engine
    
    def RequestDatabase(request: str):
        """Protéger les requètes contre injection SQL"""
        return
