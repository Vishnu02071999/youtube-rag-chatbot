import re
import requests
import streamlit as st

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig

# ================================
# Backend URL
# ================================

# Read from Streamlit secrets when deployed; fall back to localhost
# for local development where no secrets.toml is set up.
BACKEND_URL = st.secrets.get("BACKEND_URL", "http://127.0.0.1:8000")


# ================================
# Webshare Proxy Config
# ================================

# YouTube blocks most requests coming from cloud-provider IPs
# (Streamlit Cloud, Render, AWS, GCP, etc.), so transcript fetches
# are routed through Webshare's rotating residential proxies instead.
# Credentials come from Streamlit secrets, never hardcoded.

_proxy_username = st.secrets.get("WEBSHARE_PROXY_USERNAME")
_proxy_password = st.secrets.get("WEBSHARE_PROXY_PASSWORD")

if _proxy_username and _proxy_password:
    _proxy_config = WebshareProxyConfig(
        proxy_username=_proxy_username,
        proxy_password=_proxy_password,
    )
else:
    # No proxy configured (e.g. running locally) — fall back to a
    # direct connection. This will likely fail if later deployed
    # to a cloud IP without proxy credentials set.
    _proxy_config = None


# ================================
# Extract Video ID
# ================================

def extract_video_id(url: str) -> str:
    """
    Extracts the YouTube video ID from various YouTube URL formats.
    """

    patterns = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11})",
        r"youtu\.be\/([0-9A-Za-z_-]{11})",
    ]

    for pattern in patterns:
        match = re.search(pattern, url)

        if match:
            return match.group(1)

    raise ValueError("Invalid YouTube URL")


# ================================
# Index Video
# ================================

def index_video(url: str):
    """
    Fetch transcript locally (via Webshare proxy, if configured)
    and send it to the backend.
    """

    video_id = extract_video_id(url)

    api = YouTubeTranscriptApi(proxy_config=_proxy_config)

    transcript = api.fetch(
        video_id,
        languages=["en"]
    )

    transcript_data = []

    for chunk in transcript:

        transcript_data.append(
            {
                "text": chunk.text,
                "start": chunk.start,
                "duration": chunk.duration
            }
        )

    response = requests.post(
        f"{BACKEND_URL}/index",
        json={
            "transcript": transcript_data
        },
        timeout=120
    )

    response.raise_for_status()

    return response.json()


# ================================
# Ask Question
# ================================

def ask_question(question: str, session_id: str):

    response = requests.post(
        f"{BACKEND_URL}/ask",
        json={
            "question": question,
            "session_id": session_id
        },
        timeout=120
    )

    response.raise_for_status()

    return response.json()


# ================================
# Clear Chat
# ================================

def clear_chat(session_id: str):

    response = requests.post(
        f"{BACKEND_URL}/clear-chat",
        json={
            "session_id": session_id
        },
        timeout=60
    )

    response.raise_for_status()

    return response.json()
