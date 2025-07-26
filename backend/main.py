from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from models import Product, User, Conversation, Message
from routers import chat

app = FastAPI()

# Allow frontend (React dev server) to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Your React app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Register routes
app.include_router(chat.router)

@app.get("/")
def root():
    return {"message": "Backend is up"}
