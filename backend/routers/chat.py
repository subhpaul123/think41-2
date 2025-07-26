from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal
from models.user import User
from models.conversation import Conversation
from models.message import Message

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

@router.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    # Check if user exists; create if not
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

    # Create conversation if not provided
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

    # Dummy AI response
    ai_reply = f"You said: {request.message}"
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


@router.get("/api/messages/{conversation_id}")
def get_messages(conversation_id: int, db: Session = Depends(get_db)):
    messages = db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.timestamp).all()
    return [
        {"sender": m.sender, "content": m.content, "timestamp": m.timestamp}
        for m in messages
    ]