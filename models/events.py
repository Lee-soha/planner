from pydantic import BaseModel
from beanie import Document, PydanticObjectId
from typing import List, Optional

class Event(Document):
    _id: Optional[PydanticObjectId]
    creator: Optional[str]
    title: str
    image: str
    description: str
    tags: List[str]
    location: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "FastAPI Book Launch",
                "image": "http://linktomyimage.com/image.png",
                "description": "We will be discussing the contents of the FastAPI book in this event. Ensure to come with your own copy to win gifts!",
                "tags": ["python", "fastapi", "book", "launch"],
                "location": "Google Meet"
            }
        }

    class Settings:
        collection = "events" # In beanie, you specify the collection using this attribute.


class EventUpdata(BaseModel):
    title: Optional[str]
    image: Optional[str]
    description: Optional[str]
    tags: Optional[List[str]]
    location: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "title": "FastAPI Book Launch",
                "image": "http://linktomyimage.com/image.png",
                "description": "We will be discussing the contents of the FastAPI book in this event. Ensure to come with your own copy to win gifts!",
                "tags": ["python", "fastapi", "book", "launch"],
                "location": "Google Meet"
            }
        }
