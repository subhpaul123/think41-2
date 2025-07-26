from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
from models.user import User
from models.conversation import Conversation
from models.message import Message
import httpx
import os
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

router = APIRouter()

# ------------------------
# Request + Response Schemas
# ------------------------

class ChatRequest(BaseModel):
    user_id: int
    message: str
    conversation_id: int = None

class ChatResponse(BaseModel):
    conversation_id: int
    user_message: str
    ai_message: str

class MessageOut(BaseModel):
    id: int
    sender: str
    content: str
    timestamp: datetime

    class Config:
        orm_mode = True

# ------------------------
# DB Dependency
# ------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------------
# AI Call to Groq
# ------------------------

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
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("❌ Groq error:", e)
        return "Sorry, I'm unable to generate a response right now."

# ------------------------
# POST /api/chat
# ------------------------

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

    if request.message.strip():
        # Save user message
        user_msg = Message(
            conversation_id=conversation.id,
            sender="user",
            content=request.message
        )
        db.add(user_msg)

        # Generate AI response
        ai_reply = generate_ai_reply(request.message)
        ai_msg = Message(
            conversation_id=conversation.id,
            sender="ai",
            content=ai_reply
        )
        db.add(ai_msg)
    else:
        ai_reply = ""

    db.commit()

    return {
        "conversation_id": conversation.id,
        "user_message": request.message,
        "ai_message": ai_reply
    }

# ------------------------
# GET /api/conversations/{conversation_id}
# ------------------------

@router.get("/api/conversations/{conversation_id}", response_model=List[MessageOut])
def get_conversation_history(
    conversation_id: int = Path(..., title="Conversation ID"),
    db: Session = Depends(get_db)
):
    conversation = db.query(Conversation).filter_by(id=conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.timestamp)
        .all()
    )
    return messages 

# ------------------------
# GET /api/conversations
# ------------------------

@router.get("/api/conversations")
def list_conversations(db: Session = Depends(get_db)):
    return db.query(Conversation).order_by(Conversation.created_at.desc()).all()
