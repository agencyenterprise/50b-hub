def individual_serial(circuit) -> dict:
    return {
        "id": str(circuit["_id"]),
        "name": circuit["name"],
        "description": circuit["description"],
    }

def list_serial(circuits) -> list:
    return [individual_serial(circuit) for circuit in circuits]