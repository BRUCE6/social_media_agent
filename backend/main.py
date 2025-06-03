from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from agents.post_agent import PostManagementAgent
import os
from pydantic import BaseModel
from typing import Optional, List

from .db.posts import list_user_posts

load_dotenv()

OPEN_API_KEY = os.getenv("OPENAI_API_KEY")
USER_ID = "test_user"

agent = PostManagementAgent(USER_ID, OPEN_API_KEY)

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

# 👇 Replace this with your actual frontend Codespaces URL
origins = [
    "https://fuzzy-adventure-6rgwrw6pr6w25jgw-3000.app.github.dev"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] during dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Request/Response Schemas ---

class ChatRequest(BaseModel):
    message: str

class PostItem(BaseModel):
    id: str
    content: str
    platform: str
    hashtags: List[str]
    status: str
    scheduled_for: Optional[str] = None

# --- Endpoints ---

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        response = agent.run(request.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/posts", response_model=List[PostItem])
async def get_posts(status: Optional[str] = None):
    posts = list_user_posts(USER_ID, status)
    results = []
    for p in posts:
        results.append(PostItem(
            id=str(p["_id"]),
            content=p["content"],
            platform=p.get("platform", ""),
            hashtags=p.get("hashtags", []),
            status=p.get("status", ""),
            scheduled_for=p.get("scheduled_for").isoformat() if p.get("scheduled_for") else None
        ))
    return results
