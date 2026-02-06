import os

from app.client import app
from app.config import ConfigError, load_config
from app.logger import logger
from app.reader import read_last_message

CHAT_IDS = os.getenv("CHAT_IDS", "").split(",")
KEYWORDS = os.getenv("KEYWORDS", "").split(",")

LIMIT_READ_CHATS = 200

if __name__ == "__main__":
    try:
        config = load_config()

        logger.info("Starting userbot")
        logger.info(
            f"Config loaded: chats={len(config['CHAT_IDS'])}, "
            f"keywords={len(config['KEYWORDS'])}"
        )

        # # One-time launch
        # app.run()

        # Reading a specific chat
        with app:
            for chat_id in config["CHAT_IDS"]:
                logger.info(f"Processing chat: {chat_id}")

                read_last_message(
                    app,
                    chat_id,
                    keywords=config["KEYWORDS"],
                    limit=LIMIT_READ_CHATS,
                )

        # # Reading all dialogues
        # with app:
        #     for dialog in app.get_dialogs():
        #         logger.info(
        #             f"Chat title: {dialog.chat.title} | ID: {dialog.chat.id}"
        #         )

    except ConfigError as e:
        logger.info(f"Configuration error: {e}")

    except Exception:
        logger.exception("Fatal error during userbot execution")
