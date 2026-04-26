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

        loggedUser = self.user_manager.LoginCheck()
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

        loggedUser = self.user_manager.LoginCheck()# self.user_manager.LogFromJWT()
        if loggedUser is None:
            print("Authentification échouée.")
            return False
        
        if loggedUser.role.lower() != "commercial":
            print("Seul un commercial peut enregistrer un client.")
            return False
        
        with Session(engine) as session:
            client_item.commercial_id = loggedUser.id
            session.add(client_item)
            session.commit()
            return True
        return False


    def DeleteClient(self, client_id: int):
        engine = self.db.LoginDatabase()
        if engine is None:
            print("Connection échouée.")
            return None

        loggedUser = self.user_manager.LoginCheck() # self.LogFromJWT()
        if loggedUser is None:
            print("Authentification échouée.")
            return 

        with Session(engine) as session:
            clt = session.get(ClientDB, client_id)
            session.delete(clt)
            session.commit()
            return True
        return False