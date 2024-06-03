import logging
from fastapi import APIRouter
from typing import Annotated
from annotated_types import MaxLen

from app.config import Config
from app.service.factory import ServiceFactory
from .request import PingRequest, PlayEventRequest, ErrorEventRequest
from .response import EventsResponse, Status

router = APIRouter()

events_saver = ServiceFactory.get_raw_events_saver()
logger = logging.getLogger(__name__)


@router.post("/ping", tags=["events"])
async def ping(request: PingRequest) -> EventsResponse:
    try:
        events_saver.save(request)
        response = EventsResponse(status=Status.OK)
    except Exception as e:
        response = EventsResponse(status=Status.ERROR, message=str(e))

    return response


@router.post("/events", tags=["events"])
async def events(
    request: Annotated[list[PlayEventRequest | ErrorEventRequest | PingRequest],
                       MaxLen(max_length=Config.INCOMING_EVENTS_LIMIT)]
) -> EventsResponse:
    logger.debug('Received events')
    for event in request:
        await events_saver.save(event)

    response = EventsResponse(status=Status.OK)
    return response
