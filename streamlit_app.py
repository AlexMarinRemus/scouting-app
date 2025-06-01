import streamlit as st
import pandas as pd
from jinja2 import Environment, FileSystemLoader

# Load data from GitHub raw URL
url = "https://raw.githubusercontent.com/AlexMarinRemus/scouting-app/main/Romanian-Superliga-24-25.xlsx"
df = pd.read_excel(url, engine='openpyxl')

# Data cleaning and filtering
df['Birthday'] = pd.to_datetime(df['Birthday'], errors='coerce')
filtered_df = df[(df['Minutes played'] >= 600) & (df['Goals'] > 3)]
filtered_df['xG per shot per 90'] = filtered_df.apply(
    lambda row: row['xG per 90'] / row['Shots per 90'] if row['Shots per 90'] > 0 else 0,
    axis=1
)

# Relevant columns
cols = ['Full name', 'Birthday', 'Minutes played', 'Goals', 'Shots per 90', 'xG per 90', 'xG per shot per 90', 'Aerial duels won, %']

# Fix player to compare against
fixed_player = "Louis Munteanu"

# Get list of all players except the fixed one
all_players = filtered_df['Full name'].unique().tolist()
if fixed_player in all_players:
    all_players.remove(fixed_player)

st.title("Compare Player to L. Munteanu")

# User selects player from dropdown
selected_player = st.selectbox("Select a player to compare:", all_players)

# Filter data for the two players
compare_df = filtered_df[filtered_df['Full name'].isin([fixed_player, selected_player])][cols]

if compare_df.shape[0] < 2:
    st.error("Could not find both players in the dataset.")
else:
    data = {}
    for _, row in compare_df.iterrows():
        data[row['Full name']] = {
            'Birthday': row['Birthday'].strftime('%Y-%m-%d') if pd.notnull(row['Birthday']) else 'N/A',
            'Minutes played': int(row['Minutes played']),
            'Goals': int(row['Goals']),
            'Shots per 90': round(row['Shots per 90'], 2),
            'xG per 90': round(row['xG per 90'], 2),
            'xG per shot per 90': round(row['xG per shot per 90'], 4),
            'Aerial duels won, %': round(row['Aerial duels won, %'], 2)
        }

    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('index.html')

    rendered_html = template.render(player1=fixed_player, player2=selected_player, data=data)

    st.components.v1.html(rendered_html, height=400, scrolling=True)