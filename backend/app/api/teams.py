from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db

router = APIRouter(prefix="/api/teams", tags=["Teams"])

# ─── GET All Teams ───────────────────────
@router.get("/")
def get_all_teams(db: Session = Depends(get_db)):
    result = db.execute(text("""
        SELECT DISTINCT team1 as team_name
        FROM matches_raw
        UNION
        SELECT DISTINCT team2 as team_name
        FROM matches_raw
        ORDER BY team_name
    """))
    teams = [row[0] for row in result]
    return {
        "status": "success",
        "total": len(teams),
        "teams": teams
    }

# ─── GET Team Stats ──────────────────────
@router.get("/{team_name}/stats")
def get_team_stats(team_name: str, db: Session = Depends(get_db)):
    result = db.execute(text("""
        SELECT 
            COUNT(*) as total_matches,
            SUM(CASE WHEN winner = :team THEN 1 ELSE 0 END) as wins,
            COUNT(*) - SUM(CASE WHEN winner = :team THEN 1 ELSE 0 END) as losses
        FROM matches_raw
        WHERE team1 = :team OR team2 = :team
    """), {"team": team_name})
    row = result.fetchone()
    return {
        "status": "success",
        "team": team_name,
        "stats": {
            "total_matches": row[0],
            "wins": row[1],
            "losses": row[2],
            "win_percentage": round((row[1]/row[0])*100, 2)
        }
    }

# ─── GET Team Season Stats ───────────────
@router.get("/{team_name}/seasons")
def get_team_seasons(team_name: str, db: Session = Depends(get_db)):
    result = db.execute(text("""
        SELECT 
            season,
            COUNT(*) as matches,
            SUM(CASE WHEN winner = :team THEN 1 ELSE 0 END) as wins
        FROM matches_raw
        WHERE team1 = :team OR team2 = :team
        GROUP BY season
        ORDER BY season
    """), {"team": team_name})
    seasons = [
        {"season": row[0], "matches": row[1], "wins": row[2]}
        for row in result
    ]
    return {
        "status": "success",
        "team": team_name,
        "seasons": seasons
    }