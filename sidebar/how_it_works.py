import os
import pandas as pd
import streamlit as st

# Path to standard dummy dataset at root
STANDARD_DUMMY_PATH = "dummydata.csv"

def show_how_it_works_dialog():
    """
    Renders the modal dialog explaining dashboard features, dataset choices,
    accepted direction variants, sample downloads, capital control, validation,
    and analytics/ML tabs.
    """
    @st.dialog("📖 Dashboard Walkthrough & Documentation", width="large")
    def _render_dialog():
        st.markdown(
            "Welcome to the **Quantitative Trading & Diagnostic Suite**! This guide"
            " explains data formatting, accepted directions, sample downloads, and"
            " system usage."
        )

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
            st.markdown("### 📂 Data Ingestion & Accepted Schema")
            st.markdown(
                "Custom CSV/Excel logs (`.csv`, `.xlsx`) must align with the core"
                " schema below:"
            )

            # Updated Schema Table with exact mandatory headers and accepted variants
            schema_data = {
                "Column Name": [
                    "Filled time(UTC)", 
                    "Futures", 
                    "Direction", 
                    "Filled Quantity", 
                    "Filled Price", 
                    "Realized PNL", 
                    "fees"
                ],
                "Accepted Variants": [
                    "Filled time(UTC)",
                    "Futures",
                    "OPEN_LONG, OPEN_SHORT, OPEN LONG, OPEN SHORT, BUY, LONG, Open Long, Open Short, CLOSE_LONG, CLOSE_SHORT, CLOSE LONG, CLOSE SHORT, BURST_LIQUIDATE_LONG, BURST_LIQUIDATE_SHORT, OFFSET_LIQUIDATE_SHORT, FORCE_LIQUIDATE_SHORT, FORCE_LIQUIDATE_LONG, OFFSET_LIQUIDATE_LONG, SELL, SHORT, Close Long, Close Short",
                    "Filled Quantity",
                    "Filled Price",
                    "Realized PNL",
                    "fees"
                ],
                "Example": [
                    "2026-04-10 14:30:00",
                    "BTCUSDT",
                    "OPEN_LONG",
                    "0.15",
                    "65400.50",
                    "150.00",
                    "0.0025"
                ]
            }
            st.table(pd.DataFrame(schema_data))
            st.warning(
                "⚠️ **Important:** Column headers in your uploaded CSV/Excel file must match"
                " the exact casing and spelling shown in the table above (e.g.,"
                " `Filled time(UTC)`, `Futures`, `Realized PNL`). Column matching is"
                " **case-sensitive**."
            )
            st.markdown("---")
            
            # Inline Download Section
            dl_col1, dl_col2 = st.columns([2, 1], vertical_alignment="center")

            with dl_col1:
                st.markdown(
                    "Download the standard sample CSV template to see the complete"
                    " expected column structure and date formatting before uploading custom"
                    " logs"
                )

            with dl_col2:
                if os.path.exists(STANDARD_DUMMY_PATH):
                    with open(STANDARD_DUMMY_PATH, "rb") as file:
                        st.download_button(
                            label="⬇️ Download Sample Template CSV",
                            data=file,
                            file_name="sample_trading_log_template.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                else:
                    st.caption("⚠️ `dummydata.csv` missing at root.")


        with doc_tab2:
            st.markdown("### 💰 Capital & Segment Control Ledger")
            st.markdown(
                "* **Row 1 (Baseline Starting Capital):** Auto-set to the earliest trade date with a $10 baseline.\n"
                "* **Row 2+ (Top-Ups):** Add rows to simulate capital injections (e.g., $10 on `2026-04-17`), creating new analysis **Segments**.\n"
                '* **Active Segment Selector:** Defaults to **"All Segments Combined View"** for overall lifecycle analysis.'
            )

        with doc_tab3:
            st.markdown("### 🛡️ Section 1: Validation & FIFO Reconstruction Phase")
            st.markdown(
                "When trading logs are exported from exchanges, they contain fragmented execution fills rather than completed trades. "
                "The **Validation Engine** executes pre-trade structural sanity checks, runs First-In-First-Out (FIFO) fill matching, "
                "merges scaled entries and partial take-profits into single position lifecycles, and flags execution anomalies."
            )

            st.markdown("---")

            st.markdown("#### 🔍 1. Pre-FIFO Raw Execution Sanity Checks")
            st.markdown(
                "Before processing order matching, raw logs pass through 5 automated data hygiene tests:\n\n"
                "* **Timestamp Order Check:** Audits fill timing for strict chronological sequence (`✅ PASS`). Automatically re-sorts out-of-order exports (`ℹ️ AUTO-FIX`).\n"
                "* **Trade Direction Check:** Validates order tags against exchange standards (`OPEN_LONG`, `CLOSE_SHORT`, `BURST_LIQUIDATE`, etc.).\n"
                "* **Quantity Sanity Check:** Verifies all execution quantities are strictly positive (`> 0`). Flags zero/negative fill sizes (`🚨 FAIL`).\n"
                "* **Price Sanity Check:** Audits price prints to ensure zero or negative values do not corrupt portfolio performance calculations (`🚨 FAIL`).\n"
                "* **Fill Balance Pre-Audit:** Audits opening vs. closing fill row counts per asset symbol. "
                "For example, an audit detail of `Open fills: 10, Close fills: 8` indicates active open inventory or unclosed positions."
            )

            st.markdown("---")

            st.markdown("#### ⚡ 2. FIFO Order Matching & Position Consolidation")
            st.markdown(
                "Raw execution fills are passed to the FIFO matching engine to resolve execution sub-fragments into full position lifecycles:\n\n"
                "* **Sub-Fill Matching:** Opening fills enter a symbol queue and are sequentially matched against closing fills on a First-In-First-Out basis.\n"
                "* **Proportional Fee & PnL Allocation:** Fees and realized PnL are allocated proportionally to exact matched quantities.\n"
                "* **Position Consolidation:** Contiguous fills in the same symbol and direction are consolidated into single position lifecycles with volume-weighted average entry/exit prices and exact total holding duration.\n"
                "* **Position Outcome Tagging:** Trades are classified as Take Profit (`TP`), Stop Loss (`SL`), Breakeven (`BE`), or `Liquidation`."
            )

            st.markdown("---")

            st.markdown("#### 🚨 3. Audit KPIs & Execution Anomalies")
            st.markdown(
                "* **Raw Fills Ingested:** Total raw execution rows imported from the raw exchange file.\n"
                "* **Matched Execution Fragments:** Number of matched sub-fill execution pieces.\n"
                "* **Consolidated Positions:** Number of full trade lifecycles built after merging micro-fills.\n"
                "* **Orphan Open (`Open Position Inventory`):** Unclosed trade inventory remaining active at the end of the dataset window.\n"
                "* **Orphan Close (`Unmatched Close Errors`):** Closing execution rows executed without a prior opening entry on record."
            )

            st.markdown("---")

            st.markdown("#### 📊 Key Summary Reference Table")
            
            summary_ref_data = {
                "Category": [
                    "Sanity Check", "Sanity Check", "Sanity Check", "Sanity Check", "Sanity Check",
                    "Audit Metric", "Audit Metric", "Audit Metric", "Anomaly", "Anomaly", "Anomaly"
                ],
                "Check / Metric Name": [
                    "Timestamp Order", "Trade Direction", "Quantity Sanity", "Price Sanity", "Fill Balance Pre-Audit",
                    "Matched Fragments", "Consolidated Positions", "CSV Exporter", "Orphan Open", "Orphan Close", "Orphan Close (Partial)"
                ],
                "Status / Details": [
                    "✅ PASS / ℹ️ AUTO-FIX", "✅ PASS / ⚠️ WARN", "✅ PASS / 🚨 FAIL", "✅ PASS / 🚨 FAIL", "✅ PASS / ℹ️ INFO",
                    "Count of matched sub-fills", "Count of merged full trades", "Downloadable CSV button", "Active position inventory", "Missing entry error", "Queue exhaustion"
                ],
                "Meaning / Impact": [
                    "Confirms chronological sequence; auto-sorts log if out of order.",
                    "Validates standard direction strings against accepted exchange tags.",
                    "Ensures all execution fill quantities are strictly positive.",
                    "Flags invalid zero or negative price prints in the dataset.",
                    "Compares open vs close fill row counts per pair (e.g. Open: 10, Close: 8).",
                    "Tracks total sub-fragment orders processed through the FIFO queue.",
                    "Represents true entry-to-flat position lifecycles for Phase 2 analytics.",
                    "Exports consolidated FIFO position records for external auditing.",
                    "Unclosed position inventory remaining at the end of the dataset window.",
                    "Closing execution row executed without a prior opening entry on record.",
                    "Closing fill size exceeded total open inventory available in the FIFO queue."
                ]
            }
            st.table(pd.DataFrame(summary_ref_data))

        with doc_tab4:
            st.markdown("### 📈 Section 2: Trading Analysis Engine")
            st.markdown(
                "* **📊 Executive Summary:** High-level metrics—Net Realized PnL, Win Rate, Profit Factor, Open/Close Fees, Equity Curves, and Drawdown.\n"
                "* **🎯 Pair Performance:** Per-pair vs. total performance breakdowns with PnL, fee analysis, and visual charts.\n"
                "* **⏰ Session Dynamics:** Trade count and win-rate distribution mapped across market sessions with visual charting.\n"
                "* **🔄 Session Transitions & Holds:** Tracks position entry/exit sessions, hold durations, and exit triggers (`TP`, `SL`, `Liquidation`).\n"
                "* **🔍 Audit & Trade Logs:** Detailed execution table featuring trade session tags and blown-account audit logging.\n"
                "* **⚙️ Session Settings & Risk:** Account parameters—Segment Start Capital, Ending Equity, Max Peak, Risk/Drawdown thresholds, and Max $/% Drawdown."
            )

        with doc_tab5:
            st.markdown("### 🤖 Section 3: Machine Learning Engine")
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
                "* **Chronological Session Matrix:** Win probability heatmap mapped across 6 market sessions (Sydney, Tokyo, Hong Kong, Frankfurt, London, New York).\n"
                "* **Hold-Time Edge Decay:** Expected value trajectory tracking hold duration vs. trade profitability decay.\n"
                "* **Sizing Risk Dispersion:** Position size scaling analysis vs. outcome distribution."
            )

        st.markdown("---")

    _render_dialog()


def render_how_it_works_button():
    """
    Renders the sidebar button to trigger the walkthrough modal.
    """
    if st.sidebar.button("📖 How It Works", use_container_width=True):
        st.session_state.show_walkthrough_modal = True

    if st.session_state.get("show_walkthrough_modal", False):
        st.session_state.show_walkthrough_modal = False
        show_how_it_works_dialog()