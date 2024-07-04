from models.user import User
from config.database import users_collection

def get_user_by_email(email: str):
    user_data = users_collection.find_one({"email": email})
    if not user_data:
        return None
    
    return User(**user_data)