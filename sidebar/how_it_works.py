import streamlit as st
from howitworks.config import render_video_button
from howitworks.tab_data import render_tab_data
from howitworks.tab_capital import render_tab_capital
from howitworks.tab_validation import render_tab_validation
from howitworks.tab_analysis import render_tab_analysis
from howitworks.tab_ml import render_tab_ml


def show_how_it_works_dialog():
    """
    Renders the modal dialog explaining dashboard features by combining
    modularized tab views from howitworks/.
    """
    @st.dialog("📖 Dashboard Walkthrough & Documentation", width="large")
    def _render_dialog():
        col_intro_txt, col_intro_btn = st.columns([0.72, 0.28], vertical_alignment="center")
        with col_intro_txt:
            st.markdown(
                "Welcome to the **Quantitative Trading & Diagnostic Suite**! This guide"
                " explains data ingestion, fuzzy column matching, accepted direction variants, sample downloads, and"
                " system usage."
            )
        with col_intro_btn:
            render_video_button("intro", "Overview Video")

        st.markdown("---")

        # Tabbed view inside the modal
        doc_tab1, doc_tab2, doc_tab3, doc_tab4, doc_tab5 = st.tabs([
            "📂 1. Data Requirements",
            "💰 2. Capital Control",
            "🛡️ 3. Section 1: Validation",
            "📈 4. Section 2: Trading Analysis",
            "🤖 5. Section 3: Machine Learning Engine"
        ])

        with doc_tab1:
            render_tab_data()

        with doc_tab2:
            render_tab_capital()

        with doc_tab3:
            render_tab_validation()

        with doc_tab4:
            render_tab_analysis()

        with doc_tab5:
            render_tab_ml()

        st.markdown("---")

    _render_dialog()


def render_how_it_works_button():
    """
    Renders the sidebar button to trigger the walkthrough modal.
    """
    if st.sidebar.button("📖 How it Works", use_container_width=True):
        st.session_state.show_walkthrough_modal = True

    if st.session_state.get("show_walkthrough_modal", False):
        st.session_state.show_walkthrough_modal = False
        show_how_it_works_dialog()