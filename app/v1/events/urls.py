from fastapi import APIRouter

from .request import PingRequest, EventRequest
from .response import EventsResponse, Status

router = APIRouter()


@router.post("/ping", tags=["events"])
async def ping(request: PingRequest) -> EventsResponse:
    response = EventsResponse(status=Status.OK)
    return response


@router.post("/events", tags=["events"])
async def events(events: list[EventRequest]) -> EventsResponse:
    #response = EventsResponse(status=Status.OK, message=events[0].__class__)
    response = EventsResponse(status=Status.OK, message=str(events[0].__class__))
    return response

