import typer
from sqlalchemy import func
from models.event import EventDB
from controllers.ManagingContract import ManagingContract
from controllers.ManagingUser import ManagingUser
from controllers.ManagingEvent import ManagingEvent

app = typer.Typer()
contract_manager = ManagingContract()
user_manager = ManagingUser()
event_manager = ManagingEvent()


@app.command("list")
def list_events():
    # python main.py contracts list
    print("### Listing events")
    event_manager.ListEvents()


@app.command("create")
def create_event():
    # python main.py events create

    loggedUser = user_manager.LoginCheck() # user_manager.LoginUser()
    if loggedUser is None:
        print("Auhentification échouée.")
        return None
    if loggedUser.role.lower() != "commercial":
        print("Seul le département commercial peut créer un évènement.")
        return None

    print("### Création de l'évènement")
    print("# Nom de l'évènement : ")
    event_name = input()
    print("# Lieu de l'évènement : ")
    event_location = input()
    print("# Nombre de participants: ")
    event_attendees = input()
    print("#ID Contrat : ")
    event_contract_id = str(input())
    print("# Nom du client : ")
    event_client_name = input()
    print("# Contact du client : ")
    event_client_contact = input()
    print("# Notes diverses :")
    event_notes = input()
    print("# Date début (AAAA-MM-JJ) :")
    event_date_start = input()
    print("# Date fin (AAAA-MM-JJ) :")
    event_date_end = input()

    myEvent = EventDB(
        None,
        event_name,
        event_contract_id,
        event_client_name,
        event_client_contact,
        event_date_start,
        event_date_end,
        None,
        event_location,
        event_attendees,
        event_notes,
    )

    # myContract = ContractDB(None, contract_client_id, contract_commercial_id, contract_total_amount, contract_remaining_amount, func.now(), contract_is_signed)

    # created = contract_manager.CreateContract(contract_item=myContract)
    created = event_manager.CreateEvent(event_item=myEvent)
    print("Created: " + str(created))
