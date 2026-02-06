from app.client import app
from app.logger import logger
from app.reader import read_last_message

LIMIT_READ_CHATS = 200

# CHAT_ID = "@AntalyaB"
CHAT_IDS = [
    "@AntalyaB",
    "@barakholka_antalya",
    "@baraholka_antalya_avito",
    "@antalya6",
    "@baraxlanet_antalya",
]

KEYWORDS = [
    "велосипед",
    "велик",
    "bike",
    "bicycle",
    "mtb",
    "road bike",
    "salcano",
    "shimano",

]

if __name__ == "__main__":
    try:
        logger.info("Starting userbot")

        # # One-time launch
        # app.run()

        # Reading a specific chat
        with app:
            for chat_id in CHAT_IDS:
                logger.info(f"Processing chat: {chat_id}")

                read_last_message(
                    app,
                    chat_id,
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
