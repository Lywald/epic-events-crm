from controllers.ManagingUser import ManagingUser
from models.user import UserDB
from models.contract import ContractDB
from controllers.ManagingUser import ManagingUser
from database.database import Database
from sqlalchemy import select
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import jwt
import os


class ManagingContract:
    """Controller for contract CRUD operations."""

    def __init__(self):
        self.db = Database()
        self.user_manager = ManagingUser()

    def ListContracts(self):
        engine = self.db.LoginDatabase()

        loggedUser = self.user_manager.LoginCheck() #LogFromJWT()
        if loggedUser is None:
            print("Authentification échouée.")
            return

        with Session(engine) as session:
            stmt = select(ContractDB)
            for contract in session.scalars(stmt):
                print(str(contract.total_amount) + " / " + str(contract.id))

    """Functions to create user with a password"""

    def CreateContract(self, contract_item: ContractDB):
        loggedUser = self.user_manager.LoginCheck() #LogFromJWT()
        if loggedUser is None:
            print("Authentification échouée.")
            return

        engine = self.db.LoginDatabase()
        with Session(engine) as session:
            session.add(contract_item)
            session.commit()
            return True
        return False

    def DeleteContract(self, contract_id: int):
        engine = self.db.LoginDatabase()
        if engine is None:
            print("Connection échouée.")
            return None

        loggedUser = self.user_manager.LoginCheck() # self.LogFromJWT()
        if loggedUser is None:
            print("Authentification échouée.")
            return 

        with Session(engine) as session:
            ctr = session.get(ContractDB, contract_id)
            session.delete(ctr)
            session.commit()
            return True
        return False