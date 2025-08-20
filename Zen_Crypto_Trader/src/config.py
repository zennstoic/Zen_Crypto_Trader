import yaml, os
from dataclasses import dataclass
from typing import Any, Dict

DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.yaml")

def load_config(path: str = None) -> Dict[str, Any]:
    cfg_path = path or DEFAULT_CONFIG_PATH
    if not os.path.isfile(cfg_path):
        # fallback to example
        cfg_path = os.path.join(os.path.dirname(__file__), "..", "config.example.yaml")
    with open(cfg_path, "r") as f:
        return yaml.safe_load(f)
