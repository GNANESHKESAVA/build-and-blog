import os
import json
from pathlib import Path

CONFIG_DIR = Path.home() / ".codeinspector"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_CONFIG = {
    "github_token": "",
    "google_api_key": "",
    "llm_model": "gemini-2.0-flash",
    "max_pr_lines": 500,
    "coverage_threshold": 80,
    "lint_strict": True,
    "auto_approve": True,
    "db_path": str(Path.home() / ".codeinspector" / "commits.db")
}

def load_config():
    if not CONFIG_FILE.exists():
        return DEFAULT_CONFIG
    
    try:
        with open(CONFIG_FILE, "r") as f:
            return {**DEFAULT_CONFIG, **json.load(f)}
    except Exception:
        return DEFAULT_CONFIG

def save_config(config):
    CONFIG_DIR.mkdir(exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
