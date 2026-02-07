from pyrogram import Client

from app.logger import logger
from app.storage import save_match

MAX_MESSAGE_TEXT_LENGTH = 100

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

        link = get_message_link(message)

        logger.info(
            f"[MATCH][{message.chat.title}] "
            f"id={message.id} "
            f"date={message.date} "
            f"{message.from_user.id if message.from_user else 'unknown'}: \n"
            f"link={link}\n"
            f"{content[:MAX_MESSAGE_TEXT_LENGTH]}"
        )

        match_data = {
            "chat": message.chat.username or message.chat.title,
            "chat_id": message.chat.id,
            "message_id": message.id,
            "date": message.date.isoformat() if message.date else None,
            "user_id": message.from_user.id if message.from_user else None,
            "username": message.from_user.username if message.from_user else None,
            "link": link,
            "text": content[:MAX_MESSAGE_TEXT_LENGTH]
        }

        save_match(match_data)

def get_message_link(message) -> str | None:
    chat = message.chat

    if chat.username:
        return f"http://t.me/{chat.username}/{message.id}"

    if chat.id:
        internal_id = str(chat.id).replace("-100", "")
        return f"http://t.me/{internal_id}/{message.id}"

    return None
