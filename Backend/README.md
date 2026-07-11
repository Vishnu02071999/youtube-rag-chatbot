# 🎥 YouTube RAG Chatbot — Backend

A Retrieval-Augmented Generation (RAG) backend that lets you **chat with any YouTube video** using its transcript. Built with **FastAPI**, **LangChain**, **FAISS**, and **OpenAI**.

Send in a video's transcript, then ask questions about its content via a REST API — get context-aware answers with timestamps, conversational memory, and whole-video summaries.

> ⚠️ **This repo contains the backend only.** It exposes a REST API and does not include a UI or transcript-fetching logic. You'll need a frontend (or a script) to pull a video's transcript (e.g. via [`youtube-transcript-api`](https://pypi.org/project/youtube-transcript-api/)) and call the endpoints below.

---

## ✨ Features

- **Transcript Indexing** — Converts a YouTube transcript into a searchable FAISS vector store.
- **Conversational RAG** — Ask follow-up questions with full chat history awareness (history-aware query rewriting).
- **Timestamped Answers** — Returns the approximate `MM:SS` timestamp where the answer was found in the video.
- **Whole-Video Summarization** — Detects summary-style questions ("summarize this", "what's this video about") and uses a map-reduce approach over the full transcript instead of relying on limited chunk retrieval.
- **Session-based Chat History** — Multiple chat sessions supported, with the ability to clear history per session.
- **Simple REST API** — Built with FastAPI so any frontend (web app, browser extension, CLI, etc.) can integrate with it.

---

## 🏗️ Architecture

```
├── app.py         # FastAPI application & API routes
├── chatbot.py      # RAG conversational chain & summarization logic
├── indexing.py     # Transcript chunking & FAISS vector store creation
```

**Flow:**
1. A transcript (fetched externally — this backend does not fetch transcripts itself) is sent to `/index`, which splits it into chunks and stores embeddings in a local FAISS vector store.
2. Questions sent to `/ask` are either:
   - Routed to a **history-aware retrieval chain** (for specific/factual questions), which retrieves chunks using **MMR search** (`k=6`, `fetch_k=20`) to balance relevance with diversity across retrieved chunks, or
   - Routed to a **map-reduce summarizer** (for whole-video overview questions).
3. Chat history is preserved per `session_id` and can be cleared via `/clear-chat`.

---

## 🛠️ Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) — API layer
- [LangChain](https://www.langchain.com/) — RAG orchestration
- [FAISS](https://github.com/facebookresearch/faiss) — Vector store, queried via **MMR (Maximal Marginal Relevance)** retrieval for relevant *and* diverse chunks
- [OpenAI](https://platform.openai.com/) — Embeddings (`text-embedding`) & chat completions (`gpt-4o-mini`)

---

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-name>
   ```

2. **Create a virtual environment and install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up environment variables**

   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

---

## 🚀 Running the App

Start the FastAPI server:

```bash
uvicorn app:app --reload
```

The API will be available at `http://127.0.0.1:8000`.
Interactive API docs (Swagger UI) at `http://127.0.0.1:8000/docs`.

---

## 🔗 Getting a Transcript to Index

Since this backend doesn't fetch transcripts itself, you'll need to obtain one first. A common approach using [`youtube-transcript-api`](https://pypi.org/project/youtube-transcript-api/):

```python
from youtube_transcript_api import YouTubeTranscriptApi

transcript = YouTubeTranscriptApi.get_transcript("VIDEO_ID")
# transcript is a list of {"text": ..., "start": ..., "duration": ...} dicts
# — matches the shape expected by POST /index
```

Then POST that list directly to `/index` (see below).

---

## 📡 API Endpoints

### `GET /`
Health check.

**Response**
```json
{ "message": "YouTube Chatbot API is running 🚀" }
```

---

### `POST /index`
Index a video transcript into the vector store.

**Request Body**
```json
{
  "transcript": [
    { "text": "Welcome to this video...", "start": 0.0, "duration": 3.5 },
    { "text": "Today we'll talk about...", "start": 3.5, "duration": 4.2 }
  ]
}
```

**Response**
```json
{ "status": "success", "message": "Video indexed successfully." }
```

---

### `POST /ask`
Ask a question about the indexed video.

**Request Body**
```json
{
  "question": "What is the main topic of this video?",
  "session_id": "user123"
}
```

**Response**
```json
{
  "question": "What is the main topic of this video?",
  "answer": "The video discusses...",
  "timestamp": "02:15"
}
```

> `timestamp` will be `null` for whole-video summary questions.

---

### `POST /clear-chat`
Clear chat history for a given session.

**Request Body**
```json
{ "session_id": "user123" }
```

**Response**
```json
{ "status": "success", "message": "Chat history cleared." }
```

---

## 💬 CLI Mode

You can also chat with an indexed video directly from the terminal:

```bash
python chatbot.py
```

Type your questions, and `exit` to quit.

---

## 📝 Notes

- This is a **backend-only** service — no frontend, transcript fetcher, or persistent database is included.
- The vector store is persisted locally in the `vectorstore/` directory (FAISS index + full transcript text).
- Re-indexing a new video will overwrite the existing vector store and reset chat history.
- Summary-style questions are detected via keyword matching (e.g. "summarize", "overview", "main points") and bypass standard retrieval in favor of a map-reduce summarization pipeline over the entire transcript.
- Only one video is indexed at a time — indexing a new video overwrites the previous vector store rather than supporting multiple videos concurrently.

---

## 📄 License

This project is licensed under the MIT License.
