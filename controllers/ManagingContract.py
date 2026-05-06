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

    def ListContracts(self, filter_mode: str = ""):
        engine = self.db.LoginDatabase()

        loggedUser = self.user_manager.LoginCheck()  # LogFromJWT()
        if loggedUser is None:
            print("Authentification échouée.")
            return

        with Session(engine) as session:
            stmt = select(ContractDB)
            for contract in session.scalars(stmt):
                if filter_mode == "unpaid":
                    if contract.remaining_amount > 0:
                        print(
                            str(contract.total_amount)
                            + " / "
                            + str(contract.id)
                            + "  / signed"
                            if contract.is_signed
                            else "  / unsigned"
                        )
                elif filter_mode == "unsigned":
                    if contract.is_signed == False:
                        print(
                            str(contract.total_amount)
                            + " / "
                            + str(contract.id)
                            + "  / signed"
                            if contract.is_signed
                            else "  / unsigned"
                        )
                else:
                    print(
                        str(contract.total_amount)
                        + " / "
                        + str(contract.id)
                        + "  / signed"
                        if contract.is_signed
                        else "  / unsigned"
                    )

    """Functions to create user with a password"""

    def CreateContract(self, contract_item: ContractDB):
        loggedUser = self.user_manager.LoginCheck()  # LogFromJWT()
        if loggedUser is None:
            print("Authentification échouée.")
            return

        engine = self.db.LoginDatabase()
        with Session(engine) as session:
            session.add(contract_item)
            session.commit()
            return True
        return False

        def UpdateContract(self, contract_item: ContractDB):
            engine = self.db.LoginDatabase()
            if engine is None:
                print("Connection échouée.")
                return None
        
            loggedUser = self.user_manager.LoginCheck()
            if loggedUser is None:
                print("Authentification échouée.")
                return None
        
            if loggedUser.role.lower() != "gestion":
                print("Seul le département gestion peut modifier un contrat.")
                return None
        
            if contract_item.id is None:
                print("ID contrat manquant.")
                return None
        
            with Session(engine) as session:
                ctr = session.get(ContractDB, int(contract_item.id))
                if ctr is None:
                    print("Contrat introuvable.")
                    return None
        
                ctr.client_id = int(contract_item.client_id)
                ctr.commercial_id = int(contract_item.commercial_id)
                ctr.total_amount = float(contract_item.total_amount)
                ctr.remaining_amount = float(contract_item.remaining_amount)
                ctr.is_signed = bool(contract_item.is_signed)
        
                session.commit()
                return True
            return False

    def DeleteContract(self, contract_id: int):
        engine = self.db.LoginDatabase()
        if engine is None:
            print("Connection échouée.")
            return None

        loggedUser = self.user_manager.LoginCheck()  # self.LogFromJWT()
        if loggedUser is None:
            print("Authentification échouée.")
            return

        with Session(engine) as session:
            ctr = session.get(ContractDB, contract_id)
            session.delete(ctr)
            session.commit()
            return True
        return False
