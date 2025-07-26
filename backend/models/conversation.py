from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from database import Base

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("chat_users.id"))
    started_at = Column(DateTime, default=func.now())
