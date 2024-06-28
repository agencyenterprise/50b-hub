from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from enum import Enum

class ChunkStatus(str, Enum):
    PROCESSED = "PROCESSED"
    PROCESSING = "PROCESSING"
    FAILED = "FAILED"

class Chunk(BaseModel):
    _id: int
    proof_request_id: int
    layer: int
    status: ChunkStatus

class ProofRequest(BaseModel):
    _id: int
    name: str
    description: str
    graph_url: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    chunks: List[Chunk] = Field(default_factory=list)
