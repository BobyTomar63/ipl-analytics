from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db

router = APIRouter(prefix="/api/players", tags=["Players"])

# ─── Top Run Scorers ─────────────────────
@router.get("/top-batsmen")
def get_top_batsmen(
    limit: int = 10,
    season: int = None,
    db: Session = Depends(get_db)
):
    if season:
        result = db.execute(text("""
            SELECT 
                d.batsman,
                SUM(d.runs_scored) as total_runs,
                COUNT(DISTINCT d.match_id) as matches,
                ROUND(AVG(d.runs_scored)::numeric, 2) as avg_runs
            FROM deliveries_raw d
            JOIN matches_raw m ON d.match_id = m.match_id
            WHERE m.season = :season
            GROUP BY d.batsman
            ORDER BY total_runs DESC
            LIMIT :limit
        """), {"season": season, "limit": limit})
    else:
        result = db.execute(text("""
            SELECT 
                batsman,
                SUM(runs_scored) as total_runs,
                COUNT(DISTINCT match_id) as matches,
                ROUND(AVG(runs_scored)::numeric, 2) as avg_runs
            FROM deliveries_raw
            GROUP BY batsman
            ORDER BY total_runs DESC
            LIMIT :limit
        """), {"limit": limit})

    players = [
        {
            "rank": i+1,
            "batsman": row[0],
            "total_runs": row[1],
            "matches": row[2],
            "avg_runs": float(row[3])
        }
        for i, row in enumerate(result)
    ]
    return {
        "status": "success",
        "season": season or "All",
        "total": len(players),
        "players": players
    }

# ─── Top Wicket Takers ───────────────────
@router.get("/top-bowlers")
def get_top_bowlers(
    limit: int = 10,
    season: int = None,
    db: Session = Depends(get_db)
):
    if season:
        result = db.execute(text("""
            SELECT 
                d.bowler,
                SUM(d.is_wicket::int) as total_wickets,
                COUNT(DISTINCT d.match_id) as matches
            FROM deliveries_raw d
            JOIN matches_raw m ON d.match_id = m.match_id
            WHERE m.season = :season
            AND d.is_wicket = true
            GROUP BY d.bowler
            ORDER BY total_wickets DESC
            LIMIT :limit
        """), {"season": season, "limit": limit})
    else:
        result = db.execute(text("""
            SELECT 
                bowler,
                SUM(is_wicket::int) as total_wickets,
                COUNT(DISTINCT match_id) as matches
            FROM deliveries_raw
            WHERE is_wicket = true
            GROUP BY bowler
            ORDER BY total_wickets DESC
            LIMIT :limit
        """), {"limit": limit})

    players = [
        {
            "rank": i+1,
            "bowler": row[0],
            "total_wickets": row[1],
            "matches": row[2]
        }
        for i, row in enumerate(result)
    ]
    return {
        "status": "success",
        "season": season or "All",
        "total": len(players),
        "players": players
    }

# ─── Player Stats ────────────────────────
@router.get("/{player_name}/stats")
def get_player_stats(
    player_name: str,
    db: Session = Depends(get_db)
):
    # Batting stats
    batting = db.execute(text("""
        SELECT 
            SUM(runs_scored) as total_runs,
            COUNT(DISTINCT match_id) as matches,
            MAX(runs_scored) as highest_score,
            ROUND(AVG(runs_scored)::numeric, 2) as avg
        FROM deliveries_raw
        WHERE batsman = :player
    """), {"player": player_name}).fetchone()

    # Bowling stats
    bowling = db.execute(text("""
        SELECT 
            SUM(is_wicket::int) as total_wickets,
            COUNT(DISTINCT match_id) as matches
        FROM deliveries_raw
        WHERE bowler = :player
    """), {"player": player_name}).fetchone()

    return {
        "status": "success",
        "player": player_name,
        "batting": {
            "total_runs": batting[0],
            "matches": batting[1],
            "highest_score": batting[2],
            "average": float(batting[3]) if batting[3] else 0
        },
        "bowling": {
            "total_wickets": bowling[0],
            "matches": bowling[1]
        }
    }