import typer
import jwt
import bcrypt
from controllers.ManagingUser import ManagingUser
from models.user import UserDB
from database.db_init import db_create_admin

app = typer.Typer()
user_manager = ManagingUser()


@app.command("create")
def create_user():
    # python main.py users create
    print("### Creating user")

    print("# User name: ")
    user_name = input()
    print("# User email: ")
    user_email = input()
    print("# Role  (Gestion/Commercial/Support): ")
    user_role = input()
    while (
        user_role != "Gestion" and user_role != "Commercial" and user_role != "Support"
    ):
        user_role = input()
    print("# Password: ")
    user_pw = input()

    # Simple bcrypt hash (exact pattern from database/db_init.py)
    salt = bcrypt.gensalt()
    hashedPW = bcrypt.hashpw(user_pw.encode("utf-8"), salt).decode("utf-8")

    myUser = UserDB(
        None, name=user_name, email=user_email, role=user_role, password=hashedPW
    )

    created = user_manager.CreateUser(user_item=myUser)
    print("Created: " + str(created))


@app.command("update")
def update_user():
    # python main.py users create
    print("### Creating user")

    print("# User ID: ")
    user_id = input()
    print("# User name: ")
    user_name = input()
    print("# User email: ")
    user_email = input()
    print("# Role  (Gestion/Commercial/Support): ")
    user_role = input()
    while (
        user_role != "Gestion" and user_role != "Commercial" and user_role != "Support"
    ):
        user_role = input()

    myUser = UserDB(
        id=user_id, name=user_name, email=user_email, role=user_role 
    )

    updated = user_manager.UpdateUser(user_item=myUser)
    print("Updated: " + str(updated))


@app.command("createadmin")
def create_admin():
    # python main.py users createadmin
    print("Creating admin")
    db_create_admin()
    print("Created")


@app.command("delete")
def delete_user():
    print("### Deleting user")
    print("# User ID: ")
    user_id = None
    while user_id is None:
        tmp_id = int(input())
        print(tmp_id)
        user_id = tmp_id
    user_manager.DeleteUser(user_id=user_id)


@app.command("list")
def list_users():
    print("### Listing users")
    # SENTRY TEST: divvvv = 1/0
    user_manager.ListUsers()


@app.command("login")
def login_user():
    print("# LOGIN EpicEvents #")
    user_manager.LoginUser()


@app.command("logout")
def login_user():
    print("# Disconnecting...")
    user_manager.Unlog()


@app.command("detail")
def detail_user():
    print("### Detailing user")
    print("# User ID: ")
    user_id = None
    while user_id is None:
        tmp_id = int(input())
        print(tmp_id)
        user_id = tmp_id
    user_manager.DetailUser(user_id=user_id)