import typer
from views.users import app as users_app
from views.contracts import app as contracts_app

app = typer.Typer()

app.add_typer(users_app, name="users")
app.add_typer(contracts_app, name="contracts")

if __name__ == "__main__":
    app()
