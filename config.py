from __future__ import annotations
from functools import lru_cache
from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent
CONF_DIR = BASE_DIR / "conf"

def _load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

@lru_cache()
def get_app_config():
    return _load_json(CONF_DIR / "app.json")

@lru_cache()
def get_theme_config():
    return _load_json(CONF_DIR / "theme.json")

@lru_cache()
def get_menu_config():
    return _load_json(CONF_DIR / "menu.json")

@lru_cache()
def get_users_config():
    return _load_json(CONF_DIR / "users.json")

@lru_cache()
def get_page_config(page_key: str):
    return _load_json(CONF_DIR / "pages" / f"{page_key}.json")

@lru_cache()
def get_master_sync_config():
    return _load_json(CONF_DIR / "master_sync.json")
