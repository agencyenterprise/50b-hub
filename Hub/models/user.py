from pydantic import BaseModel

class User(BaseModel):
    full_name: str
    email: str #@todo: validate email format
    hashed_password: str
    disabled: bool = False
