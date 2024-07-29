from models.user import User
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from enum import Enum
from bson import ObjectId
from models.id import ID

class ChunkStatus(str, Enum):
    PROCESSED = "PROCESSED"
    PROCESSING = "PROCESSING"
    VERIFIED = "VERIFIED"
    FAILED = "FAILED"

class Chunk(BaseModel):
    id: ID = None
    proof_request_id: int
    layer: int
    status: ChunkStatus

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
        }

class ProofRequest(BaseModel):
    id: ID = None
    name: str
    description: str
    ai_model_name: str
    ai_model_inputs: str
    owner_id: ObjectId
    owner: Optional[User] = None
    chunks: List[Chunk] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
        }


    def populate_owner(self, db):
        user_data = db.users.find_one({"_id": self.owner_id})
        if user_data:
            self.owner = User(**user_data)
    
    def dict(self, *args, **kwargs):
        kwargs.setdefault('exclude', {'owner', 'id'})
        return super().dict(*args, **kwargs)
    
    def model_dump(self, *args, **kwargs):
        kwargs.setdefault('exclude', {'owner', 'id'})
        return super().model_dump(*args, **kwargs)

