import typer
import traceback
import sentry_sdk
from views.users import app as users_app
from views.contracts import app as contracts_app
from views.clients import app as clients_app
from views.events import app as events_app

sentry_sdk.init(
    dsn="https://32f5bedd53c5f636f9204e88723622bc@o4511344235249664.ingest.de.sentry.io/4511344238198864",
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
)

#app = typer.Typer()
app = typer.Typer(pretty_exceptions_enable=False)

app.add_typer(users_app, name="users")
app.add_typer(contracts_app, name="contracts")
app.add_typer(clients_app, name="clients")
app.add_typer(events_app, name="events")


if __name__ == "__main__":
    # divvv = 1/0
    try:
        app()
        # divvv = 1/0
    except Exception as e:
        sentry_sdk.capture_exception(e)
        sentry_sdk.flush(timeout=5)
        # Extract the file name and line number from the traceback
        tb = traceback.extract_tb(e.__traceback__)[-1]
        file_name = tb.filename
        line_number = tb.lineno
        
        # Print the name of the exception, file, and line number
        print(f"An unexpected error occurred: {type(e).__name__} in {file_name} at line {line_number}. The issue has been reported to Sentry.io")
        

        exit(1)