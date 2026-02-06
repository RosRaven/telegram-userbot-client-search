from app.client import app
from app.logger import logger
from app.reader import read_last_message

LIMIT_READ_CHATS = 200
CHAT_ID = "@AntalyaB"

KEYWORDS = [
    "велосипед",
    "велик",
    "bike",
    "bicycle",
    "mtb",
    "road bike",
]

if __name__ == "__main__":
    try:
        logger.info("Starting userbot")

        # # One-time launch
        # app.run()

        # Reading a specific chat
        with app:
            read_last_message(
                app,
                CHAT_ID,
                keywords=KEYWORDS,
                limit=LIMIT_READ_CHATS
            )

        # # Reading all dialogues
        # with app:
        #     for dialog in app.get_dialogs():
        #         logger.info(
        #             f"Chat title: {dialog.chat.title} | ID: {dialog.chat.id}"
        #         )

    except Exception:
        logger.exception("Fatal error during userbot execution")
