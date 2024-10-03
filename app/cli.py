import typer
from fastapi_cli.cli import app as FastAPICLIApp

from application import setup_app
from application.ports.cli import listener

app = typer.Typer(no_args_is_help=True)

app.callback()(setup_app)
listener.register(app)

app.add_typer(FastAPICLIApp, name='api')

def run():
    app()


__all__ = ['run']
