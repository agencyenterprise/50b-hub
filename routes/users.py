from fastapi import APIRouter, Depends, HTTPException, status, Body, Response
from auth.auth import authenticate_user, create_access_token, get_current_active_user, hash_password
from config.database import users_collection
from models.user import User
from pydantic import EmailStr

router = APIRouter()

@router.post("/register")
async def register(
    full_name: str = Body(),
    email: EmailStr = Body(),
    password: str = Body()
):
    user: User = User(
        full_name=full_name,
        email=email,
        hashed_password=hash_password(password)
    )
    users_collection.insert_one(dict(user))

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

    response.set_cookie(
        key="SESSION_TOKEN",
        # value=user["session_token"],
        value=access_token,
        secure=True,
        httponly=True,
        samesite="none",
        max_age=60*60*24*7
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
