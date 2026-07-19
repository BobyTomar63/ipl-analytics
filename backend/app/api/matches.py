from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db

router = APIRouter(prefix="/api/matches", tags=["Matches"])

# ─── Get All Matches ─────────────────────
@router.get("/")
def get_all_matches(
    season: int = None,
    team: str = None,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    query = """
        SELECT match_id, season, match_date,
               venue, team1, team2, winner,
               result, player_of_match
        FROM matches_raw
        WHERE 1=1
    """
    params = {"limit": limit}

    if season:
        query += " AND season = :season"
        params["season"] = season

    if team:
        query += " AND (team1 = :team OR team2 = :team)"
        params["team"] = team

    query += " ORDER BY match_date DESC LIMIT :limit"

    result = db.execute(text(query), params)
    matches = [
        {
            "match_id": row[0],
            "season": row[1],
            "date": str(row[2]),
            "venue": row[3],
            "team1": row[4],
            "team2": row[5],
            "winner": row[6],
            "result": row[7],
            "player_of_match": row[8]
        }
        for row in result
    ]
    return {
        "status": "success",
        "total": len(matches),
        "matches": matches
    }

# ─── Get Match Detail ────────────────────
@router.get("/{match_id}")
def get_match_detail(
    match_id: int,
    db: Session = Depends(get_db)
):
    # Match info
    match = db.execute(text("""
        SELECT match_id, season, match_date,
               venue, team1, team2, winner,
               result, player_of_match,
               toss_winner, toss_decision
        FROM matches_raw
        WHERE match_id = :match_id
    """), {"match_id": match_id}).fetchone()

    if not match:
        return {"status": "error", "message": "Match not found"}

    # Innings summary
    innings = db.execute(text("""
        SELECT 
            inning,
            batting_team,
            SUM(runs_scored + extras) as total_runs,
            SUM(is_wicket::int) as wickets,
            COUNT(DISTINCT over_num) as overs
        FROM deliveries_raw
        WHERE match_id = :match_id
        GROUP BY inning, batting_team
        ORDER BY inning
    """), {"match_id": match_id})

    innings_data = [
        {
            "inning": row[0],
            "batting_team": row[1],
            "total_runs": row[2],
            "wickets": row[3],
            "overs": row[4]
        }
        for row in innings
    ]

    return {
        "status": "success",
        "match": {
            "match_id": match[0],
            "season": match[1],
            "date": str(match[2]),
            "venue": match[3],
            "team1": match[4],
            "team2": match[5],
            "winner": match[6],
            "result": match[7],
            "player_of_match": match[8],
            "toss_winner": match[9],
            "toss_decision": match[10]
        },
        "innings": innings_data
    }

# ─── Season Stats ────────────────────────
@router.get("/season/{year}/stats")
def get_season_stats(
    year: int,
    db: Session = Depends(get_db)
):
    result = db.execute(text("""
        SELECT 
            COUNT(*) as total_matches,
            COUNT(DISTINCT team1) as teams,
            COUNT(DISTINCT venue) as venues
        FROM matches_raw
        WHERE season = :year
    """), {"year": year}).fetchone()

    # Season winner
    winner = db.execute(text("""
        SELECT winner, COUNT(*) as wins
        FROM matches_raw
        WHERE season = :year
        GROUP BY winner
        ORDER BY wins DESC
        LIMIT 1
    """), {"year": year}).fetchone()

    return {
        "status": "success",
        "season": year,
        "stats": {
            "total_matches": result[0],
            "teams": result[1],
            "venues": result[2],
            "most_wins": winner[0] if winner else None,
            "most_wins_count": winner[1] if winner else 0
        }
    }