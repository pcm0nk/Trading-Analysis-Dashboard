import os
import pandas as pd
import streamlit as st
from howitworks.config import render_video_button

STANDARD_DUMMY_PATH = "dummydata.csv"


def render_tab_data():
    col_txt, col_btn = st.columns([0.72, 0.28], vertical_alignment="center")
    with col_txt:
        st.markdown("### 📂 Data Ingestion & Automated Schema Matching")
    with col_btn:
        render_video_button("data", "Watch Data Video")

    st.markdown(
        "The system features an **Automated Schema Engine (`RapidFuzz`)** that automatically detects exchange export formats "
        "(e.g., WEEX, Binance, Bybit, OKX) and maps column headers to our internal schema. "
        "You can upload custom CSV/Excel files (`.csv`, `.xlsx`) without manually reformatting your columns."
    )

    schema_data = {
        "Standard Name": [
            "fill_time", 
            "pair", 
            "direction", 
            "quantity", 
            "price", 
            "pnl", 
            "fees"
        ],
        "Accepted Variants & Fuzzy Matching Aliases": [
            "Filled time(UTC), fill time, time, created time, date, timestamp, trade time, order time, exec_time",
            "Futures, Symbol, Instrument, pair, market, contract, ticker, asset, product",
            "OPEN_LONG, OPEN_SHORT, BUY, SELL, LONG, SHORT, CLOSE_LONG, CLOSE_SHORT, BURST_LIQUIDATE, Side, Direction, Type, Action",
            "Filled Quantity, Amount, Qty, quantity, filled qty, size, filled amount, executed qty, exec_qty",
            "Filled Price, Price, avg price, executed price, fill price, avg_price, exec_price",
            "Realized PNL, PNL, realized pnl, profit, closed pnl, realized profit, net pnl",
            "fees, Fee, fee, commission, trading fee, exec_fee, fee_amount"
        ],
        "Example Format": [
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
    st.info(
        "💡 **Fuzzy Matching Active:** Even if your exchange export uses slightly different casing or column titles "
        "(e.g., `Exec_Time`, `Symbol`, `Qty`), `AutoMapper Helper` will automatically resolve and standardize them for analysis."
    )
    st.markdown("---")
    
    dl_col1, dl_col2 = st.columns([2, 1], vertical_alignment="center")

    with dl_col1:
        st.markdown(
            "Download the standard sample CSV template to see a reference structure"
            " for execution logs before uploading custom files."
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