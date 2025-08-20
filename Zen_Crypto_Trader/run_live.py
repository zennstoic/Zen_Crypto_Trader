# run_live.py
import time
import logging
import yaml
from src.exchanges.ccxt_client import CCXTClient
from src.strategies.sma_cross import SMACrossStrategy

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

# Load config
with open("config.example.yaml", "r") as f:
    config = yaml.safe_load(f)

# Initialize exchanges
exchanges = CCXTClient(config.get("exchanges", []))

# Initialize strategy
strategy_config = config["strategy"]
strategy = SMACrossStrategy(strategy_config["params"])

# Paper/live settings
position_size = config["risk"]["position_size_usd"]
loop_interval = config["loop_interval_sec"]

logging.info("Starting LIVE multi-exchange trading bot...")

while True:
    market_data = exchanges.get_market_data()
    for exchange_name, ticker in market_data.items():
        signal = strategy.generate_signal(ticker)
        if signal:
            logging.info(f"{exchange_name} signal: {signal}")
            exchanges.place_order(signal, position_size)
    time.sleep(loop_interval)
