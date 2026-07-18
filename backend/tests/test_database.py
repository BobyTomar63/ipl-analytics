import pytest
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# ─── TEST 1 — Connection Test ────────────
def test_database_connection():
    print("\n🔍 Database connection test...")
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        assert result.scalar() == 1
    print("✅ Database connected!")

# ─── TEST 2 — Matches Count ─────────────
def test_matches_count():
    print("\n🔍 Matches count test...")
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT COUNT(*) FROM matches_raw")
        )
        count = result.scalar()
        assert count == 1095
    print(f"✅ Matches count: {count}")

# ─── TEST 3 — Deliveries Count ──────────
def test_deliveries_count():
    print("\n🔍 Deliveries count test...")
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT COUNT(*) FROM deliveries_raw")
        )
        count = result.scalar()
        assert count == 260920
    print(f"✅ Deliveries count: {count}")

# ─── TEST 4 — Top Scorer ────────────────
def test_top_scorer():
    print("\n🔍 Top scorer test...")
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT batsman, SUM(runs_scored) as runs
            FROM deliveries_raw
            GROUP BY batsman
            ORDER BY runs DESC
            LIMIT 1
        """))
        row = result.fetchone()
        assert row[0] == 'V Kohli'
        assert row[1] == 8014
    print(f"✅ Top scorer: {row[0]} — {row[1]} runs")

# ─── TEST 5 — Season Range ──────────────
def test_season_range():
    print("\n🔍 Season range test...")
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT MIN(season), MAX(season)
            FROM matches_raw
        """))
        row = result.fetchone()
        assert row[0] >= 2007
        assert row[1] <= 2026
    print(f"✅ Seasons: {row[0]} to {row[1]}")

# ─── TEST 6 — No Invalid Runs ───────────
def test_no_invalid_runs():
    print("\n🔍 Invalid runs test...")
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT COUNT(*) FROM deliveries_raw
            WHERE runs_scored < 0 OR runs_scored > 36
        """))
        count = result.scalar()
        assert count == 0
    print(f"✅ Invalid runs: {count}")

# ─── TEST 7 — Teams Exist ───────────────
def test_teams_exist():
    print("\n🔍 Teams test...")
    teams = ['Mumbai Indians', 'Chennai Super Kings',
             'Royal Challengers Bangalore',
             'Kolkata Knight Riders']
    with engine.connect() as conn:
        for team in teams:
            result = conn.execute(text("""
                SELECT COUNT(*) FROM matches_raw
                WHERE team1 = :team OR team2 = :team
            """), {"team": team})
            count = result.scalar()
            assert count > 0
    print(f"✅ All major teams exist!")