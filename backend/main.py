from fastapi import FastAPI
from database import Base, engine
from models import Product, User, Conversation, Message
from routers import chat

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(chat.router)

@app.get("/")
def root():
    return {"message": "Backend is up"}
