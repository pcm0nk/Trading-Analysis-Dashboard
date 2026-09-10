import pandas as pd
from rapidfuzz import process, fuzz

# The exact standard schema expected downstream in your project
TARGET_SCHEMA = [
    "fill_time",
    "pair",
    "direction",
    "quantity",
    "price",
    "pnl",
    "fees"
]

# Aliases mapped across various exchanges (WEX, Binance, Bybit, OKX, etc.)
KNOWN_EXCHANGE_ALIASES = {
    "fill_time": [
        "Filled time(UTC)", "filled time", "fill time", "time", "created time", 
        "date", "timestamp", "trade time", "filled_time", "order time", "exec_time"
    ],
    "pair": [
        "Futures", "Symbol", "Instrument", "pair", "market", "contract", 
        "ticker", "asset", "product"
    ],
    "direction": [
        "Direction", "Side", "type", "order side", "position side", "action", 
        "buy/sell", "trade type"
    ],
    "quantity": [
        "Filled Quantity", "Amount", "Qty", "quantity", "filled qty", "size", 
        "filled amount", "executed qty", "exec_qty"
    ],
    "price": [
        "Filled Price", "Price", "avg price", "executed price", "fill price", 
        "avg_price", "exec_price"
    ],
    "pnl": [
        "Realized PNL", "PNL", "realized pnl", "realized_pnl", "profit", 
        "closed pnl", "realized profit", "net pnl"
    ],
    "fees": [
        "fees", "Fee", "fee", "commission", "trading fee", "exec_fee", "fee_amount"
    ]
}

def detect_exchange_signature(df: pd.DataFrame) -> str:
    """
    Inspects raw DataFrame column names and patterns to detect 
    which exchange/broker format the sheet belongs to.
    """
    cols = [str(c).strip().lower() for c in df.columns]

    if "filled time(utc)" in cols and "futures" in cols:
        return "Standard / WEX Format"
    elif "exec_time" in cols or "symbol" in cols and "closed_pnl" in cols:
        return "Bybit / Binance Export"
    elif "instrument" in cols and "side" in cols:
        return "OKX / Generic FX Export"
    
    return "Custom / Unrecognized Exchange Export"


def map_columns_to_standard(df: pd.DataFrame, score_cutoff: int = 70) -> tuple[pd.DataFrame, dict, list]:
    """
    Scans raw DataFrame columns and normalizes headers to the standard internal target names.
    Returns: (mapped_df, mapping_report, missing_columns)
    """
    df_cols = list(df.columns)
    mapping_report = {}
    mapped_df = df.copy()
    used_df_cols = set()

    for target_col in TARGET_SCHEMA:
        aliases = KNOWN_EXCHANGE_ALIASES.get(target_col, [])
        best_match = None
        best_score = 0

        # Phase 1: Direct Match or Exact Alias Match
        for df_col in df_cols:
            if df_col in used_df_cols:
                continue

            cleaned = str(df_col).strip()
            if cleaned == target_col or cleaned in aliases or cleaned.lower() in [a.lower() for a in aliases]:
                best_match = df_col
                best_score = 100
                break

        # Phase 2: Fuzzy Logic Match (if no exact alias hit)
        if not best_match:
            candidate_pool = [c for c in df_cols if c not in used_df_cols]
            search_choices = [target_col] + aliases

            for df_col in candidate_pool:
                cleaned_df_col = str(df_col).lower().replace("_", " ").strip()
                match_result = process.extractOne(
                    cleaned_df_col, 
                    [str(choice).lower().replace("_", " ") for choice in search_choices],
                    scorer=fuzz.WRatio
                )
                if match_result and match_result[1] > best_score and match_result[1] >= score_cutoff:
                    best_score = match_result[1]
                    best_match = df_col

        if best_match:
            mapping_report[best_match] = target_col
            used_df_cols.add(best_match)

    mapped_df = mapped_df.rename(columns=mapping_report)
    missing_columns = [col for col in TARGET_SCHEMA if col not in mapped_df.columns]

    return mapped_df, mapping_report, missing_columns