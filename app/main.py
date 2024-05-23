from fastapi import FastAPI
from .v1 import urls as v1

app = FastAPI(
    title="Events API",
    description="Mediabox Events API",
    version="1.0.0",
    debug=True,
    # openapi_url="/v1/openapi.json",
    # docs_url="/v1/docs",
    # redoc_url=None,
)

app.include_router(v1.router)
