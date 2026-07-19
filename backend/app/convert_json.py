import json
import pandas as pd
import os
from pathlib import Path

JSON_FOLDER = "data/ipl_json"
OUTPUT_FOLDER = "data"

def convert_json_to_csv():
    matches = []
    deliveries = []
    match_id_counter = 100000

    json_files = list(Path(JSON_FOLDER).glob("*.json"))
    total = len(json_files)
    print(f"📁 Total JSON files: {total}")

    for i, json_file in enumerate(json_files):
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)

            info = data.get('info', {})
            innings_data = data.get('innings', [])

            # Season nikalo
            dates = info.get('dates', [])
            if not dates:
                continue

            date = dates[0]
            year = int(date.split('-')[0])

            # Sirf IPL seasons
            if year < 2007:
                continue

            # Teams
            teams = info.get('teams', [])
            if len(teams) < 2:
                continue

            team1 = teams[0]
            team2 = teams[1]

            # Winner
            outcome = info.get('outcome', {})
            winner = outcome.get('winner', 'No Result')

            # Venue
            venue = info.get('venue', 'Unknown')
            city = info.get('city', 'Unknown')

            # Toss
            toss = info.get('toss', {})
            toss_winner = toss.get('winner', '')
            toss_decision = toss.get('decision', '')

            # Player of match
            player_of_match = ''
            pom = info.get('player_of_match', [])
            if pom:
                player_of_match = pom[0]

            match_id = match_id_counter
            match_id_counter += 1

            # Match add karo
            matches.append({
                'match_id': match_id,
                'season': year,
                'city': city,
                'match_date': date,
                'player_of_match': player_of_match,
                'venue': venue,
                'team1': team1,
                'team2': team2,
                'toss_winner': toss_winner,
                'toss_decision': toss_decision,
                'winner': winner,
                'result': outcome.get('by', {}).get('runs', ''),
                'result_margin': ''
            })

            # Deliveries
            for inning_num, inning in enumerate(innings_data, 1):
                batting_team = inning.get('team', '')
                overs = inning.get('overs', [])

                for over_data in overs:
                    over_num = over_data.get('over', 0)
                    balls = over_data.get('deliveries', [])

                    for ball_num, ball in enumerate(balls, 1):
                        batsman = ball.get('batter', '')
                        bowler = ball.get('bowler', '')

                        runs = ball.get('runs', {})
                        batsman_runs = runs.get('batter', 0)
                        extra_runs = runs.get('extras', 0)

                        # Wicket check
                        wickets = ball.get('wickets', [])
                        is_wicket = len(wickets) > 0
                        wicket_type = ''
                        if wickets:
                            wicket_type = wickets[0].get('kind', '')

                        deliveries.append({
                            'match_id': match_id,
                            'inning': inning_num,
                            'batting_team': batting_team,
                            'bowling_team': team2 if batting_team == team1 else team1,
                            'over_num': over_num,
                            'ball_num': ball_num,
                            'batsman': batsman,
                            'bowler': bowler,
                            'runs_scored': batsman_runs,
                            'extras': extra_runs,
                            'is_wicket': is_wicket,
                            'wicket_type': wicket_type
                        })

        except Exception as e:
            print(f"⚠️ Error in {json_file.name}: {e}")
            continue

        if (i+1) % 100 == 0:
            print(f"✅ {i+1}/{total} files processed...")

    # CSV save karo
    print("\n💾 CSV files save ho rahi hain...")

    matches_df = pd.DataFrame(matches)
    deliveries_df = pd.DataFrame(deliveries)

    matches_df.to_csv(f"{OUTPUT_FOLDER}/new_matches.csv", index=False)
    deliveries_df.to_csv(f"{OUTPUT_FOLDER}/new_deliveries.csv", index=False)

    print(f"✅ Total matches: {len(matches_df)}")
    print(f"✅ Total deliveries: {len(deliveries_df)}")
    print(f"✅ Seasons: {sorted(matches_df['season'].unique())}")
    print("\n🎉 Conversion complete!")

if __name__ == "__main__":
    convert_json_to_csv()