import streamlit as st
from howitworks.config import render_video_button


def render_tab_ml():
    col_txt, col_btn = st.columns([0.72, 0.28], vertical_alignment="center")
    with col_txt:
        st.markdown("### 🤖 Section 3: Machine Learning Engine")
    with col_btn:
        render_video_button("ml", "Watch ML Video")

    st.markdown(
        "Advanced diagnostic analytics powered by `scikit-learn` for behavioral pattern recognition:"
    )
    
    st.markdown("---")
    
    st.markdown("#### 🌲 Tab 1: Feature Importance & Predictive Drivers")
    st.markdown(
        "* **Random Forest Classifier:** Supervised model identifying key trade drivers (e.g., duration, sizing, session, direction) predicting win/loss outcomes.\n"
        "* **Cross-Validation Accuracy:** Stratified K-Fold validation score measuring model predictive reliability without overfitting.\n"
        "* **Gini Importance Weights:** Feature influence ranking chart displaying key factors impacting overall trade equity."
    )

    st.markdown("---")

    st.markdown("#### 🎯 Tab 2: Trade Archetype Clustering")
    st.markdown(
        "* **K-Means Unsupervised Clustering:** Groups executions into distinct behavioral archetypes based on risk profile, duration, and position size.\n"
        "* **Profile Segments:** Identifies trade patterns like *Quick Scalps*, *Overleveraged Holds*, or *Session Drift Trades*.\n"
        "* **Segment Performance Metrics:** Breakdown of net PnL, win probability, and total fee impact per behavior cluster."
    )

    st.markdown("---")

    st.markdown("#### 📊 Tab 3: Behavioral Edge Diagnostics")
    st.markdown(
        "* **Chronological Session Matrix:** Win probability heatmap mapped across market sessions.\n"
        "* **Hold-Time Edge Decay:** Expected value trajectory tracking hold duration vs. trade profitability decay.\n"
        "* **Sizing Risk Dispersion:** Position size scaling analysis vs. outcome distribution."
    )