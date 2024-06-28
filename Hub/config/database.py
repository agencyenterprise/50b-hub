from pymongo import MongoClient

uri = "mongodb://localhost/degenarcade"

client = MongoClient(uri)

db = client.fifty_b_hub

users_collection = db["users"]
proof_requests_collection = db["proof_requests"]

users_collection.create_index('email', unique=True)

