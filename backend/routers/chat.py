from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal
from models.user import User
from models.conversation import Conversation
from models.message import Message
import httpx
import os
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
print("🔐 GROQ_API_KEY:", os.getenv("GROQ_API_KEY"))


router = APIRouter()

class ChatRequest(BaseModel):
    user_id: int
    message: str
    conversation_id: int = None

class ChatResponse(BaseModel):
    conversation_id: int
    user_message: str
    ai_message: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_ai_reply(message: str) -> str:
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are a helpful e-commerce support assistant."},
            {"role": "user", "content": message}
        ],
        "temperature": 0.7
    }

    try:
        response = httpx.post(url, json=payload, headers=headers, timeout=10)
        print("✅ Groq status:", response.status_code)
        print("📦 Groq response:", response.text)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("❌ Groq error:", e)
        return "Sorry, I'm unable to generate a response right now."

@router.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    # Auto-create user
    user = db.query(User).filter(User.id == request.user_id).first()
    if not user:
        user = User(
            id=request.user_id,
            name=f"User{request.user_id}",
            email=f"user{request.user_id}@example.com"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # Auto-create conversation
    if request.conversation_id is None:
        conversation = Conversation(user_id=user.id)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
    else:
        conversation = db.query(Conversation).filter(Conversation.id == request.conversation_id).first()
        if not conversation:
            raise HTTPException(status_code=404, detail="Invalid conversation ID")

    # Save user message
    user_msg = Message(
        conversation_id=conversation.id,
        sender="user",
        content=request.message
    )
    db.add(user_msg)

    # AI response via Groq
    ai_reply = generate_ai_reply(request.message)
    ai_msg = Message(
        conversation_id=conversation.id,
        sender="ai",
        content=ai_reply
    )
    db.add(ai_msg)

    db.commit()

    return {
        "conversation_id": conversation.id,
        "user_message": request.message,
        "ai_message": ai_reply
    }
