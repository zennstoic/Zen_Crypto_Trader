import logging, os, sys
from datetime import datetime

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLOR = True
except Exception:
    COLOR = False
    class _F: CYAN=GREEN=YELLOW=RED=MAGENTA=""
    class _S: RESET_ALL=""
    Fore=_F(); Style=_S()

ZEN_LINES = [
    "Breathe. Trade with intention.",
    "Edge > ego. Let the data speak.",
    "Small risk, many reps.",
    "Discipline is alpha."
]

def banner(app_name="Zen Crypto Trader"):
    tag = ZEN_LINES[datetime.utcnow().second % len(ZEN_LINES)]
    line = "═" * 68
    txt = f"\n{line}\n  {app_name} • Zen Style™ • {tag}\n{line}\n"
    return f"{Fore.CYAN}{txt}{Style.RESET_ALL}" if COLOR else txt

def get_logger(logs_dir="logs", name="zen"):
    os.makedirs(logs_dir, exist_ok=True)
    logfile = os.path.join(logs_dir, "app.log")
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        fh = logging.FileHandler(logfile)
        ch = logging.StreamHandler(sys.stdout)
        fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        fh.setFormatter(fmt); ch.setFormatter(fmt)
        logger.addHandler(fh); logger.addHandler(ch)
    return logger

def color(msg, c):
    return getattr(Fore, c.upper(), "") + msg + getattr(Style, "RESET_ALL", "")
