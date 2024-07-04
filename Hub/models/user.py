from models.id import ID
from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId
from typing import Optional

class User(BaseModel):
    id: ID = None
    full_name: str
    email: EmailStr
    hashed_password: Optional[str] = Field(default=None)
    disabled: bool = False

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
        }
    
    def model_dump(self, *args, **kwargs):
        kwargs.setdefault('exclude', {'id'})
        return super().model_dump(*args, **kwargs)

