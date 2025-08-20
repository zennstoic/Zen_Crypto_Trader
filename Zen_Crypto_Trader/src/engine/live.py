import time, pandas as pd, math
from typing import Dict, Any
from ..exchanges.ccxt_client import CCXTClient
from ..strategies.sma_cross import SMACross
from ..utils.storage import append_trade
from ..utils.logger import get_logger, banner

def ohlcv_to_df(ohlcv):
    df = pd.DataFrame(ohlcv, columns=["time","open","high","low","close","volume"])
    df["time"] = pd.to_datetime(df["time"], unit="ms")
    return df

def run_live(config: Dict[str, Any]):
    print(banner("Zen Crypto Trader — LIVE"))
    logger = get_logger(config["paths"]["logs_dir"])
    ex = CCXTClient(
        name=config["exchange"]["name"],
        api_key=config["exchange"]["api_key"],
        api_secret=config["exchange"]["api_secret"],
        password=config["exchange"]["password"],
        testnet=bool(config["exchange"]["testnet"])
    )
    sym = config["symbols"][0]; tf = config["timeframe"]
    size_usd = float(config["risk"]["position_size_usd"])
    strat = SMACross(**config["strategy"]["params"])

    logger.info(f"Live trading on {sym} @ {tf} | Size ${size_usd:.2f}")

    while True:
        try:
            ohlcv = ex.get_ohlcv(sym, timeframe=tf, limit=500)
            df = ohlcv_to_df(ohlcv)
            signals = strat.generate_signals(df)
            if signals:
                sig = signals[-1]
                ticker = ex.get_ticker(sym)
                if not ticker: 
                    time.sleep(2); continue
                price = float(ticker["last"])

                # position sizing (base amount)
                amount = size_usd / price
                side = "buy" if sig["type"] == "buy" else "sell"

                order = ex.create_market_order(sym, side, amount)
                logger.info(f"[LIVE] {side.upper()} {sym} ~ {amount:.6f} @ ~{price:.2f} | id={order.get('id','?')}")
                append_trade(config["paths"]["trades_csv"], {
                    "mode":"live","side":side,"symbol":sym,"price":price,
                    "qty":amount,"order_id":order.get("id","")
                })
            time.sleep(int(config["loop_interval_sec"]))
        except KeyboardInterrupt:
            logger.info("Stop requested. Exiting.")
            break
        except Exception as e:
            logger.exception(f"Loop error: {e}")
            time.sleep(3)
