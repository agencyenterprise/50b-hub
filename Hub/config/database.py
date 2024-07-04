from pymongo import MongoClient

# uri = "mongodb://localhost:27017/"
uri = "mongodb+srv://kevinkons:<password>@50b-hub.dkfbkz7.mongodb.net/?retryWrites=true&w=majority&appName=50b-hub"

client = MongoClient(uri)

db = client.fifty_b_hub

users_collection = db["users"]
proof_requests_collection = db["proof_requests"]

users_collection.create_index('email', unique=True)

