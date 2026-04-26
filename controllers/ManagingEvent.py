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


        #loggedUser = self.user_manager.LoginUser()
        loggedUser = self.user_manager.LogFromJWT()
        if loggedUser is None:
            loggedUser = self.user_manager.LoginUser()
        if loggedUser is None:
            print("Authentification échouée.")
            return
        else:
            print(f"(Auto Logged in to {loggedUser.email} )")
        if loggedUser is None:
            print("Authentification échouée.")
            return

        with Session(engine) as session:
            stmt = select(EventDB)
            for event in session.scalars(stmt):
                print(str(event.name) + " / " + str(event.id))

    """Functions to create event"""

    def CreateEvent(self, event_item: EventDB):
        #user_manager = ManagingUser()

        loggedUser = self.user_manager.LogFromJWT()
        if loggedUser is None:
            loggedUser = self.user_manager.LoginUser()
        if loggedUser is None:
            print("Authentification échouée.")
            return
        else:
            print(f"(Auto Logged in to {loggedUser.email} )")
        #self.user_manager.LoginUser()  # Trigger input() form

        engine = self.db.LoginDatabase()
        with Session(engine) as session:
            session.add(event_item)
            session.commit()
            # key = "secret"
            # encoded = jwt.encode({"loggedin": "false"}, key, algorithm="HS256")
            # with open("jwt.json", "w") as f:
            #     import json
            #     json.dump({"token": encoded}, f)
            return True
        return False
