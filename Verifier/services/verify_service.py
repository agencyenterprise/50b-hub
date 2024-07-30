import base64
import json
import dill
import os

from services.queue_service import PikaClient
from dohko.verifier.verifier import ZkVerifier

async def verify_proof(consumer_id: str, proof_request_id: str, circuit: str, proof: str):
    print('Verifying proof for request ' + proof_request_id + ' using verifier: ' + consumer_id)

    layered_circuit = dill.loads(base64.b64decode(circuit))
    proof_transcript = base64.b64decode(proof)
    
    verifier = ZkVerifier(layered_circuit)
    verification = verifier.run_verifier(proof_transcript)

    print(verification)

    pika_client = PikaClient(os.environ.get('RABBITMQ_URL'))

    await pika_client.publish("verifications_queue", json.dumps({
        'proof_request_id': proof_request_id,
        'circuit': circuit,
        'proof': proof,
        'verification': verification
    }))
