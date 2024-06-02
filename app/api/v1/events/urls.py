import asyncio

from fastapi import APIRouter, Query, Response
from typing import Annotated, Union

from .request import PingRequest, EventRequest, PlayEventRequest, ErrorEventRequest, EventType
from .response import EventsResponse, Status

router = APIRouter()


@router.post("/ping", tags=["events"])
async def ping(request: PingRequest) -> EventsResponse:
    print(f"Ping event: {request}")
    response = EventsResponse(status=Status.OK)
    return response


@router.post("/events", tags=["events"])
async def events(request: list[PlayEventRequest | ErrorEventRequest | PingRequest]) -> EventsResponse:
    for event in request:
        match event.type:
            case EventType.PLAY.value:
                print(f"Play event: {event}")
            case EventType.ERROR.value:
                print(f"Error event: {event}")
            case EventType.PING.value:
                _ = asyncio.create_task(ping(event))

    response = EventsResponse(status=Status.OK, message=str(request[2].model_dump()))
    return response
