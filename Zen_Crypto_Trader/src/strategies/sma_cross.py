import pandas as pd
from typing import Dict, Any, List

def _sma(series: pd.Series, window: int) -> pd.Series:
    return series.rolling(window=window, min_periods=window).mean()

class SMACross:
    """
    Classic SMA crossover:
      - BUY when SMA(short) crosses above SMA(long)
      - SELL when SMA(short) crosses below SMA(long)
    """
    def __init__(self, short_window: int=9, long_window: int=21, warmup_bars: int=50):
        self.short = short_window
        self.long = long_window
        self.warmup = warmup_bars

    def generate_signals(self, ohlcv: pd.DataFrame) -> List[Dict[str, Any]]:
        df = ohlcv.copy()
        df["sma_s"] = _sma(df["close"], self.short)
        df["sma_l"] = _sma(df["close"], self.long)
        df["pos"] = 0
        df.loc[df["sma_s"] > df["sma_l"], "pos"] = 1
        df["signal"] = df["pos"].diff().fillna(0)

        # Convert to list of signals: +1 buy, -1 sell
        out = []
        for i, row in df.iterrows():
            if i < self.warmup:
                continue
            if row["signal"] == 1:
                out.append({"type": "buy", "price": row["close"], "index": int(i)})
            elif row["signal"] == -1:
                out.append({"type": "sell", "price": row["close"], "index": int(i)})
        return out
