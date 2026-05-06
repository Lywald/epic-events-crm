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

        loggedUser = self.user_manager.LoginCheck()  # self.user_manager.LogFromJWT()
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

    def UpdateClient(self, client_item: ClientDB):
        engine = self.db.LoginDatabase()
        if engine is None:
            print("Connection échouée.")
            return None
    
        loggedUser = self.user_manager.LoginCheck()
        if loggedUser is None:
            print("Authentification échouée.")
            return None
    
        if loggedUser.role.lower() != "commercial":
            print("Seul un commercial peut modifier un client.")
            return None
    
        if getattr(client_item, "id", None) is None:
            print("ID client manquant.")
            return None
    
        with Session(engine) as session:
            clt = session.get(ClientDB, int(client_item.id))
            if clt is None:
                print("Client introuvable.")
                return None
    
            # Optional ownership check:
            if clt.commercial_id != loggedUser.id:
                print("Vous ne pouvez modifier que vos propres clients.")
                return None
    
            clt.full_name = client_item.full_name
            clt.email = client_item.email
            clt.phone = client_item.phone
            clt.company_name = client_item.company_name
            clt.updated_at = func.now()
            clt.commercial_id = loggedUser.id
    
            session.commit()
            return True
        return False

    def DeleteClient(self, client_id: int):
        engine = self.db.LoginDatabase()
        if engine is None:
            print("Connection échouée.")
            return None

        loggedUser = self.user_manager.LoginCheck()  # self.LogFromJWT()
        if loggedUser is None:
            print("Authentification échouée.")
            return None

        if loggedUser.role.lower() != "commercial":
            print("Seul un commercial peut supprimer un client.")
            return None

        with Session(engine) as session:
            clt = session.get(ClientDB, client_id)
            if clt.commercial_id != loggedUser.id:
                print("Vous ne pouvez supprimer que vos propres clients.")
                return None
            session.delete(clt)
            session.commit()
            return True
        return False
