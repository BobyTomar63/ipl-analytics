from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

# ─── Main Dashboard Overview ─────────────
@router.get("/overview")
def get_overview(db: Session = Depends(get_db)):

    # Total matches
    matches = db.execute(text(
        "SELECT COUNT(*) FROM matches_raw"
    )).scalar()

    # Total seasons
    seasons = db.execute(text(
        "SELECT COUNT(DISTINCT season) FROM matches_raw"
    )).scalar()

    # Total teams
    teams = db.execute(text("""
        SELECT COUNT(DISTINCT team) FROM (
            SELECT team1 as team FROM matches_raw
            UNION
            SELECT team2 as team FROM matches_raw
        ) t
    """)).scalar()

    # Total runs
    runs = db.execute(text(
        "SELECT SUM(runs_scored) FROM deliveries_raw"
    )).scalar()

    # Total wickets
    wickets = db.execute(text(
        "SELECT SUM(is_wicket::int) FROM deliveries_raw"
    )).scalar()

    return {
        "status": "success",
        "overview": {
            "total_matches": matches,
            "total_seasons": seasons,
            "total_teams": teams,
            "total_runs": runs,
            "total_wickets": wickets
        }
    }

# ─── Orange Cap (Top Scorer) ─────────────
@router.get("/orange-cap")
def get_orange_cap(
    season: int = None,
    db: Session = Depends(get_db)
):
    if season:
        result = db.execute(text("""
            SELECT d.batsman, SUM(d.runs_scored) as runs
            FROM deliveries_raw d
            JOIN matches_raw m ON d.match_id = m.match_id
            WHERE m.season = :season
            GROUP BY d.batsman
            ORDER BY runs DESC
            LIMIT 10
        """), {"season": season})
    else:
        result = db.execute(text("""
            SELECT batsman, SUM(runs_scored) as runs
            FROM deliveries_raw
            GROUP BY batsman
            ORDER BY runs DESC
            LIMIT 10
        """))

    players = [
        {"rank": i+1, "batsman": row[0], "runs": row[1]}
        for i, row in enumerate(result)
    ]
    return {
        "status": "success",
        "season": season or "All Time",
        "orange_cap": players
    }

# ─── Purple Cap (Top Wickets) ────────────
@router.get("/purple-cap")
def get_purple_cap(
    season: int = None,
    db: Session = Depends(get_db)
):
    if season:
        result = db.execute(text("""
            SELECT d.bowler, SUM(d.is_wicket::int) as wickets
            FROM deliveries_raw d
            JOIN matches_raw m ON d.match_id = m.match_id
            WHERE m.season = :season
            AND d.is_wicket = true
            GROUP BY d.bowler
            ORDER BY wickets DESC
            LIMIT 10
        """), {"season": season})
    else:
        result = db.execute(text("""
            SELECT bowler, SUM(is_wicket::int) as wickets
            FROM deliveries_raw
            WHERE is_wicket = true
            GROUP BY bowler
            ORDER BY wickets DESC
            LIMIT 10
        """))

    players = [
        {"rank": i+1, "bowler": row[0], "wickets": row[1]}
        for i, row in enumerate(result)
    ]
    return {
        "status": "success",
        "season": season or "All Time",
        "purple_cap": players
    }

# ─── Season Wise Stats ───────────────────
@router.get("/seasons")
def get_all_seasons(db: Session = Depends(get_db)):
    result = db.execute(text("""
        SELECT 
            season,
            COUNT(*) as matches,
            COUNT(DISTINCT team1) as teams
        FROM matches_raw
        GROUP BY season
        ORDER BY season
    """))

    seasons = [
        {
            "season": row[0],
            "matches": row[1],
            "teams": row[2]
        }
        for row in result
    ]
    return {
        "status": "success",
        "total_seasons": len(seasons),
        "seasons": seasons
    }

# ─── Toss Analysis ───────────────────────
@router.get("/toss-analysis")
def get_toss_analysis(db: Session = Depends(get_db)):
    result = db.execute(text("""
        SELECT 
            toss_decision,
            COUNT(*) as total,
            SUM(CASE WHEN toss_winner = winner 
                THEN 1 ELSE 0 END) as toss_winner_won
        FROM matches_raw
        GROUP BY toss_decision
    """))

    analysis = [
        {
            "decision": row[0],
            "total": row[1],
            "won_after_toss": row[2],
            "win_percentage": round((row[2]/row[1])*100, 2)
        }
        for row in result
    ]
    return {
        "status": "success",
        "toss_analysis": analysis
    }