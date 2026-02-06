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

    chat_ids_row = get_required_env("CHAT_IDS")
    keywords_row = get_required_env("KEYWORDS")

    chat_ids = [chat.strip() for chat in chat_ids_row.split(",") if chat.strip()]
    keywords = [kw.strip() for kw in keywords_row.split(",") if kw.strip()]

    if not chat_ids:
        raise ConfigError("CHAT_IDS must contain at least one chat")

    if not keywords:
        raise ConfigError("KEYWORDS must contain at least one keyword")

    return {
        "API_ID": int(api_id),
        "API_HASH": api_hash,
        "CHAT_IDS": chat_ids,
        "KEYWORDS": keywords,
    }
