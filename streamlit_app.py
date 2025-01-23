import streamlit as st

# Custom CSS for better styling
st.markdown(
    """
    <style>
    body {
        background-color: #f4f4f4;
        font-family: 'Arial', sans-serif;
    }
    .container {
        background: #ffffff;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        max-width: 600px;
        margin: auto;
        margin-top: 50px;
    }
    .title {
        text-align: center;
        color: #333333;
        font-size: 2rem;
    }
    .input-field {
        margin-top: 1.5rem;
        text-align: center;
    }
    .button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 1rem;
    }
    .button:hover {
        background-color: #45a049;
    }
    .greeting {
        margin-top: 1.5rem;
        text-align: center;
        color: #333333;
        font-size: 1.25rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# HTML structure
st.markdown(
    """
    <div class="container">
        <div class="title">🎈 My New App</div>
        <div class="input-field">
            <label for="name">What's your name?</label><br>
            <input id="name" type="text" class="text-box" placeholder="Enter your name" />
            <button id="submit-button" class="button">Submit</button>
        </div>
        <div id="greeting" class="greeting"></div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Custom JavaScript to handle interactivity
st.markdown(
    """
    <script>
    document.getElementById("submit-button").addEventListener("click", function() {
        const name = document.getElementById("name").value;
        const greeting = document.getElementById("greeting");
        if (name) {
            greeting.innerHTML = `Hello, ${name}! 🎉 Welcome to my app!`;
        } else {
            greeting.innerHTML = "Please enter your name!";
        }
    });
    </script>
    """,
    unsafe_allow_html=True,
)
