import os
import requests
import streamlit as st


# ================================
# Backend URL
# ================================

# During local development:
# BACKEND_URL=http://127.0.0.1:8000

# During deployment:
# Add BACKEND_URL inside Streamlit Secrets.

BACKEND_URL = st.secrets.get(
    "BACKEND_URL",
    os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
)


# ================================
# Index Video
# ================================

def index_video(url: str):

    response = requests.post(
        f"{BACKEND_URL}/index",
        json={
            "url": url
        }
    )

    response.raise_for_status()

    return response.json()


# ================================
# Ask Question
# ================================

def ask_question(question, session_id):

    response = requests.post(
        f"{BACKEND_URL}/ask",
        json={
    "question": question,
    "session_id": session_id
}
    )

    response.raise_for_status()

    return response.json()


# ================================
# Clear Chat
# ================================

def clear_chat(session_id):

    response = requests.post(
    f"{BACKEND_URL}/clear-chat",
    json={
        "session_id": session_id
    }
)

    response.raise_for_status()

    return response.json()