# Zen Crypto Trader (Zen Style™)

Breathe. Then trade.

A professional, modular crypto trading bot for your portfolio:
- **Backtest** on historical OHLCV
- **Paper trade** (simulated, no keys required)
- **Live trade** via CCXT (Binance, Bybit, etc.)
- Clean config, human logs, CSV trade history

> Out-of-the-box: works in **paper mode** using public market data (no API keys).
> Add keys → it can place real orders (at your own risk).

---

## Features
- SMA Crossover strategy (pluggable)
- Risk config (position size, TP/SL %)
- CCXT exchange client
- Logs + `data/trades.csv`
- Zen Style™ banner + readable output

## Quickstart
```bash
git clone https://github.com/<you>/zen-crypto-trader.git
cd zen-crypto-trader
pip install -r requirements.txt
cp config.example.yaml config.yaml
Edit config.yaml to your taste. For paper mode you can keep API keys empty.

Backtest

python run_backtest.py
Paper Trading (no keys needed)

python run_paper.py
Live Trading (requires exchange API keys)
Put your keys inside config.yaml under exchange.

Optional: set testnet: true if your exchange supports sandbox.


python run_live.py
⚠️ Disclaimer: Live trading is risky. Use at your own risk. Start small.

Config
See config.example.yaml for all options. Key sections:

strategy: sma_cross with short_window, long_window

risk: position_size_usd, take_profit_pct, stop_loss_pct

exchange: name, api_key, api_secret, testnet

paths: logs and CSV output

Extend
Add more strategies to src/strategies/

Swap in a ML model (sklearn/torch) that outputs buy/sell/hold

Add new exchanges via CCXT config

Zen Notes
Start with paper mode.

Keep size small; test signals calmly.

Edge > ego. Let the data speak.