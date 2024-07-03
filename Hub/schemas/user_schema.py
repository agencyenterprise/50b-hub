def individual_serial(user) -> dict:
    return {
        "id": str(user["id"]),
        "full_name": user["full_name"],
        "email": user["email"],
    }

def list_serial(users) -> list:
    return [individual_serial(user) for user in users]