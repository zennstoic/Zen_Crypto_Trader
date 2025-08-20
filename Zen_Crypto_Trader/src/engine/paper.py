import time, math, pandas as pd
from typing import Dict, Any
from ..exchanges.ccxt_client import CCXTClient
from ..strategies.sma_cross import SMACross
from ..utils.storage import append_trade
from ..utils.logger import get_logger, banner

def ohlcv_to_df(ohlcv):
    df = pd.DataFrame(ohlcv, columns=["time","open","high","low","close","volume"])
    df["time"] = pd.to_datetime(df["time"], unit="ms")
    return df

def run_paper(config: Dict[str, Any]):
    print(banner("Zen Crypto Trader — Paper"))
    logger = get_logger(config["paths"]["logs_dir"])

    ex = CCXTClient(
        name=config["exchange"]["name"],
        api_key=config["exchange"]["api_key"],
        api_secret=config["exchange"]["api_secret"],
        password=config["exchange"]["password"],
        testnet=bool(config["exchange"]["testnet"])
    )
    sym = config["symbols"][0]
    tf  = config["timeframe"]

    strat = SMACross(**config["strategy"]["params"])
    bal = float(config["risk"]["starting_balance_usd"])
    pos = 0.0
    entry = None

    logger.info(f"Paper mode on {sym} @ {tf}. Starting balance: ${bal:.2f}")

    while True:
        try:
            ohlcv = ex.get_ohlcv(sym, timeframe=tf, limit=500)
            df = ohlcv_to_df(ohlcv)
            signals = strat.generate_signals(df)
            if signals:
                sig = signals[-1]  # act on most recent signal
                price = float(sig["price"])
                if sig["type"] == "buy" and bal > 0:
                    pos = bal / price
                    entry = price
                    bal = 0.0
                    logger.info(f"[DRY] BUY {sym} @ {price:.2f}")
                    append_trade(config["paths"]["trades_csv"], {
                        "mode": "paper","side":"buy","symbol":sym,"price":price,
                        "qty": pos, "balance_after": bal
                    })
                elif sig["type"] == "sell" and pos > 0:
                    bal = pos * price
                    pnl = (price - entry) * pos if entry else 0.0
                    logger.info(f"[DRY] SELL {sym} @ {price:.2f} | PnL: ${pnl:.2f} | Bal: ${bal:.2f}")
                    append_trade(config["paths"]["trades_csv"], {
                        "mode": "paper","side":"sell","symbol":sym,"price":price,
                        "qty": pos, "balance_after": bal, "pnl": pnl
                    })
                    pos = 0.0; entry = None
            time.sleep(int(config["loop_interval_sec"]))
        except KeyboardInterrupt:
            logger.info("Stop requested. Exiting.")
            break
        except Exception as e:
            logger.exception(f"Loop error: {e}")
            time.sleep(3)
