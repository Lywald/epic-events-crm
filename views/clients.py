import typer
from sqlalchemy import func
from models.contract import ContractDB
from models.client import ClientDB
from controllers.ManagingContract import ManagingContract
from controllers.ManagingClient import ManagingClient
from controllers.ManagingUser import ManagingUser

app = typer.Typer()
client_manager = ManagingClient()
user_manager = ManagingUser()


@app.command("list")
def list_clients():
    # python main.py client list
    print("### Listing contracts")
    client_manager.ListClients()


@app.command("create")
def create_client():
    # python main.py contract create
    loggedUser = user_manager.LoginCheck()  # user_manager.LoginUser()
    if loggedUser is None:
        print("Erreur a l'authentification.")
        return None

    if loggedUser.role.lower() != "commercial":
        print("Seuls les commerciaux peuvent rajouter des clients.")
        return None

    print("### Creating client")

    print("# Client full name: ")
    client_full_name = input()
    print("# Client email: ")
    client_email = input()
    print("# Client phone: ")
    client_phone = input()
    print("# Client Company Name: ")
    client_company_name = input()
    print("# Commercial id: ")
    client_commercial_id = input()

    myClient = ClientDB(
        client_full_name,
        client_email,
        client_phone,
        client_company_name,
        func.now(),
        func.now(),
        1,
    )

    created = client_manager.CreateClient(client_item=myClient)

    print("Created: " + str(created))

    return True


@app.command("delete")
def delete_client():
    print("### Deleting client")
    print("# Client ID: ")
    client_id = None
    while client_id is None:
        tmp_id = int(input())
        print(tmp_id)
        client_id = tmp_id
    client_manager.DeleteClient(client_id=client_id)
