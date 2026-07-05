from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from indexing import YouTubeIndexer
from chatbot import YouTubeChatbot

# Create FastAPI app
app = FastAPI(
    title="YouTube Chatbot API",
    description="RAG-based chatbot for YouTube videos",
    version="1.0.0"
)

# Initialize backend services
indexer = YouTubeIndexer()
chatbot = None


# ----------------------------
# Request Models
# ----------------------------

class VideoRequest(BaseModel):
    url: str


class QuestionRequest(BaseModel):
    question: str
    session_id: str


class ClearChatRequest(BaseModel):
    session_id: str


# ----------------------------
# Health Check
# ----------------------------

@app.get("/")
def home():
    return {
        "message": "Welcome to the YouTube Chatbot API!"
    }

@app.get("/")
def root():
    return {
        "message": "YouTube Chatbot API is running 🚀"
    }

# ----------------------------
# Index a YouTube Video
# ----------------------------

@app.post("/index")
def index_video(request: VideoRequest):

    global chatbot

    try:

        indexer.index_video(request.url)

        # Reload chatbot with newly created vector store
        chatbot = YouTubeChatbot()
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


# ----------------------------
# Ask Questions
# ----------------------------

@app.post("/ask")
def ask_question(request: QuestionRequest):

    global chatbot

    if chatbot is None:

        raise HTTPException(
            status_code=400,
            detail="Please index a YouTube video first."
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

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

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