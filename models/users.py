from pydantic import BaseModel, EmailStr
from typing import Optional, List
from beanie import Document, Link, Document, PydanticObjectId
from models.events import Event

class User(Document, BaseModel):
    _id: Optional[PydanticObjectId]
    email: EmailStr
    password: str
    events: Optional[List[Link[Event]]]

    class Settings:
        name = "users"
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "fastapi@packt.com",
                "username": "strong!!!",
                "events": [],
            }
        }
class TokenResponse(BaseModel):
    access_token: str
    token_type: str

# class UserSignIn(BaseModel):
#     email: EmailStr
#     password: str

#     class Config:
#         json_schema_extra = {
#             "example": {
#                 "email": "fastapi@packt.com",
#                 "password": "strong!!!",
#             }
#         }