import typer
from sqlalchemy import func
from models.contract import ContractDB
from controllers.ManagingContract import ManagingContract
from controllers.ManagingUser import ManagingUser

app = typer.Typer()
contract_manager = ManagingContract()
user_manager = ManagingUser()


@app.command("list")
def list_contracts():
    # python main.py contracts list
    print("### Listing contracts")
    contract_manager.ListContracts()


@app.command("create")
def create_contract():
    # python main.py contract create

    loggedUser = user_manager.LoginCheck() # user_manager.LoginUser()
    if loggedUser is None:
        print("Auhentification échouée.")
        return None
    if loggedUser.role != "gestion" and loggedUser.role != "Gestion":
        print("Seul le département gestion peut créer un contrat.")
        return None

    print("### Creating contract")
    print("# Client id: ")
    contract_client_id = input()
    print("# Commercial id: ")
    contract_commercial_id = input()
    print("# Total amount: ")
    contract_total_amount = input()
    contract_remaining_amount = contract_total_amount
    print("# Is contract signed? (yes/no): ")
    contract_is_signed = input()
    while contract_is_signed != "yes" and contract_is_signed != "no":
        contract_is_signed = input()
    if contract_is_signed == "yes":
        contract_is_signed = True
    else:
        contract_is_signed = False

    myContract = ContractDB(
        None,
        contract_client_id,
        contract_commercial_id,
        contract_total_amount,
        contract_remaining_amount,
        func.now(),
        contract_is_signed,
    )

    created = contract_manager.CreateContract(contract_item=myContract)
    print("Created: " + str(created))


@app.command("delete")
def delete_contract():
    print("### Deleting contract")
    print("# Contract ID: ")
    contract_id = None
    while contract_id is None:
        tmp_id = int(input())
        print(tmp_id)
        contract_id = tmp_id
    contract_manager.DeleteContract(contract_id=contract_id)