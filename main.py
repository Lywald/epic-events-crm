import typer
from views.users import app as users_app
from views.contracts import app as contracts_app
from views.clients import app as clients_app
from views.events import app as events_app

app = typer.Typer()

app.add_typer(users_app, name="users")
app.add_typer(contracts_app, name="contracts")
app.add_typer(clients_app, name="clients")
app.add_typer(events_app, name="events")

if __name__ == "__main__":
    app()
