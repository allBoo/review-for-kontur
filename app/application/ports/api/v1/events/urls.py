import asyncio
import logging

from fastapi import APIRouter
from typing import Annotated
from annotated_types import MaxLen

from config import settings
from application.service.factory import ServiceFactory
from .request import PingRequest, PlayEventRequest, ErrorEventRequest
from .response import EventsResponse, Status

router = APIRouter()

events_saver = ServiceFactory.get_events_saver()
logger = logging.getLogger(__name__)


@router.post("/ping", tags=["events"])
async def ping(request: PingRequest) -> EventsResponse:
    try:
        await events_saver.save(request)
        response = EventsResponse(status=Status.OK)
    except Exception as e:
        response = EventsResponse(status=Status.ERROR, message=str(e))

    return response


@router.post("/events", tags=["events"])
async def events(
    request: Annotated[list[PlayEventRequest | ErrorEventRequest | PingRequest],
                       MaxLen(max_length=settings.INCOMING_EVENTS_LIMIT)]
) -> EventsResponse:
    logger.debug('Received events')

    save = [events_saver.save(event) for event in request]
    await asyncio.gather(*save)

    response = EventsResponse(status=Status.OK)
    return response
