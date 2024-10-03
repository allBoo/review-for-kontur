import typer

from application.config import setup_app_config
from shared.infrastructure.lockbox import setup_lockbox
from shared.infrastructure.logs.setup import setup_logs_from_config_file
from shared.infrastructure.sentry import setup_sentry


def setup_app(
        config_file_path: str = typer.Option(
            "config/app.ini",
            "-c", "--config",
            help="Path to the configuration file",
            is_eager=True
        ),
        debug: bool = typer.Option(
            False,
            help="Debug mode",
            is_eager=True
        )
) -> None:
    setup_logs_from_config_file(config_file_path)
    setup_app_config(config_file_path, debug)
    setup_lockbox()
    setup_sentry()
