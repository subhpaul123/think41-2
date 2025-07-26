from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime, func, String
from database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    sender = Column(String)  # 'user' or 'ai'
    content = Column(Text)
    timestamp = Column(DateTime, default=func.now())
