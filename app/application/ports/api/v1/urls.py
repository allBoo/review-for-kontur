from fastapi import APIRouter
from .events import urls as events  # type: ignore

router = APIRouter(
    prefix='/v1'
)
router.include_router(events.router)
