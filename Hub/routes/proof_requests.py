from fastapi import APIRouter, Body, Depends
from auth.auth import get_current_active_user
from models.user import User
from services.queue_service import publish_proof_request
from models.proof_request import ProofRequest
from config.database import proof_requests_collection
from schema.schemas import individual_serial, list_serial
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
    graph_url: str = Body(),
    current_user: User = Depends(get_current_active_user)
):
    proofRequest = ProofRequest(name=name, description=description, graph_url=graph_url, owner_id=current_user._id)
    result = proof_requests_collection.insert_one(proofRequest.dict())
    inserted_id = str(result.inserted_id)

    proof_request_message = {
        'proof_request_id': inserted_id,
        'graph_url': 'graph_url',
    }

    proof_request_message_body = json.dumps(proof_request_message)
 
    publish_proof_request(proof_request_message_body)
