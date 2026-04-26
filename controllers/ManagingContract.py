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
        # if loggedUser is None:
        #     loggedUser = self.user_manager.LoginUser()
        # if loggedUser is None:
        #     print("Authentification échouée.")
        #     return
        # else:
        #     print(f"(Auto Logged in to {loggedUser.email} )")
        #loggedUser = self.user_manager.LoginUser()

        with Session(engine) as session:
            stmt = select(ContractDB)
            for contract in session.scalars(stmt):
                print(str(contract.total_amount) + " / " + str(contract.id))

    """Functions to create user with a password"""

    def CreateContract(self, contract_item: ContractDB):
        #user_manager = ManagingUser()
        #self.user_manager.LoginUser()  # Trigger input() form
        loggedUser = self.user_manager.LoginCheck() #LogFromJWT()
        if loggedUser is None:
            print("Authentification échouée.")
            return
        # if loggedUser is None:
        #     loggedUser = self.user_manager.LoginUser()
        # if loggedUser is None:
        #     print("Authentification échouée.")
        #     return
        # else:
        #     print(f"(Auto Logged in to {loggedUser.email} )")

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
