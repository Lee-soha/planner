from beanie import init_beanie, PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional, Any, List
from pydantic import BaseSettings, BaseModel
from models.users import User
from models.events import Event

class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None
    DATABASE_NAME: Optional[str] = "My_Database"
    SECRET_KEY: Optional[str] = None

    async def initialize_database(self):
        clint = AsyncIOMotorClient(self.DATABASE_URL)
        await init_beanie(database=clint[self.DATABASE_NAME], document_models =[Event, User])
    
    class Config:
        env_file = ".env"

class Database:
    def __init__(self, model):
        self.model = model
    
    async def save(self, document) -> None:
        return await document.create() 
    
    async def get(self, _id: PydanticObjectId) -> Any:
        doc = await self.model.get(_id)
        if doc:
            return doc
        return False
    
    async def get_all(self) -> List[Any]:
        docs = await self.model.find_all().to_list(length=None)
        return docs
    
    async def update(self, _id: PydanticObjectId, body: BaseModel) -> Any:
        doc_id = _id 
        des_body = body.dict()
        des_body = {k: v for k, v in des_body.items() if v is not None}
        update_query = {"$set": {field: value for field, value in des_body.items()}}

        doc = await self.model.get(doc_id)
        if not doc:
            return False
        await doc.update(update_query)
        return doc

    async def delete(self, _id: PydanticObjectId) -> bool: 
        doc = await self.get(_id)
        if not doc:
            return False
        await doc.delete()
        return True

    