import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

uri = os.environ.get("MONGO_URL")

client = MongoClient(uri)

db = client.fifty_b_hub

users_collection = db["users"]
proof_requests_collection = db["proof_requests"]

users_collection.create_index('email', unique=True)

