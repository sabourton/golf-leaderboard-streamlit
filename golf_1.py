import requests
import pandas as pd

# Define the API URL
api_url = "https://www.golfpost.com/web-api/tournaments/2022628/leaderboard"

# Fetch data from the API
response = requests.get(api_url)

# Check if the request was successful
if response.status_code == 200:

    data = response.json()

    # Print the entire data to debug
    print("Response JSON:", data)

    # Check if 'leaderboard' key exists
    if 'leaderboard' in data:
        # Flatten the JSON data and convert to DataFrame
        leaderboard = data['leaderboard']
        df = pd.json_normalize(leaderboard)

        # Save DataFrame to Excel
        df.to_excel("leaderboard.xlsx", index=False)

        print("Data has been successfully saved to leaderboard.xlsx")
    else:
        print("Key 'leaderboard' not found in the response.")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")