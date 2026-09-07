import streamlit as st
import pandas as pd

from validation.data_prep import clean_and_prepare_data
from validation.sanity_checks import run_sanity_checks
from validation.fifo_engine import process_fifo_trades

def run_validation_phase(uploaded_file):
    """
    Executes Phase 1: Data Preparation, Structural Sanity Checks, 
    and FIFO Order Matching & Position Consolidation.
    """
    # 1. Load Raw File and Standardize Schema
    if isinstance(uploaded_file, str):
        file_name = uploaded_file
    else:
        file_name = uploaded_file.name

    # Load CSV or Excel based on file extension
    if file_name.lower().endswith('.csv'):
        raw_df = pd.read_csv(uploaded_file)
    else:
        raw_df = pd.read_excel(uploaded_file)
        
    df = clean_and_prepare_data(raw_df)

    start_dt = df['fill_time'].min().strftime('%Y-%m-%d %H:%M UTC')
    end_dt = df['fill_time'].max().strftime('%Y-%m-%d %H:%M UTC')

    st.subheader("Phase 1: Validation & FIFO Reconstruction")
    st.caption(f"**Execution Window:** {start_dt} to {end_dt} | **Total Raw Fills:** {len(df):,}")

    # 2. Run Sanity Checks BEFORE FIFO Processing
    st.markdown("### 1. Pre-FIFO Raw Execution Sanity Checks")
    sanity_results, df_sorted = run_sanity_checks(df)

    sanity_table = []
    for test_name, res in sanity_results.items():
        sanity_table.append({
            "Validation Check": test_name,
            "Status": res['Status'],
            "Audit Detail": res['Detail']
        })

    st.dataframe(pd.DataFrame(sanity_table), use_container_width=True)

    #3. Pass Clean Fills to FIFO Engine (Receives raw fragments, consolidated positions, anomalies)
    st.markdown(
    "### 2. FIFO Order Reconstruction & Position Audit",
    help=(
        "How It Works:\n"
        "1. Queue Management: The engine iterates through raw fills grouped by symbol/pair. Opening fills enter an open_queue.\n\n"
        "2. FIFO Matching: When a closing fill occurs, the algorithm matches it against the oldest available entry in the queue (open_queue[0]).\n\n"
        "3. Proportional Fee & PnL Allocation: If a close partial-fills an entry, entry fees, exit fees, and realized PnL are allocated proportionally based on matched volume.\n\n"
        "4. Exit Outcome Classification: Each sub-trade is tagged as a Take Profit (TP), Stop Loss (SL), Breakeven (BE), or Liquidation.\n\n"
        "5. Position Consolidation: Next, our consolidation function aggregates contiguous partial fills in the same direction into a single row. Entry and exit prices are recalculated using volume-weighted averages, fees are summed, and total holding duration is calculated from initial entry to final exit flat."
    )
)
    clean_trades_df, consolidated_trades_df, anomalies_df = process_fifo_trades(df_sorted)

    # Separate FIFO Orphans
    orphan_opens = anomalies_df[anomalies_df['anomaly_type'].str.contains('Open', case=False, na=False)] if not anomalies_df.empty else pd.DataFrame()
    orphan_closes = anomalies_df[anomalies_df['anomaly_type'].str.contains('Close', case=False, na=False)] if not anomalies_df.empty else pd.DataFrame()

    # Metrics Summary Bar
    mcol1, mcol2, mcol3, mcol4, mcol5 = st.columns(5)
    mcol1.metric(
        label="Raw Fills Ingested",
        value=f"{len(df_sorted):,}",
        help="The total number of execution rows uploaded from the raw exchange file."
    )

    mcol2.metric(
        label="Matched Execution Fragments",
        value=f"{len(clean_trades_df):,}",
        help="The number of sub-fill execution pieces that were successfully matched on a First-In-First-Out basis."
    )

    mcol3.metric(
        label="Consolidated Positions",
        value=f"{len(consolidated_trades_df):,}",
        help="The number of completed full trade lifecycles created after merging scaled entries and partial exits."
    )

    mcol4.metric(
        label="Open Position Inventory",
        value=f"{len(orphan_opens):,}",
        help="Count of unclosed position fills remaining open at the end of the dataset."
    )

    mcol5.metric(
        label="Unmatched Close Errors",
        value=f"{len(orphan_closes):,}",
        delta_color="inverse",
        help="Severe anomalies where a closing fill occurred without a prior open order on record."
    )

    # Download Button for Consolidated Positions CSV
    if not consolidated_trades_df.empty:
        csv_data = consolidated_trades_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Consolidated Positions (CSV)",
            data=csv_data,
            file_name="consolidated_fifo_positions.csv",
            mime="text/csv",
            help="Download the consolidated position dataset where partial entries and scaled exits are merged into single unified trade lifecycles."
        )

    # Display Anomalies Table if present
    if not anomalies_df.empty:
     st.markdown(
        "#### FIFO Audit Inventory & Execution Anomalies",
        help="""If the raw log contains missing data or active positions,
        this table appears. Three distinct anomaly types exist:

        1. Orphan Open (Unclosed Inventory)
        • What it is: Position inventory opened but not closed
        before the log window ended.
        • Why it happens: Active open trade, or file export
        range ended while position was open.
        • Detail: 'Unmatched position inventory remaining'

        2. Orphan Close (Missing Entry Error)
        • What it is: Closing/liquidation order executed without
        a prior opening trade in queue.
        • Why it happens: Trade was opened before the start
        date of the exported date range.
        • Detail: 'Missing prior opening trade entry'

        3. Orphan Close (Partial) (Queue Exhaustion Error)
        • What it is: Close fill partially matched, but entry queue
        ran out before full exit quantity was resolved.
        • Why it happens: Open quantity on record was smaller
        than the exit quantity executed.
        • Detail: 'Exhausted open order queue before matching'"""
     )

    st.dataframe(anomalies_df, use_container_width=True)

    # Metadata pipeline handoff to Phase 2 (Trade Analysis)
    all_sanity_passed = all(res['Passed'] for res in sanity_results.values())
    has_no_close_errors = len(orphan_closes) == 0

    meta = {
        'passed': all_sanity_passed and has_no_close_errors,
        'total_fills': len(df_sorted),
        'matched_trades': len(clean_trades_df),
        'consolidated_positions': len(consolidated_trades_df),
        'open_positions': len(orphan_opens),
        'unmatched_errors': len(orphan_closes)
    }

    # Pass consolidated positions to Phase 2 so Session Transitions/Trade Analysis use full trades
    return meta, consolidated_trades_df