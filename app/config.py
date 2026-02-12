import os

class ConfigError(RuntimeError):
    pass

def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ConfigError(f"Required environment varible '{name}' is missing or empty")
    return value

def load_config() -> dict:
    api_id = get_required_env("API_ID")
    api_hash = get_required_env("API_HASH")

    LIMIT_READ_CHATS = int(get_required_env("LIMIT_READ_CHATS"))
    CHAT_PAUSE_SECONDS = int(get_required_env("CHAT_PAUSE_SECONDS"))

    MIN_DENSITY = float(get_required_env("MIN_DENSITY"))
    MIN_MATCH_MESSAGES = int(get_required_env("MIN_MATCH_MESSAGES"))
    MIN_UNIQUE_AUTHORS = int(get_required_env("MIN_UNIQUE_AUTHORS"))

    # chat_ids_row = get_required_env("CHAT_IDS")
    # chat_ids = [chat.strip() for chat in chat_ids_row.split(",") if chat.strip()]

    keywords_row = get_required_env("KEYWORDS")
    keywords = [kw.strip() for kw in keywords_row.split(",") if kw.strip()]

    # if not chat_ids:
    #     raise ConfigError("CHAT_IDS must contain at least one chat")

    if not keywords:
        raise ConfigError("KEYWORDS must contain at least one keyword")

    return {
        "API_ID": int(api_id),
        "API_HASH": api_hash,
        # "CHAT_IDS": chat_ids,
        "KEYWORDS": keywords,
        "LIMIT_READ_CHATS": LIMIT_READ_CHATS,
        "CHAT_PAUSE_SECONDS": CHAT_PAUSE_SECONDS,
        "MIN_DENSITY": MIN_DENSITY,
        "MIN_MATCH_MESSAGES": MIN_MATCH_MESSAGES,
        "MIN_UNIQUE_AUTHORS": MIN_UNIQUE_AUTHORS
    }
