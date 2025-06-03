from langchain.memory import ConversationBufferMemory
from db.conversations import add_message, get_conversation

class MongoChatMemory(ConversationBufferMemory):
    session_id: str
    
    def __init__(self, session_id: str):
        super().__init__(session_id=session_id, memory_key="chat_history")
        self.session_id = session_id

    def load_memory_variables(self, inputs):
        messages = get_conversation(self.session_id)
        # format for LangChain chat memory as string
        chat_str = ""
        for msg in messages:
            role = "Human" if msg["role"] == "user" else "AI"
            chat_str += f"{role}: {msg['content']}\n"
        return {"chat_history": chat_str}

    def save_context(self, inputs, outputs):
        add_message(self.session_id, "user", inputs.get("input", ""))
        add_message(self.session_id, "agent", outputs.get("output", ""))
