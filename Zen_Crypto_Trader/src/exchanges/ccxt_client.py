# src/exchanges/ccxt_client.py
import ccxt
import logging

class CCXTClient:
    def __init__(self, exchange_configs):
        """
        Accepts a list of exchange configs from YAML
        """
        self.clients = []
        for cfg in exchange_configs:
            name = cfg.get("name")
            if not hasattr(ccxt, name):
                logging.warning(f"Exchange {name} not found in CCXT. Skipping.")
                continue
            exchange_class = getattr(ccxt, name)
            client = exchange_class({
                "apiKey": cfg.get("api_key", ""),
                "secret": cfg.get("api_secret", ""),
                "password": cfg.get("password", ""),
                "enableRateLimit": True,
            })
            # enable sandbox if testnet=True
            if cfg.get("testnet", False) and hasattr(client, "set_sandbox_mode"):
                client.set_sandbox_mode(True)
            self.clients.append({"name": name, "client": client, "symbol": cfg.get("symbol", "BTC/USDT")})
            logging.info(f"{name} client initialized.")
    
    def get_market_data(self, symbol=None):
        results = {}
        for ex in self.clients:
            s = symbol or ex["symbol"]
            try:
                ticker = ex["client"].fetch_ticker(s)
                results[ex["name"]] = ticker
            except Exception as e:
                logging.error(f"Error fetching market data from {ex['name']}: {e}")
        return results

    def place_order(self, signal, amount):
        orders = {}
        for ex in self.clients:
            try:
                if signal == "buy":
                    order = ex["client"].create_market_buy_order(ex["symbol"], amount)
                elif signal == "sell":
                    order = ex["client"].create_market_sell_order(ex["symbol"], amount)
                else:
                    logging.warning("Unknown signal.")
                    orders[ex["name"]] = None
                    continue
                logging.info(f"{ex['name']}: {signal.upper()} order executed: {order}")
                orders[ex["name"]] = order
            except Exception as e:
                logging.error(f"{ex['name']}: Failed to place order: {e}")
                orders[ex["name"]] = None
        return orders
