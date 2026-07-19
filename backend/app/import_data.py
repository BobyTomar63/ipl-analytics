import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def clean_matches(df):
    print("🧹 Matches data clean ho raha hai...")
    df['season'] = df['season'].astype(str).str[:4].astype(int)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['city']            = df['city'].fillna('Unknown')
    df['player_of_match'] = df['player_of_match'].fillna('Unknown')
    df['winner']          = df['winner'].fillna('No Result')
    df['result']          = df['result'].fillna('No Result')
    df['method']          = df['method'].fillna('None') if 'method' in df.columns else df
    return df

def clean_deliveries(df):
    print("🧹 Deliveries data clean ho raha hai...")
    if 'extras_type' in df.columns:
        df['extras_type'] = df['extras_type'].fillna('none')
    if 'player_dismissed' in df.columns:
        df['player_dismissed'] = df['player_dismissed'].fillna('none')
    if 'dismissal_kind' in df.columns:
        df['dismissal_kind'] = df['dismissal_kind'].fillna('none')
    if 'fielder' in df.columns:
        df['fielder'] = df['fielder'].fillna('none')
    df['is_wicket'] = df['is_wicket'].astype(bool)
    return df

def import_matches():
    print("\n📊 Matches import shuru...")
    df = pd.read_csv("data/matches.csv")
    df = clean_matches(df)
    df_clean = df[[
        'id', 'season', 'city', 'date',
        'player_of_match', 'venue',
        'team1', 'team2', 'toss_winner',
        'toss_decision', 'winner', 'result',
        'result_margin'
    ]].copy()
    df_clean.columns = [
        'match_id', 'season', 'city', 'match_date',
        'player_of_match', 'venue',
        'team1', 'team2', 'toss_winner',
        'toss_decision', 'winner', 'result',
        'result_margin'
    ]
    df_clean.to_sql(
        'matches_raw',
        engine,
        if_exists='replace',
        index=False
    )
    print(f"✅ {len(df_clean)} matches import ho gaye!")

def import_deliveries():
    print("\n📊 Deliveries import shuru...")
    df = pd.read_csv("data/deliveries.csv")
    df = clean_deliveries(df)
    df = df.rename(columns={
        'over':         'over_num',
        'ball':         'ball_num',
        'batter':       'batsman',
        'batsman_runs': 'runs_scored',
        'extra_runs':   'extras',
    })
    chunk_size = 10000
    total      = len(df)
    for i in range(0, total, chunk_size):
        chunk = df[i:i+chunk_size]
        chunk.to_sql(
            'deliveries_raw',
            engine,
            if_exists='replace' if i == 0 else 'append',
            index=False
        )
        print(f"  → {min(i+chunk_size, total)}/{total} rows imported...")
    print(f"✅ {total} deliveries import ho gayi!")

def validate_data():
    print("\n🔍 Data Validation Shuru...")
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT COUNT(*) FROM matches_raw")
        )
        count = result.scalar()
        print(f"✅ Total Matches: {count}")

        result = conn.execute(text("""
            SELECT COUNT(*) FROM matches_raw
            WHERE season < 2007 OR season > 2026
        """))
        invalid = result.scalar()
        print(f"{'✅' if invalid == 0 else '❌'} Invalid seasons: {invalid}")

        result = conn.execute(text("""
            SELECT COUNT(*) FROM matches_raw
            WHERE winner IS NULL OR winner = ''
        """))
        null_winners = result.scalar()
        print(f"{'✅' if null_winners == 0 else '⚠️'} Null winners: {null_winners}")

        result = conn.execute(
            text("SELECT COUNT(*) FROM deliveries_raw")
        )
        count = result.scalar()
        print(f"✅ Total Deliveries: {count}")

        result = conn.execute(text("""
            SELECT COUNT(*) FROM deliveries_raw
            WHERE runs_scored < 0 OR runs_scored > 36
        """))
        invalid_runs = result.scalar()
        print(f"{'✅' if invalid_runs == 0 else '❌'} Invalid runs: {invalid_runs}")

        result = conn.execute(text("""
            SELECT COUNT(*) FROM deliveries_raw
            WHERE over_num < 0 OR over_num > 19
        """))
        invalid_overs = result.scalar()
        print(f"{'✅' if invalid_overs == 0 else '❌'} Invalid overs: {invalid_overs}")

    print("\n🎉 Validation Complete!")

def import_new_data():
    print("\n📊 New data import shuru...")

    # New matches import
    df_matches = pd.read_csv("data/new_matches.csv")

    # Sirf new seasons lo (2025, 2026)
    df_new = df_matches[df_matches['season'].isin([2025, 2026])]
    print(f"New matches: {len(df_new)}")

    df_new.to_sql(
        'matches_raw',
        engine,
        if_exists='append',
        index=False
    )
    print(f"✅ {len(df_new)} new matches imported!")

    # New deliveries import
    df_deliveries = pd.read_csv("data/new_deliveries.csv")
    new_match_ids = df_new['match_id'].tolist()
    df_new_del = df_deliveries[
        df_deliveries['match_id'].isin(new_match_ids)
    ]
    print(f"New deliveries: {len(df_new_del)}")

    chunk_size = 10000
    total = len(df_new_del)
    for i in range(0, total, chunk_size):
        chunk = df_new_del[i:i+chunk_size]
        chunk.to_sql(
            'deliveries_raw',
            engine,
            if_exists='append',
            index=False
        )
        print(f"  → {min(i+chunk_size, total)}/{total} rows...")

    print(f"✅ {total} new deliveries imported!")

if __name__ == "__main__":
    import_new_data()