import uuid
import streamlit as st
from styles import load_css
from api import index_video, ask_question, clear_chat

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

st.set_page_config(
    page_title="YouTube Chatbot",
    page_icon="🎥",
    layout="wide",
)

st.markdown(load_css(), unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "video_indexed" not in st.session_state:
    st.session_state.video_indexed = False

# ---------------- Sidebar ---------------- #

with st.sidebar:

    st.markdown("<h2 style='text-align:center;'>🎥 YouTube Chatbot</h2>",
                unsafe_allow_html=True)

    youtube_url = st.text_input(
        "YouTube URL",
        placeholder="https://www.youtube.com/watch?v=..."
    )

    if st.button("📥 Index Video", use_container_width=True):

        if youtube_url.strip() == "":
            st.warning("Please enter a YouTube URL.")
        else:
            with st.spinner("Indexing video..."):
                try:
                    index_video(youtube_url)
                    st.session_state.video_indexed = True
                    st.session_state.messages = []
                    st.session_state.session_id = str(uuid.uuid4())
                    st.success("Video indexed successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to index video.\n\n{e}")

    if st.button("🗑 Clear Chat", use_container_width=True):

        try:
            clear_chat(
            st.session_state.session_id
             )
            st.session_state.messages = []
            st.session_state.session_id = str(uuid.uuid4())
            st.success("Chat cleared!")
        except Exception as e:
            st.error(str(e))

# ---------------- Hero ---------------- #
if not st.session_state.video_indexed:
    st.markdown("""
<div class="hero">

    <div class="hero-icon">
        🎥
    </div>

    <div class="hero-title">
        YOUTUBE CHATBOT
    </div>

    <div class="hero-subtitle">
        Chat with any YouTube video<br>
        using AI
    </div>

    <div class="hero-divider"></div>

</div>
""", unsafe_allow_html=True)

if not st.session_state.video_indexed:

    st.markdown("""
    <div class="welcome-card">

    <h3>👋 Welcome!</h3>

    Paste a YouTube URL in the sidebar.<br><br>

    Click <b>📥 Index Video</b>.<br><br>

    Then start asking questions about the video!

    </div>
    """, unsafe_allow_html=True)

# ---------------- Chat History ---------------- #

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant" and message.get("timestamp"):

            st.caption(f"📍 Mentioned around {message['timestamp']}")

# ---------------- Chat Input ---------------- #

if prompt := st.chat_input("Ask anything about the indexed video..."):

    if not st.session_state.video_indexed:

        st.warning("Please index a YouTube video first.")

    else:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                try:

                    response = ask_question(
                      prompt,
                      st.session_state.session_id
                    )

                    answer = response["answer"]

                    timestamp = response.get("timestamp")

                    st.markdown(answer)

                    if timestamp:
                        st.caption(f"📍 Mentioned around {timestamp}")

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer,
                            "timestamp": timestamp
                        }
                    )

                except Exception as e:

                    st.error(str(e))
