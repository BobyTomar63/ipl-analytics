from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.models import Team, Player, Match, Delivery
from app.api import teams, players, matches, dashboard

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="IPL Analytics API",
    description="IPL Data Analysis Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://ipl-analytics-blue.vercel.app",
        "*"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(teams.router)
app.include_router(players.router)
app.include_router(matches.router)
app.include_router(dashboard.router)

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