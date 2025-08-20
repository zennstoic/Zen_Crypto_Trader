import os, csv
from typing import Dict, Any

def ensure_dirs(*paths):
    for p in paths:
        os.makedirs(p, exist_ok=True)

def append_trade(trades_csv: str, trade: Dict[str, Any]):
    os.makedirs(os.path.dirname(trades_csv), exist_ok=True)
    file_exists = os.path.isfile(trades_csv)
    with open(trades_csv, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=trade.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(trade)
