import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status, Body, Response
from auth.auth import authenticate_user, create_access_token, get_current_active_user, hash_password
from config.database import users_collection
from models.user import User
from pydantic import EmailStr, SecretStr, BaseModel, Field
from pymongo.errors import DuplicateKeyError
from datetime import timedelta, datetime

load_dotenv()

router = APIRouter()

class RegisterBody(BaseModel):
    full_name: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str

@router.post("/register")
async def register(body: RegisterBody):
    user = User.model_validate(body, from_attributes=True)
    user.hashed_password=hash_password(body.password)
    try:
        users_collection.insert_one(User.model_dump(user))
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Email already registered")


@router.post("/login")
async def login(
    response: Response,
    email: EmailStr = Body(),
    password: str = Body()
):  
    user = authenticate_user(email, password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect email or password", headers={"WWW-Authenticate": "Bearer"})
    access_token = create_access_token(data={"sub": user.email})

    max_age = 60 * 60 * 24 * 7  # 1 week
    expires = datetime.utcnow() + timedelta(seconds=max_age)

    env = os.environ.get('ENV')
    if env is "local": 
            response.set_cookie(
            key="SESSION_TOKEN",
            value=access_token,
            httponly=True,
            samesite="lax",
            max_age=max_age,
            expires=expires.strftime("%a, %d-%b-%Y %H:%M:%S GMT"),
            path="/"
        )
    else:
        response.set_cookie(
            key="SESSION_TOKEN",
            value=access_token,
            httponly=True,
            samesite="None",
            secure=True,
            max_age=max_age,
            expires=expires.strftime("%a, %d-%b-%Y %H:%M:%S GMT"),
            path="/"
        )

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
