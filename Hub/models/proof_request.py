from models.user import User
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from enum import Enum
from bson import ObjectId

class ChunkStatus(str, Enum):
    PROCESSED = "PROCESSED"
    PROCESSING = "PROCESSING"
    VERIFIED = "VERIFIED"
    FAILED = "FAILED"

class Chunk(BaseModel):
    _id: int
    proof_request_id: int
    layer: int
    status: ChunkStatus

class ProofRequest(BaseModel):
    _id: Optional[ObjectId]
    name: str
    description: str
    graph_url: str
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
        kwargs.setdefault('exclude', {'owner'})
        return super().dict(*args, **kwargs)

