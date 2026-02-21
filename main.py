import argparse
import os
import time

from app.client import app
from app.config import ConfigError, load_config
from app.chat_registry import load_chat_registry, update_chat_registry, save_chat_registry
from app.logger import logger
from app.reader import read_last_message, analyze_chat
from app.state import load_seen, save_seen

def parse_args():
    parser = argparse.ArgumentParser(description="Telegram userbot lead scanner")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--scan-review", action="store_true", help="Analyse REVIEW chats and update registry")
    mode.add_argument("--run", action="store_true", help="Read READ chats and search matches")
    return parser.parse_args()

def run_scan_review(app, config, registry):
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

        changed_any = False

        for chat_id in list(dict.fromkeys(registry["REVIEW"])):
            logger.info(f"Analyzing chat: {chat_id}")

            decision = analyze_chat(app, chat_id, config)
            changed = update_chat_registry(chat_id, decision["verdict"], registry)
            changed_any = changed_any or changed

            time.sleep(config["CHAT_PAUSE_SECONDS"])

        if changed_any:
            logger.info(
                f"[MAIN] Changed chats\n"
                f"{registry}"
            )
            save_chat_registry(registry)


def run_run_mode(app, config, registry, seen_messages):
    with app:
        for chat_id in registry["READ"]:
            logger.info(f"Processing chat: {chat_id}")
    
            chat_seen = seen_messages.setdefault(str(chat_id), set())
    
            read_last_message(
                app,
                chat_id,
                keywords=config["KEYWORDS"],
                seen_ids=chat_seen,
                limit=config["LIMIT_READ_CHATS"],
            )
    
            time.sleep(config["CHAT_PAUSE_SECONDS"])
    
        save_seen(seen_messages)

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

        logger.info(f"History read limit per chat: {config['LIMIT_READ_CHATS']}")

        registry = load_chat_registry()
        for category, chats in registry.items():
            logger.info(f"{category}: {len(chats)} chats")

        args = parse_args()

        if args.scan_review:
            run_scan_review(app, config, registry)
        elif args.run:
            run_run_mode(app, config, registry, seen_messages)

        # # One-time launch
        # app.run()

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
