from fastapi import APIRouter
from .events import urls

router = APIRouter(
    prefix='/v1'
)
router.include_router(urls.router)
