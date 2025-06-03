from pymongo import MongoClient
import os

MONGODB_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGODB_URI)
db = client["post_agent_db"]

posts_col = db["posts"]
convo_col = db["conversations"]
