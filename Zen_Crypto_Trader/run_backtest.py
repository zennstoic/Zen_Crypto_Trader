from src.config import load_config
from src.engine.backtest import run_backtest
from src.utils.logger import banner

if __name__ == "__main__":
    print(banner("Zen Crypto Trader — Backtest"))
    cfg = load_config()
    final_balance, _ = run_backtest(cfg)
    start = cfg["risk"]["starting_balance_usd"]
    print(f"Start: ${start:.2f}  ->  End: ${final_balance:.2f}")
