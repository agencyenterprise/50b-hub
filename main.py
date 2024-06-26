from fastapi import FastAPI

from routes.circuits import router as CircuitRouter
from routes.users import router as UserRouter

app = FastAPI()

app.include_router(UserRouter, tags=["User"], prefix="/users")
app.include_router(CircuitRouter, tags=["Circuit"], prefix="/circuits")