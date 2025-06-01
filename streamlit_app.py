import streamlit as st
import pandas as pd
from jinja2 import Environment, FileSystemLoader

# Load data
url = "https://raw.githubusercontent.com/AlexMarinRemus/scouting-app/main/Romanian-Superliga-24-25.xlsx"
df = pd.read_excel(url, engine='openpyxl')

# Data cleaning and filtering
df['Birthday'] = pd.to_datetime(df['Birthday'], errors='coerce')
filtered_df = df[(df['Minutes played'] >= 600) & (df['Goals'] > 3)]
filtered_df['xG per shot per 90'] = filtered_df.apply(
    lambda row: row['xG per 90'] / row['Shots per 90'] if row['Shots per 90'] > 0 else 0,
    axis=1
)

# Select relevant columns
players_of_interest = ['L. Munteanu', 'D. Alibec']
compare_df = filtered_df[filtered_df['Full name'].isin(players_of_interest)][
    ['Full name', 'Birthday', 'Minutes played', 'xG per shot per 90', 'Aerial duels won, %', 'Goals', 'Shots per 90', 'xG per 90']
]

if compare_df.shape[0] < 2:
    st.error("Could not find both players in the dataset.")
else:
    # Prepare data as a dict for the template
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

    # Load template
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('template.html')

    # Render HTML
    rendered_html = template.render(player1=players_of_interest[0], player2=players_of_interest[1], data=data)

    st.title("Player Comparison: L. Munteanu vs D. Alibec")
    st.components.v1.html(rendered_html, height=400, scrolling=True)
