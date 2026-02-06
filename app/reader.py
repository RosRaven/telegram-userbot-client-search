from pyrogram import Client

from app.logger import logger


def read_last_message(app: Client, chat_id: str, limit: int = 5) -> None:
    logger.info(f"Reading last {limit} messages from chat: {chat_id}")

    for message in app.get_chat_history(chat_id, limit=limit):
        # Temporary stub. Checking that the message limit is read.
        logger.info(
            f"[{message.chat.title}] "
            f"id={message.id} "
            f"text={bool(message.text)} "
            f"caption={bool(message.caption)} "
            f"media={bool(message.media)} "
            f"service={bool(message.service)} "
        )

        # content = message.text or message.caption
        # if not content:
        #     continue
        #
        # logger.info(
        #     f"[{message.chat.title}] "
        #     f"id={message.id} "
        #     f"date={message.date} "
        #     f"{message.from_user.id if message.from_user else 'unknown'}: "
        #     f"{content[:100]}"
        # )
