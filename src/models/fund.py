from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from src.schemas.general import PyObjectId
from pydantic import BaseModel, Field
from bson import ObjectId

class Fund(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    name: str
    minimum_amount: float
    category: str
    created_at: datetime = datetime.now()

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = { ObjectId: str }
