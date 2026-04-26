from sqlalchemy import select
from sqlalchemy.orm import Session
import os
import jwt
import json
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

        loggedUser = self.LoginCheck() # self.LogFromJWT()
        if loggedUser is None:
            print("Authentification échouée.")
            return
       
        if loggedUser.role.lower() != "gestion":
            print("Authentification échouée: seul Gestion peut créer un utilisateur.")
            return None

        with Session(engine) as session:
            session.add(user_item)
            session.commit()
            return True
        return False

    def DeleteUser(self, user_id: int):
        engine = self.db.LoginDatabase()
        if engine is None:
            print("Connection échouée.")
            return None

        loggedUser = self.LoginCheck() # self.LogFromJWT()
        if loggedUser is None:
            print("Authentification échouée.")
            return 

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
                JWT_SECRET = os.getenv("JWT_SECRET")
                if not JWT_SECRET:
                    raise ValueError("JWT_SEGMENT missing from .env")
                payload = {
                    "user_id": user.id,
                    "email": user.email,
                    "role": getattr(user, 'role', 'user'),  # UserDB may need role column
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=8)
                }
                token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
                with open("jwt.json", "w") as f:
                    import json
                    json.dump({"token": token}, f, indent=2)
                return user
            else:
                print("Incorrect password")
        return None

    def ListUsers(self):
        engine = self.db.LoginDatabase()

        loggedUser = self.LoginCheck() #LogFromJWT()
        if loggedUser is None:
            print("Authentification échouée.")
            return 
        
        with Session(engine) as session:
            stmt = select(UserDB)
            for usr in session.scalars(stmt):
                print(f"{usr.name or 'N/A'} / {usr.id} / {usr.email}")

    def LogFromJWT(self):
        jwt_key = os.getenv("JWT_SECRET")
        if not jwt_key:
            print("Clef JWT manquante pour authentifier.")
            return None
        
        try:
            with open("jwt.json", "r") as f:
                data = json.load(f)

            token = data.get("token")
            if not token:
                print("Token manquant dans jwt.json")

            payload = jwt.decode(token, jwt_key, algorithms=["HS256"])
            user_id = payload.get("user_id")
            if user_id is None:
                print("Token manquant le user_id")

            engine = self.db.LoginDatabase()
            if engine is None:
                return None
            # Manage expirated tokens
            with Session(engine) as session:
                user = session.get(UserDB, int(user_id))
                if user is None:
                    print("User pas trouvé dans la base de données")
                    return None
                self.db.currentUser = user
                return user
        except:
            print("Erreur a la connexion JWT")
            return None
        
    def LoginCheck(self):
        loggedUser = self.LogFromJWT()
        if loggedUser is None:
            loggedUser = self.LoginUser()
        if loggedUser is None:
            print("Authentification échouée.")
            return None
        else:
            print(f"(Auto Logged in to {loggedUser.email} as {loggedUser.role})")
        return loggedUser
