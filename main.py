from app.client import app
from app.logger import logger

if __name__ == "__main__":
    try:
        logger.info("Starting userbot")
        app.run()
    except Exception:
        logger.exception("Fatal error during userbot execution")
