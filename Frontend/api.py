import re
import requests
from youtube_transcript_api import YouTubeTranscriptApi

# ================================
# Backend URL
# ================================

BACKEND_URL = "http://127.0.0.1:8000"


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
    Fetch transcript locally and send it to the backend.
    """

    video_id = extract_video_id(url)

    api = YouTubeTranscriptApi()

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