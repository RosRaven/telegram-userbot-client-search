import json

from pathlib import Path

CHAT_FILE = Path("chats.json")

REQUIRED_KEYS = {"READ", "REVIEW", "SKIP"}

def load_chat_registry() -> dict[str, list]:
    if not CHAT_FILE.exists():
        raise RuntimeError("chats.json not found")

    with CHAT_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)

    missing = REQUIRED_KEYS - data.keys()
    if missing:
        raise RuntimeError(f"Missing chat categories: {missing}")

    return data
