import streamlit as st
import pandas as pd
from jinja2 import Environment, FileSystemLoader

# Load data from GitHub raw URL
url = "https://raw.githubusercontent.com/AlexMarinRemus/scouting-app/main/Romanian-Superliga-24-25.xlsx"
df = pd.read_excel(url, engine='openpyxl')

# Data cleaning and filtering
df['Birthday'] = pd.to_datetime(df['Birthday'], errors='coerce')
filtered_df = df[(df['Minutes played'] >= 600)]
filtered_df['xG per shot per 90'] = filtered_df.apply(
    lambda row: row['xG per 90'] / row['Shots per 90'] if row['Shots per 90'] > 0 else 0,
    axis=1
)

# Relevant columns to show
cols = ['Full name', 'Birthday', 'Minutes played', 'Goals', 'Shots per 90', 'xG per 90', 'xG per shot per 90', 'Aerial duels won, %']

# List of players for dropdowns
players = filtered_df['Full name'].unique().tolist()

st.title("Compare Two Players")

# Find indexes of default players (fall back to 0 or 1 if not found)
default_player1 = "L. Munteanu"
default_player2 = "D. Alibec"

index1 = players.index(default_player1) if default_player1 in players else 0
index2 = players.index(default_player2) if default_player2 in players else 1

col1, col2 = st.columns(2)

with col1:
    player1 = st.selectbox("Select Player 1:", players, index=index1)

with col2:
    player2 = st.selectbox("Select Player 2:", players, index=index2)

if player1 == player2:
    st.warning("Please select two different players to compare.")
else:
    # Filter dataframe for these two players
    compare_df = filtered_df[filtered_df['Full name'].isin([player1, player2])][cols]

    # Prepare data dict for the template
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

    # Render HTML with Jinja2 template
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('templates/index.html')

    rendered_html = template.render(player1=player1, player2=player2, data=data)

    st.components.v1.html(rendered_html, height=400, scrolling=True)
