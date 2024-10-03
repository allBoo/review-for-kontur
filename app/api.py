from fastapi import FastAPI, Depends

from application.config import settings
from application.ports.api.v1 import urls as v1
from application.ports.api.security import get_api_token_validator, setup_allowed_hosts

app = FastAPI(
    title="Events API",
    description="Mediabox Events API",
    version="1.0.0",
    debug=settings.DEBUG,
    dependencies=[
        Depends(get_api_token_validator(settings.API_TOKEN))
    ],
    # openapi_url="/v1/openapi.json",
    # docs_url="/v1/docs",
    # redoc_url=None,
)
setup_allowed_hosts(app, settings.ALLOWED_HOSTS)

app.include_router(v1.router)
