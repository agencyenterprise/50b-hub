from fastapi import FastAPI

from routes.proof_requests import router as ProofRequestRouter
from routes.users import router as UserRouter

app = FastAPI()

app.include_router(UserRouter, tags=["User"], prefix="/users")
app.include_router(ProofRequestRouter, tags=["Circuit"], prefix="/proof_requests")