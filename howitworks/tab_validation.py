import pandas as pd
import streamlit as st
from howitworks.config import render_video_button


def render_tab_validation():
    col_txt, col_btn = st.columns([0.72, 0.28], vertical_alignment="center")
    with col_txt:
        st.markdown("### 🛡️ Section 1: Validation & FIFO Reconstruction Phase")
    with col_btn:
        render_video_button("validation", "Watch FIFO Video")

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