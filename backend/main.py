from fastapi import FastAPI
from database import Base, engine
from models import Product, User, Conversation, Message

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Backend is up"}
