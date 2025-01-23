import streamlit as st
import streamlit.components.v1 as components

# Load the updated HTML template
with open("templates/index.html", "r") as f:
    html_content = f.read()

# Render the custom HTML in Streamlit
components.html(html_content, height=600)

# Sidebar for additional information
st.sidebar.title("About")
st.sidebar.info("This is a football-themed login page. Customize it to integrate with your app!")
