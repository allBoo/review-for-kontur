from fastapi import FastAPI, Depends

from .config import Config
from .api.v1 import urls as v1
from .api.security import get_api_token_validator, setup_allowed_hosts


app = FastAPI(
    title="Events API",
    description="Mediabox Events API",
    version="1.0.0",
    debug=Config.DEBUG,
    dependencies=[
        Depends(get_api_token_validator(Config.API_TOKEN))
    ],
    # openapi_url="/v1/openapi.json",
    # docs_url="/v1/docs",
    # redoc_url=None,
)
setup_allowed_hosts(app, Config.ALLOWED_HOSTS)

app.include_router(v1.router)
