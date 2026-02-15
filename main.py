import os
import time

from app.client import app
from app.config import ConfigError, load_config
from app.chat_registry import load_chat_registry
from app.logger import logger
from app.reader import read_last_message, analyze_chat
from app.state import load_seen, save_seen

# LIMIT_READ_CHATS = 2000
# CHAT_PAUSE_SECONDS = 1

if __name__ == "__main__":
    try:
        logger.info("Starting userbot")

        config = load_config()
        logger.info("Configuration loaded successfully")

        seen_messages = load_seen()

        # logger.info(f"Chats to monitor: {len(config['CHAT_IDS'])}")
        # for chat_id in config["CHAT_IDS"]:
        #     logger.info(f" - {chat_id}")

        logger.info(f"Search keywords: {len(config['KEYWORDS'])}")
        for keyword in config["KEYWORDS"]:
            logger.info(f" - {keyword}")

        logger.info(f"History read limit per chat: {config["LIMIT_READ_CHATS"]}")

        chat_registry = load_chat_registry()
        for category, chats in chat_registry.items():
            logger.info(f"{category}: {len(chats)} chats")

        # # One-time launch
        # app.run()

        # # Only read chats from category READ
        # with app:
        #     for chat_id in chat_registry["READ"]:
        #         logger.info(f"Processing chat: {chat_id}")
        #
        #         chat_seen = seen_messages.setdefault(str(chat_id), set())
        #
        #         read_last_message(
        #             app,
        #             chat_id,
        #             keywords=config["KEYWORDS"],
        #             seen_ids=chat_seen,
        #             limit=config["LIMIT_READ_CHATS"],
        #         )
        #
        #         time.sleep(config["CHAT_PAUSE_SECONDS"])
        #
        #     save_seen(seen_messages)

        # # Reading all dialogues
        # with app:
        #     for dialog in app.get_dialogs():
        #         logger.info(
        #             f"Chat title: {dialog.chat.title} | ID: {dialog.chat.id}"
        #         )

        # I read all unsorted chats "REVIEW"
        with app:
            MIN_DENSITY = config["MIN_DENSITY"]
            MIN_MATCH_MESSAGES = config["MIN_MATCH_MESSAGES"]
            MIN_UNIQUE_AUTHORS = config["MIN_UNIQUE_AUTHORS"]
            logger.info(
                "Start analyzing chats\n"
                f"MIN_DENSITY = {MIN_DENSITY}\n"
                f"MIN_MATCH_MESSAGES = {MIN_MATCH_MESSAGES}\n"
                f"MIN_UNIQUE_AUTHORS = {MIN_UNIQUE_AUTHORS}\n"
            )

            for chat_id in chat_registry["REVIEW"]:
                logger.info(f"Analis chat: {chat_id}")

                # data_analyze = analyze_chat(app, chat_id, config['KEYWORDS'], config["LIMIT_READ_CHATS"])
                decision = analyze_chat(app, chat_id, config)

                time.sleep(config["CHAT_PAUSE_SECONDS"])


    except ConfigError as e:
        logger.error(f"Configuration error: {e}")

    except Exception:
        logger.exception("Fatal error during userbot execution")
