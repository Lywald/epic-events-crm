import typer

app = typer.Typer()

@app.command("list")
def list_contracts():
    #python main.py contracts list
    print("Listing contracts")
