import json

from pathlib import Path

SEEN_FILE = Path("seen_messages.json")

def load_seen() -> dict[str, set[int]]:
    if not SEEN_FILE.exists():
        return {}

    if SEEN_FILE.stat().st_size == 0:
        return {}

    try:
        with SEEN_FILE.open("r", encoding="utf-8") as f:
            raw = json.load(f)
    except json.JSONDecodeError:
        return {}

    return {
        chat_id: set(map(int, message_ids))
        for chat_id, message_ids in raw.items()
    }

def save_seen(seen: dict[str, set[int]]) -> None:
    serializable = {
        chat_id: list(message_ids)
        for chat_id, message_ids in seen.items()
    }

    with SEEN_FILE.open("w", encoding="utf-8") as f:
        json.dump(serializable, f, ensure_ascii=False, indent=2)
