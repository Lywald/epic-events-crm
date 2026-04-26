from controllers.ManagingUser import ManagingUser
from models.user import UserDB
from models.contract import ContractDB
from models.client import ClientDB
from database.database import Database
from sqlalchemy import select
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import jwt
import os


class ManagingClient:
    ###Functions to manage contracts

    def __init__(self):
        self.db = Database()
        self.user_manager = ManagingUser()

    def ListClients(self):
        engine = self.db.LoginDatabase()

        loggedUser = self.user_manager.LogFromJWT()
        if loggedUser is None:
            loggedUser = self.user_manager.LoginUser()
        if loggedUser is None:
            print("Authentification échouée.")
            return
        else:
            print(f"(Auto Logged in to {loggedUser.email} )")
        #loggedUser = self.user_manager.LoginUser()
        if loggedUser is None:
            print("Authentification échouée.")
            return

        with Session(engine) as session:
            stmt = select(ClientDB)
            for client in session.scalars(stmt):
                print(str(client.full_name) + " / " + str(client.email))

    """Functions to create user with a password"""

    def CreateClient(self, client_item: ClientDB):
        engine = self.db.LoginDatabase()

        loggedUser = self.user_manager.LogFromJWT()
        if loggedUser is None:
            loggedUser = self.user_manager.LoginUser()
        if loggedUser is None:
            print("Authentification échouée.")
            return
        else:
            print(f"(Auto Logged in to {loggedUser.email} )")
        #loggedUser = self.user_manager.LoginUser()
        if loggedUser is None:
            print("Authentification échouée.")
            return False
        
        with Session(engine) as session:
            session.add(client_item)
            session.commit()
            # key = "secret"
            # encoded = jwt.encode({"loggedin": "false"}, key, algorithm="HS256")
            # with open("jwt.json", "w") as f:
            #     import json
            #     json.dump({"token": encoded}, f)
            return True
        return False
