from .mongodb import convo_col

def add_message(session_id, role, content):
    convo = convo_col.find_one({"session_id": session_id})
    message = {"role": role, "content": content}
    if convo:
        convo_col.update_one({"session_id": session_id}, {"$push": {"messages": message}, "$set": {"last_active": datetime.utcnow()}})
    else:
        convo_col.insert_one({"session_id": session_id, "messages": [message], "last_active": datetime.utcnow()})

def get_conversation(session_id):
    convo = convo_col.find_one({"session_id": session_id})
    return convo["messages"] if convo else []
