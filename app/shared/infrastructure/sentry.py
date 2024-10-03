import sentry_sdk

from config import settings


def setup_sentry() -> None:
    if not settings.SENTRY_DSN:
        return

    sentry_sdk.init(
        dsn=str(settings.SENTRY_DSN),
        environment=settings.SENTRY_ENVIRONMENT,
        traces_sample_rate=0.1,
    )
