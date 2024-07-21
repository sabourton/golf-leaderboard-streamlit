import requests
import pandas as pd

# Define the API URL
api_url = "https://www.golfpost.com/web-api/tournaments/2022628/leaderboard"

# Fetch data from the API
response = requests.get(api_url)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()

    # Debug print to check the structure
    # print("Response JSON:", data)

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
    df = pd.json_normalize(leaderboard_data)

    # Save DataFrame to Excel
    df.to_excel("leaderboard.xlsx", index=False)

    print("Data has been successfully saved to leaderboard.xlsx")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
