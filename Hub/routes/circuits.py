from fastapi import APIRouter
from models.circuits import Circuit
from config.database import circuits_collection
from schema.schemas import individual_serial, list_serial
from bson import ObjectId

router = APIRouter()

@router.get("/")
async def get_circuits():
    circuits = circuits_collection.find()
    return list_serial(circuits)

@router.post("/")
async def create_circuit(circuit: Circuit):
    circuits_collection.insert_one(dict(circuit))
