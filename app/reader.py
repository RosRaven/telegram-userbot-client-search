from pyrogram import Client

from app.logger import logger


def read_last_message(app: Client, chat_id: str, limit: int = 5) -> None:
    logger.info(f"Reading last {limit} messages from chat: {chat_id}")

    for message in app.get_chat_history(chat_id, limit=limit):
        if message.text:
            logger.info(
                f"[{message.chat.title}] "
                f"{message.from_user.id if message.from_user else 'unknown'}: "
                f"{message.text[:100]}"
            )
