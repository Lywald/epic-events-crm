from sqlalchemy import select
from sqlalchemy.orm import Session
import os
import jwt
import datetime
import bcrypt
from dotenv import load_dotenv
from models.user import UserDB
from database.database import Database

load_dotenv()


class ManagingUser:
    ###Functions to manage users

    def __init__(self):
        self.db = Database()

    """Functions to create user with a password"""

    def CreateUser(self, user_item: UserDB):
        engine = self.db.LoginDatabase()
        if engine is None:
            print("Connection échouée.")
            return None

        loggedUser = self.LoginUser()
        if loggedUser is None or loggedUser.role.lower() != "gestion":
            print("Authentification échouée.")
            return None

        with Session(engine) as session:
            session.add(user_item)
            session.commit()
            # key = "secret"
            # encoded = jwt.encode({"loggedin": "false"}, key, algorithm="HS256")
            # with open("jwt.json", "w") as f:
            #     import json
            #     json.dump({"token": encoded}, f)
            return True
        return False

    def DeleteUser(self, user_id: int):
        engine = self.db.LoginDatabase()
        if engine is None:
            print("Connection échouée.")
            return None

        loggedUser = self.LoginUser()
        if loggedUser is None or loggedUser.role.lower() != "gestion":
            print("Authentification échouée.")
            return None

        with Session(engine) as session:
            usr = session.get(UserDB, user_id)
            session.delete(usr)
            session.commit()
            return True
        return False

    def LoginUser(self, email=None, password_hash=None):
        """Login if the password_hash is the same than in db"""
        engine = self.db.LoginDatabase()
        if engine is None:
            return None

        if email == "" or password_hash == "" or email == None or password_hash == None:
            print("Login email: ")
            email = input()
            print("Login password: ")
            user_password = input()
            # salt = bcrypt.gensalt()
            # hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), salt).decode('utf-8')
            # password_hash = hashed_password

        with Session(engine) as session:
            stmt = select(UserDB).where(UserDB.email == email)
            user = session.scalar(stmt)
            # session.commit()
            # key = "secret"
            if not user:
                return None

            if bcrypt.checkpw(
                user_password.encode("utf-8"), user.password.encode("utf-8")
            ):
                print("Correct password")
                self.db.currentUser = user
                return user
                # JWT_SECRET = os.getenv("JWT_SECRET")
                # if not JWT_SECRET:
                #     raise ValueError("JWT_SEGMENT missing from .env")
                # payload = {
                #     "user_id": user.id,
                #     "email": user.email,
                #     "role": getattr(user, 'role', 'user'),  # UserDB may need role column
                #     "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=8)
                # }
                # token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

                # with open("jwt.json", "w") as f:
                #     import json
                #     json.dump({"token": token}, f, indent=2)
            else:
                print("Incorrect password")
        return None

    def ListUsers(self):
        engine = self.db.LoginDatabase()

        loggedUser = self.LoginUser()
        if loggedUser is None:
            print("Authentification échouée.")
            return

        with Session(engine) as session:
            stmt = select(UserDB)
            for usr in session.scalars(stmt):
                print(f"{usr.name or 'N/A'} / {usr.id} / {usr.email}")
