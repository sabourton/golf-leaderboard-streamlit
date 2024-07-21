import requests
import pandas as pd

# Define the API URL
api_url = "https://www.golfpost.com/web-api/tournaments/2022628/leaderboard"

# Fetch data from the API
response = requests.get(api_url)

if response.status_code == 200:
    data = response.json()

    # Extract the leaderboard references
    leaderboard_refs = data.get('objects', {}).get('result', {}).get('data', [])

    # Extract the entities
    entities = data.get('entities', {})

    # Collect leaderboard data
    leaderboard_data = []
    for ref in leaderboard_refs:
        entry = entities.get(ref, {})
        if entry:
            leaderboard_data.append(entry)

    # Convert to DataFrame
    df_leaderboard = pd.json_normalize(leaderboard_data)

    # Load player input data
    df_player_input = pd.read_excel('player_input.xlsx')

    # Merge leaderboard data with player input data based on playerEU
    df_final = pd.merge(df_leaderboard, df_player_input, how='left', left_on='playerEU', right_on='playerEU')

    # Select and reorder the required fields
    required_fields = [
        'playerEU', 'playerName', 'Name', 'playerNationality', 'pos', 'ttp',
        'currentHole', 'topar', 'today', 'round1', 'round2', 'round3', 'round4',
        'total', 'playerNationalityFlagUrl'
    ]
    df_final = df_final[required_fields]

    # Rename columns to match requested names
    df_final.columns = [
        'playerEU', 'playername', 'name', 'playernationality', 'pos', 'ttp',
        'currenthole', 'topar', 'today', 'round1', 'round2', 'round3', 'round4',
        'total', 'nationalityflagurl'
    ]

    # Save the final dataset to Excel
    df_final.to_excel("final_leaderboard.xlsx", index=False)

    print("Data has been successfully saved to final_leaderboard.xlsx")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
