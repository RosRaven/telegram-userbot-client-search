from pyrogram import Client

from app.logger import logger

MAX_MESSAGE_TEXT_LENGTH = 600

def read_last_message(
        app: Client,
        chat_id: str,
        keywords: list[str],
        limit: int = 5
) -> None:
    logger.info(f"Reading last {limit} messages from chat: {chat_id}")

    for message in app.get_chat_history(chat_id, limit=limit):
        content = message.text or message.caption
        if not content:
            continue

        text_lower = content.lower()

        if not any(keyword in text_lower for keyword in keywords):
            continue

        logger.info(
            f"[MATCH][{message.chat.title}] "
            f"id={message.id} "
            f"date={message.date} "
            f"{message.from_user.id if message.from_user else 'unknown'}: "
            f"{content[:MAX_MESSAGE_TEXT_LENGTH]}"
        )
