from pydantic import BaseModel

class Circuit(BaseModel):
    name: str
    description: str
