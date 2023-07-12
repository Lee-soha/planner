from beanie import PydanticObjectId
from fastapi import APIRouter, Body, HTTPException, status
from database.connection import Database

from models.events import Event, EventUpdata
from typing import List

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
async def create_event(body: Event) -> dict:
    await event_database.save(body)
    return {
        "message": "Event created successfully",
    }

@event_router.put("/{_id}", response_model=Event)
async def update_event(_id: PydanticObjectId, body: EventUpdata) -> Event:
    updated_event = await event_database.update(id, body)
    if not updated_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist",
        )
    return updated_event

@event_router.delete("/{_id}")
async def delete_event(_id: PydanticObjectId) -> dict:
    event = await event_database.delete(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist",
        )
    return {
        "message": "Event deleted successfully",
    }

@event_router.delete("/")
async def delete_all_events() -> dict:
    events.clear()
    return {
        "message": "All events deleted successfully",
    }