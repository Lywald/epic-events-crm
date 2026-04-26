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

    def ListContracts(self):
        engine = self.db.LoginDatabase()
        
        loggedUser = self.LoginUser()
        if loggedUser is None:
            print("Authentification échouée.")
            return
        
        with Session(engine) as session:
            stmt = select(ContractDB)
            for contract in session.scalars(stmt):
                print(str(contract.total_amount) + " / " + str(contract.id))

    """Functions to create user with a password"""
    def CreateContract(self, contract_item: ContractDB):
        user_manager = ManagingUser()
        user_manager.LoginUser() # Trigger input() form

        engine = self.db.LoginDatabase()
        with Session(engine) as session:
            session.add(contract_item)
            session.commit()
            # key = "secret"
            # encoded = jwt.encode({"loggedin": "false"}, key, algorithm="HS256")
            # with open("jwt.json", "w") as f:
            #     import json
            #     json.dump({"token": encoded}, f)
            return True
        return False