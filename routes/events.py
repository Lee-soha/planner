from beanie import PydanticObjectId
from fastapi import APIRouter, Body, HTTPException, status, Depends
from database.connection import Database
from auth.authenticate import authenticate
from models.events import Event, EventUpdata
from typing import List, Annotated

event_database = Database(Event)
event_router = APIRouter(
    tags=["Events"],
)

events = []

@event_router.get("/", response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    events = await event_database.get_all()
    return events

@event_router.get("/{_id}", response_model=Event)
async def retrieve_events(_id: PydanticObjectId) -> Event:
    event = await event_database.get(_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist",
        )
    return event


@event_router.post("/new")
async def create_event(body: Event, user: Annotated[str, Depends(authenticate)]) -> dict:
    body.creator = user
    await event_database.save(body)
    return {
        "message": "Event created successfully",
    }

@event_router.put("/{_id}", response_model=Event)
async def update_event(_id: PydanticObjectId, body: EventUpdata, user: Annotated[str, Depends(authenticate)]) -> Event:
    event = await event_database.get(id)
    if event.creator != user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist",
        )
    return event

@event_router.delete("/{_id}")
async def delete_event(_id: PydanticObjectId, user: Annotated[str, Depends(authenticate)]) -> dict:
    event = await event_database.get(id)
    if event.creator!= user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Operation not allowed",
        )
    return {
        "message": "Event deleted successfully",
    }

@event_router.delete("/")
async def delete_all_events(user: Annotated[str, Depends(authenticate)]) -> dict:
    events.clear()
    return {
        "message": "All events deleted successfully",
    }