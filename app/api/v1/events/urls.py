from fastapi import APIRouter, Query
from typing import Annotated, Union

from .request import PingRequest, EventRequest, PlayEventRequest, ErrorEventRequest
from .response import EventsResponse, Status

router = APIRouter()


@router.post("/ping", tags=["events"])
async def ping(request: PingRequest) -> EventsResponse:
    response = EventsResponse(status=Status.OK)
    return response


@router.post("/events", tags=["events"])
async def events(request: list[PlayEventRequest | ErrorEventRequest | PingRequest]) -> EventsResponse:
    response = EventsResponse(status=Status.OK, message=str(request[2].model_dump()))
    return response

