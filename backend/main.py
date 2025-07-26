from fastapi import FastAPI
from database import Base, engine
from models import Product  # makes sure model is registered

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Backend is up"}
