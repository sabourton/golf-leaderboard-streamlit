import requests
import pandas as pd
import streamlit as st

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

    # Ensure playerEU in df_leaderboard is a string
    df_leaderboard['playerEU'] = df_leaderboard['playerEU'].astype(str)

    # Player input data as a dictionary
    player_input = {
        "36489": "Jonny", "1941": "Georgia", "40915": "Norah", "34737": "Katie", "41218": "Sarah D",
        "37979": "Ste", "40502": "Georgia", "38194": "Phoebe", "41757": "Rachel", "33932": "Rory",
        "42599": "Aida", "41763": "Ollie", "41208": "Marc", "36198": "Ollie", "39359": "Sarah D",
        "38783": "Sarah P", "43410": "Ste", "40378": "Evie", "3467": "Jonny", "37537": "Jonny",
        "31575": "Matt", "36883": "Matt", "42143": "Norah", "39309": "Phoebe", "39523": "Rachel",
        "40623": "Ste", "42154": "Ste", "35918": "Amelia", "37624": "Emily", "38796": "Emily",
        "40327": "Evie", "41282": "Evie", "293": "Georgia", "37051": "Marc", "39543": "Matt",
        "39791": "Matt", "36519": "Phoebe", "41288": "Aida", "43406": "Emily", "35122": "Georgia",
        "39968": "Jonny", "40336": "Jonny", "41684": "Katie", "36199": "Marc", "37405": "Marc",
        "34788": "Matt", "38780": "Ollie", "39594": "Phoebe", "101241": "Rachel", "41824": "Rachel",
        "42144": "Rory", "39035": "Sarah D", "42481": "Sarah P", "39583": "Aida", "41227": "Amelia",
        "39887": "Amelia", "30717": "Evie", "40946": "Georgia", "100020": "Katie", "38868": "Katie",
        "43333": "Marc", "38035": "Norah", "4660": "Norah", "42694": "Norah", "39617": "Ollie",
        "100019": "Ollie", "105456": "Phoebe", "9118": "Rachel", "41312": "Sarah P", "39187": "Sarah P",
        "39358": "Ste", "42474": "Amelia", "5889": "Emily", "1402": "Evie", "36218": "Jonny",
        "36867": "Matt", "39271": "Ollie", "39474": "Ste", "101732": "Rachel"
    }

    # Convert player input data to DataFrame
    df_player_input = pd.DataFrame(list(player_input.items()), columns=['playerEU', 'Name'])

    # Ensure playerEU in df_player_input is a string
    df_player_input['playerEU'] = df_player_input['playerEU'].astype(str)

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

    # Streamlit Dashboard
    st.title("Golf Tournament Leaderboard")

    # Highlight the leader
    leader = df_final[df_final['pos'] == 1]
    if not leader.empty:
        leader_name = leader.iloc[0]['name']
        leader_playername = leader.iloc[0]['playername']
        st.subheader(f"Leader: {leader_name} ({leader_playername})")
        st.markdown("### Leader Details")
        st.dataframe(leader)

    # Display the entire leaderboard
    st.markdown("### Full Leaderboard")
    st.dataframe(df_final)

    # Visualize leaderboard
    st.markdown("### Leaderboard Positions")
    st.bar_chart(df_final.set_index('name')['total'])

    # Save the final dataset to Excel
    output_excel = "final_leaderboard_auto_fitted.xlsx"
    df_final.to_excel(output_excel, index=False)

    st.markdown("### Download the Leaderboard")
    with open(output_excel, "rb") as file:
        btn = st.download_button(
            label="Download Excel",
            data=file,
            file_name=output_excel,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

else:
    st.error(f"Failed to fetch data. Status code: {response.status_code}")
