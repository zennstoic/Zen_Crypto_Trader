import pandas as pd
from typing import Dict, Any, Tuple
from ..exchanges.ccxt_client import CCXTClient
from ..strategies.sma_cross import SMACross

def fetch_ohlcv_df(exchange_name: str, symbol: str, timeframe: str, limit: int=500) -> pd.DataFrame:
    ex = CCXTClient(name=exchange_name)
    data = ex.get_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(data, columns=["time","open","high","low","close","volume"])
    df["time"] = pd.to_datetime(df["time"], unit="ms")
    return df

def run_backtest(config: Dict[str, Any]) -> Tuple[float, pd.DataFrame]:
    ex_name = config["exchange"]["name"]
    symbol = config["symbols"][0]
    tf     = config["timeframe"]
    df = fetch_ohlcv_df(ex_name, symbol, tf, limit=1000)

    strat_cfg = config["strategy"]["params"]
    strat = SMACross(**strat_cfg)
    signals = strat.generate_signals(df)

    balance = float(config["risk"]["starting_balance_usd"])
    position = 0.0
    entry_price = None

    for sig in signals:
        price = float(sig["price"])
        if sig["type"] == "buy" and balance > 0:
            position = balance / price
            entry_price = price
            balance = 0.0
        elif sig["type"] == "sell" and position > 0:
            balance = position * price
            position = 0.0
            entry_price = None

    if position > 0:
        balance = position * float(df["close"].iloc[-1])

    return balance, df
