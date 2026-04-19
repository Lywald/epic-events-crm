from models.user import UserDB
from models.contract import ContractDB
from controllers.ManagingUser import LoginUser
from database.database import Database
from sqlalchemy import select
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import jwt
import os

class ManagingContract:
    ###Functions to manage contracts

    def __init__(self):
        self.db = Database()

    def ListContracts(self):
        admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
        engine = self.db.LoginDatabase(email="admin@epicevents.com", password=admin_password)
        with Session(engine) as session:
            stmt = select(ContractDB)
            for contract in session.scalars(stmt):
                print(str(contract.total_amount) + " / " + str(contract.id))

    """Functions to create user with a password"""
    def CreateContract(self, contract_item: ContractDB):
        # Use admin password from .env for DB operations (dummy for SQLite)
        LoginUser(None, None) # Trigger input() form
        admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
        engine = self.db.LoginDatabase(email="admin@epicevents.com", password=admin_password)
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