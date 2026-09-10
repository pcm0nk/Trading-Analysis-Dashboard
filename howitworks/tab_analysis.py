import streamlit as st
from howitworks.config import render_video_button


def render_tab_analysis():
    col_txt, col_btn = st.columns([0.72, 0.28], vertical_alignment="center")
    with col_txt:
        st.markdown("### 📈 Section 2: Trading Analysis Engine")
    with col_btn:
        render_video_button("analysis", "Watch Analysis Video")

    st.markdown(
        "* **📊 Executive Summary:** High-level metrics—Net Realized PnL, Win Rate, Profit Factor, Open/Close Fees, Equity Curves, and Drawdown.\n"
        "* **🎯 Pair Performance:** Per-pair vs. total performance breakdowns with PnL, fee analysis, and visual charts.\n"
        "* **⏰ Session Dynamics:** Trade count and win-rate distribution mapped across market sessions with visual charting.\n"
        "* **🔄 Session Transitions & Holds:** Tracks position entry/exit sessions, hold durations, and exit triggers (`TP`, `SL`, `Liquidation`).\n"
        "* **🔍 Audit & Trade Logs:** Detailed execution table featuring trade session tags and blown-account audit logging.\n"
        "* **⚙️ Session Settings & Risk:** Account parameters—Segment Start Capital, Ending Equity, Max Peak, Risk/Drawdown thresholds, and Max $/% Drawdown."
    )