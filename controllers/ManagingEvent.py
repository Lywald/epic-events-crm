from controllers.ManagingUser import ManagingUser
from models.user import UserDB
from models.contract import ContractDB
from models.event import EventDB
from controllers.ManagingUser import ManagingUser
from database.database import Database
from sqlalchemy import select
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import jwt
import os


class ManagingEvent:
    ###Functions to manage events

    def __init__(self):
        self.db = Database()
        self.user_manager = ManagingUser()

    def ListEvents(self):
        engine = self.db.LoginDatabase()

        loggedUser = self.user_manager.LoginCheck() #.LogFromJWT()
        if loggedUser is None:
            print("Authentification échouée.")
            return

        with Session(engine) as session:
            stmt = select(EventDB)
            for event in session.scalars(stmt):
                print(str(event.name) + " / " + str(event.id))

    """Functions to create event"""

    def CreateEvent(self, event_item: EventDB):
        loggedUser = self.user_manager.LoginCheck() #.LogFromJWT()
        if loggedUser is None:
            print("Authentification échouée.")
            return
        
        engine = self.db.LoginDatabase()
        with Session(engine) as session:
            session.add(event_item)
            session.commit()
            return True
        return False


    def DeleteEvent(self, event_id: int):
        engine = self.db.LoginDatabase()
        if engine is None:
            print("Connection échouée.")
            return None

        loggedUser = self.user_manager.LoginCheck() 
        if loggedUser is None:
            print("Authentification échouée.")
            return 

        with Session(engine) as session:
            evt = session.get(EventDB, event_id)
            session.delete(evt)
            session.commit()
            return True
        return False


    def AddSupport(self, user_id: int, event_id: int):
        engine = self.db.LoginDatabase()
        if engine is None:
            print("Connection échouée.")
            return False

        loggedUser = self.user_manager.LoginCheck() 
        if loggedUser is None:
            print("Authentification échouée.")
            return False
        
        if loggedUser.role.lower() != "gestion":
            print("Seul un membre de gestion peut assigner un support à l'évènement.")
            return False
        
        with Session(engine) as session:
            evt = session.get(EventDB, event_id)
            
            if evt is None:
                return False
            
            support_user = session.get(UserDB, user_id)
            if support_user is None:
                return False
            
            if support_user.role.lower() != "support":
                return False
            
            evt.support_contact_id = support_user.id
            session.commit()
            return True


#    def CreateEvent