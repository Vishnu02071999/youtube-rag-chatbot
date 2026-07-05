from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import traceback
from indexing import YouTubeIndexer
from chatbot import YouTubeChatbot

# -----------------------------------------
# Create FastAPI App
# -----------------------------------------

app = FastAPI(
    title="YouTube Chatbot API",
    description="RAG-based chatbot for YouTube videos",
    version="1.0.0"
)

# -----------------------------------------
# Backend Services
# -----------------------------------------

indexer = YouTubeIndexer()
chatbot = None


# -----------------------------------------
# Request Models
# -----------------------------------------

class TranscriptChunk(BaseModel):
    text: str
    start: float
    duration: float


class VideoRequest(BaseModel):
    transcript: list[TranscriptChunk]


class QuestionRequest(BaseModel):
    question: str
    session_id: str


class ClearChatRequest(BaseModel):
    session_id: str


# -----------------------------------------
# Health Check
# -----------------------------------------

@app.get("/")
def root():
    return {
        "message": "YouTube Chatbot API is running 🚀"
    }


# -----------------------------------------
# Index Video
# -----------------------------------------

@app.post("/index")
def index_video(request: VideoRequest):

    global chatbot

    try:

        # Convert Pydantic models to dictionaries
        transcript = [
            chunk.model_dump()
            for chunk in request.transcript
        ]

        # Create FAISS Vector Store
        indexer.index_video(transcript)

        # Reload chatbot
        chatbot = YouTubeChatbot()

        # Clear previous chat
        chatbot.clear_chat()

        return {
            "status": "success",
            "message": "Video indexed successfully."
        }

    except Exception as e:
        raise HTTPException(
        status_code=500,
        detail=str(e)
    )


# -----------------------------------------
# Ask Questions
# -----------------------------------------

@app.post("/ask")
def ask_question(request: QuestionRequest):

    global chatbot

    if chatbot is None:

        raise HTTPException(
            status_code=400,
            detail="Please index a video first."
        )

    try:

        response = chatbot.ask(
            request.question,
            request.session_id
        )

        return {
            "question": request.question,
            "answer": response["answer"],
            "timestamp": response["timestamp"]
        }

    except Exception as e:
        print("\n" + "=" * 80)
        traceback.print_exc()
        print("=" * 80 + "\n")

        raise HTTPException(
        status_code=500,
        detail=str(e)
    )


# -----------------------------------------
# Clear Chat
# -----------------------------------------

@app.post("/clear-chat")
def clear_chat(request: ClearChatRequest):

    global chatbot

    if chatbot is None:

        raise HTTPException(
            status_code=400,
            detail="Please index a video first."
        )

    chatbot.clear_chat(request.session_id)

    return {
        "status": "success",
        "message": "Chat history cleared."
    }