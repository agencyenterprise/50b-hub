from fastapi import APIRouter, Body, Depends
from auth.auth import get_current_active_user
from models.user import User
from services.queue_service import PikaClient
from models.proof_request import ProofRequest
from config.database import proof_requests_collection
from schemas.proof_request_schema import individual_serial, list_serial
from bson import ObjectId
import json
import os

router = APIRouter()

@router.get("/")
async def get_proof_requests(current_user: User = Depends(get_current_active_user)):
    proofs = proof_requests_collection.find({"owner_id": current_user.id })
    return list_serial(proofs)

@router.post("/")
async def create_proof_request(
    name: str = Body(),
    description: str = Body(),
    ai_model_name: str = Body(),
    ai_model_inputs: str = Body(),
    current_user: User = Depends(get_current_active_user)
):
    proofRequest = ProofRequest(name=name, description=description, ai_model_name=ai_model_name, ai_model_inputs=ai_model_inputs, owner_id=ObjectId(current_user.id))
    result = proof_requests_collection.insert_one(proofRequest.dict())
    inserted_id = str(result.inserted_id)

    proof_request_message = {
        "proof_request_id": inserted_id,
        "ai_model_name": ai_model_name,
        "ai_model_inputs": ai_model_inputs,
    }

    proof_request_message_body = json.dumps(proof_request_message)
 
    pika_client = PikaClient(os.environ.get("RABBITMQ_URL"))
    await pika_client.publish("requests_queue", proof_request_message_body)
