import json

from pathlib import Path
from typing import Dict

RESULT_FILE = Path("results.jsonl")

def save_match(data: Dict) -> None:
    RESULT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with RESULT_FILE.open("a", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
        f.write("\n")