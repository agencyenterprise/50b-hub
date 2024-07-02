from models.id import Id
from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId
from typing import Optional

class User(BaseModel):
    _id: Id = None
    full_name: str
    email: EmailStr
    hashed_password: Optional[str] = Field(default=None)
    disabled: bool = False

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
        }

