# {
#   "_id": ObjectId,
#   "user_id": "user_123",
#   "content": "Sip the summer away with our refreshing matcha 🍵☀️",
#   "platform": "Instagram",               // e.g. Instagram, Twitter
#   "hashtags": ["#matcha", "#summer"],
#   "status": "draft",                     // draft | scheduled | posted
#   "created_at": ISODate("2025-06-02T10:00:00Z"),
#   "scheduled_for": ISODate("2025-06-08T10:00:00Z")  // nullable if draft or posted
# }


from datetime import datetime
from bson.objectid import ObjectId # unique distributable ID

from .mongodb import posts_col

def save_post(user_id, content, platform, hashtags, status="draft", scheduled_for=None):
    post_doc = {
        "user_id": user_id,
        "content": content,
        "platform": platform,
        "hashtags": hashtags,
        "status": status,
        "created_at": datetime.utcnow(),
        "scheduled_for": scheduled_for
    }
    result = posts_col.insert_one(post_doc)
    return result.inserted_id

def list_user_posts(user_id, status=None):
    query = {"user_id": user_id}
    if status:
        query["status"] = status
    return list(posts_col.find(query))

def schedule_post(post_id, scheduled_time):
    result = posts_col.update_one(
        {"_id": ObjectId(post_id)},
        {"$set": {"status": "scheduled", "scheduled_for": scheduled_time}}
    )
    return result.modified_count == 1
