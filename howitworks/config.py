import streamlit as st

# Video Tutorial URLs (Set URL to None or "" to hide button)
VIDEO_TUTORIALS = {
    "intro": {
        "title": "🎬 Overview & Platform Walkthrough",
        "url": "https://www.youtube.com/watch?v=BfMqe8RlEzw&list=PLf4o7835wCCI&index=1"
    },
    "data": {
        "title": "📂 Data Ingestion & Schema Guide",
        "url": None  # Set URL here or leave None to hide
    },
    "capital": {
        "title": "💰 Capital Control & Ledger Guide",
        "url": None
    },
    "validation": {
        "title": "🛡️ Validation & FIFO Reconstruction Guide",
        "url": None
    },
    "analysis": {
        "title": "📈 Trading Analysis Engine Guide",
        "url": None
    },
    "ml": {
        "title": "🤖 Machine Learning Suite Guide",
        "url": None
    }
}


def render_video_button(video_key: str, default_label: str = "Watch Video"):
    """
    Renders an st.link_button only if a valid URL exists for the given video key.
    If the URL is None, empty, or a placeholder string, nothing is rendered.
    """
    video_info = VIDEO_TUTORIALS.get(video_key, {})
    url = video_info.get("url")

    if url and isinstance(url, str) and not url.startswith("https://www.youtube.com/watch?v=YOUR_"):
        st.link_button(f"▶️ {default_label}", url, use_container_width=True)