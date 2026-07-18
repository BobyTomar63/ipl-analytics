from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base

# Models import karna zaroori hai!
from app.models import Team, Player, Match, Delivery

# Tables banao
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="IPL Analytics API",
    description="IPL Data Analysis Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "IPL Analytics API Chal Raha Hai! 🏏",
        "status": "success"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0"
    }