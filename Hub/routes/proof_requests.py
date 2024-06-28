from fastapi import APIRouter, Body
from services.queue_service import publish_proof_request
from models.proof_request import ProofRequest
from config.database import proof_requests_collection
from schema.schemas import individual_serial, list_serial
from bson import ObjectId
import json

router = APIRouter()

@router.get("/")
async def get_circuits():
    circuits = proof_requests_collection.find()
    return list_serial(circuits)

@router.post("/")
async def create_proof_request(
    name: str = Body(),
    description: str = Body(),
    graph_url: str = Body()
):
    proofRequest = ProofRequest(name=name, description=description, graph_url=graph_url)
    result = proof_requests_collection.insert_one(proofRequest.dict())
    inserted_id = str(result.inserted_id)

    proof_request_message = {
        'proof_request_id': inserted_id,
        'graph_url': 'graph_url',
    }

    proof_request_message_body = json.dumps(proof_request_message)

    publish_proof_request(proof_request_message_body)
