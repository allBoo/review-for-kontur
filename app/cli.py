from logging.config import dictConfig
import typer

from app.infrastructure.logs.config import LogConfig
from app.ports.cli import listener, restore

dictConfig(LogConfig(LOG_LEVEL="INFO").dict())


app = typer.Typer(no_args_is_help=True)

listener.register(app)
restore.register(app)


def run():
    app()


__all__ = ['run']
