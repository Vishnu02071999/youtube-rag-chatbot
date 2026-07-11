# 🎥 YouTube RAG Chatbot — Frontend

A [Streamlit](https://streamlit.io/) chat UI for the [YouTube RAG Chatbot backend](#-related-backend). Paste a YouTube URL, index it, and chat with the video — powered by a FastAPI + LangChain + FAISS backend.

> ⚠️ **This repo contains the frontend only.** It's a client for a separate FastAPI backend. You'll need that backend running (locally or deployed) for this app to work. See [Related Backend](#-related-backend) below.

---

## ✨ Features

- **Paste & Index** — Drop in any YouTube URL and index its transcript with one click.
- **Transcript Fetching (client-side)** — Pulls the transcript directly via `youtube-transcript-api`, so the backend never needs to talk to YouTube itself.
- **Proxy Support** — Routes transcript fetches through [Webshare](https://www.webshare.io/) rotating residential proxies, since YouTube blocks most cloud-provider IPs (Streamlit Cloud, Render, AWS, GCP, etc.). Falls back to a direct connection when no proxy credentials are set (e.g. local development).
- **Chat Interface** — Streamlit's native chat components, with per-message timestamps showing where in the video the answer came from.
- **Session Handling** — A fresh session ID is generated per indexed video and on chat clear, keeping conversations isolated.
- **Custom Themed UI** — Dark, neon-accented custom styling (`styles.py`) layered on top of Streamlit's defaults.

---

## 🏗️ Project Structure

```
├── streamlit_app.py   # Main Streamlit app — layout, sidebar, chat loop
├── api.py             # Backend client — transcript fetching + HTTP calls to FastAPI backend
├── styles.py           # Custom CSS (dark theme, hero section, chat bubbles)
└── requirements.txt    # Python dependencies
```

**Flow:**
1. User pastes a YouTube URL in the sidebar and clicks **Index Video**.
2. `api.py` extracts the video ID, fetches the transcript client-side via `youtube-transcript-api` (optionally through a Webshare proxy), and `POST`s it to the backend's `/index` endpoint.
3. Once indexed, the user asks questions in the chat input — each question is sent to the backend's `/ask` endpoint along with a `session_id`, and the answer (plus optional timestamp) is rendered in the chat.
4. **Clear Chat** resets local messages and generates a new `session_id`, then calls the backend's `/clear-chat`.

---

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/) — UI framework
- [youtube-transcript-api](https://pypi.org/project/youtube-transcript-api/) — Fetches YouTube video transcripts
- [Webshare Proxy](https://www.webshare.io/) — Rotating residential proxies for transcript fetching from cloud environments
- [requests](https://docs.python-requests.org/) — HTTP client for talking to the backend API

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

3. **Configure secrets**

   Create a `.streamlit/secrets.toml` file in the project root:
   ```toml
   BACKEND_URL = "http://127.0.0.1:8000"

   # Optional — only needed if deploying to a cloud host where
   # YouTube blocks direct transcript requests
   WEBSHARE_PROXY_USERNAME = "your_webshare_username"
   WEBSHARE_PROXY_PASSWORD = "your_webshare_password"
   ```

   - `BACKEND_URL` defaults to `http://127.0.0.1:8000` if not set — fine for local development against a locally running backend.
   - `WEBSHARE_PROXY_USERNAME` / `WEBSHARE_PROXY_PASSWORD` are optional. Without them, transcript fetches go through a direct connection, which will likely fail on cloud-hosted deployments (Streamlit Cloud, Render, etc.) due to YouTube IP blocking.

---

## 🚀 Running the App

Make sure the [backend](#-related-backend) is running first, then:

```bash
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501`.

---

## 🖱️ Usage

1. Paste a YouTube video URL into the sidebar.
2. Click **📥 Index Video** — this fetches the transcript and sends it to the backend for embedding.
3. Once indexed, ask questions in the chat box at the bottom.
4. Answers appear with a **📍 timestamp** when the answer can be traced to a specific point in the video.
5. Click **🗑 Clear Chat** to reset the conversation (this does not require re-indexing the video).

---

## 🔗 Related Backend

This frontend expects a compatible FastAPI backend exposing:

- `POST /index` — accepts a transcript and builds a vector store
- `POST /ask` — accepts a question + `session_id`, returns an answer + optional timestamp
- `POST /clear-chat` — clears chat history for a `session_id`

Set `BACKEND_URL` in `secrets.toml` to point at wherever that backend is deployed.

---

## 📝 Notes

- The transcript is fetched **client-side, on this frontend**, not by the backend — the backend only receives already-fetched transcript data.
- Only English (`en`) transcripts are currently requested; videos without an English transcript will fail to index.
- Secrets (`BACKEND_URL`, Webshare credentials) are read via `st.secrets` and should never be hardcoded — use `.streamlit/secrets.toml` locally, and your hosting platform's secrets manager in production.
- `.streamlit/secrets.toml` should be excluded from version control (add it to `.gitignore`).

---

## 📄 License

This project is licensed under the MIT License.
