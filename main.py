import os

from app.client import app
from app.config import ConfigError, load_config
from app.logger import logger
from app.reader import read_last_message

LIMIT_READ_CHATS = 200

if __name__ == "__main__":
    try:
        logger.info("Starting userbot")

        config = load_config()
        logger.info("Configuration loaded successfully")

        logger.info(f"Chats to monitor: {len(config['CHAT_IDS'])}")
        for chat_id in config["CHAT_IDS"]:
            logger.info(f" - {chat_id}")

        logger.info(f"Search keywords: {len(config['KEYWORDS'])}")
        for keyword in config["KEYWORDS"]:
            logger.info(f" - {keyword}")

        logger.info(f"History read limit per chat: {LIMIT_READ_CHATS}")

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
        logger.error(f"Configuration error: {e}")

    except Exception:
        logger.exception("Fatal error during userbot execution")
