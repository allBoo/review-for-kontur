import typer

#from app.service.factory import ServiceFactory

__all__ = ['register']


def restore():
    pass


def register(app: typer.Typer):
    app.command(name="restore")(restore)

