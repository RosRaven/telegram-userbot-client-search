import logging

from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

# папка для логов
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
)

file_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=1_000_000, # ~1MB
    backupCount=5,
    encoding="utf-8"
)

file_handler.setFormatter(
    logging.Formatter(LOG_FORMAT)
)

logger = logging.getLogger("userbot")
logger.addHandler(file_handler)
logger.propagate = False

