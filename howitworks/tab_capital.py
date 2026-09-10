import streamlit as st
from howitworks.config import render_video_button


def render_tab_capital():
    col_txt, col_btn = st.columns([0.72, 0.28], vertical_alignment="center")
    with col_txt:
        st.markdown("### 💰 Capital & Segment Control Ledger")
    with col_btn:
        render_video_button("capital", "Watch Capital Video")

    st.markdown(
        "* **Row 1 (Baseline Starting Capital):** Auto-set to the earliest trade date with a $10 baseline.\n"
        "* **Row 2+ (Top-Ups):** Add rows to simulate capital injections (e.g., $10 on `2026-04-17`), creating new analysis **Segments**.\n"
        '* **Active Segment Selector:** Defaults to **"All Segments Combined View"** for overall lifecycle analysis.'
    )