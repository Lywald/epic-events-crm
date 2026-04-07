import typer
from controllers.ManagingUser import ManagingUser
from models.user import User, UserDB
from database.db_init import db_create_admin

app = typer.Typer()
user_manager = ManagingUser()

@app.command("create")
def create_user():
    #python main.py users create
    print("### Creating user")
    print("# User name: ")
    user_name = input()
    myUser = User(None, name=user_name)
    userToCreate = UserDB.loadUserDB(myUser)
    #userToCreate = UserDB(user_name, employee_number)
    created = user_manager.CreateUser(user_item=userToCreate)
    print("Created: " + str(created))

@app.command("createadmin")
def create_admin():
    #python main.py users createadmin
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