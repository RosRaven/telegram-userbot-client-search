import json

from pathlib import Path

from app.logger import logger

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

def update_chat_registry(chat_id: str, verdict: str, registry: dict) -> bool:
    allowed = {"READ", "REVIEW", "SKIP"}
    verdict = verdict.strip().upper()
    if verdict not in allowed:
        raise ValueError(f"Verdict {verdict} not allowed")

    chat_id = str(chat_id)
    changed = False

    for category in allowed:
        bucket = registry.setdefault(category, [])
        before = len(bucket)
        bucket[:] = [x for x in bucket if str(x) != chat_id]
        if len(bucket) != before:
            changed = True
    
    if not any(str(x) == chat_id for x in registry[verdict]):
        registry[verdict].append(chat_id)
        changed = True
    
    return changed

def save_chat_registry(data: dict) -> None:
    with CHAT_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"[save_chat_registry] Rewrite file with chats_ids")
