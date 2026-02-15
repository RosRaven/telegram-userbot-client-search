from pyrogram import Client

from app.logger import logger
from app.storage import save_match

MAX_MESSAGE_TEXT_LENGTH = 100

DEMAND_KEYWORDS = [
    "ищу",
    "нужен",
    "нужна",
    "нужно",
    "подскажите",
    "посоветуйте",
    "кто может",
    "есть ли",
]

OFFER_KEYWORDS = [
    "провожу",
    "провожу занятия",
    "предлагаю",
    "набираю",
    "обучаю",
    "обучение",
    "курсы",
    "школа",
    "онлайн школа",
    "опыт работы",
    "стаж",
]



def read_last_message(
        app: Client,
        chat_id: str,
        keywords: list[str],
        seen_ids: set[int],
        limit: int = 5,
) -> None:
    logger.info(f"Reading last {limit} messages from chat: {chat_id}")

    for message in app.get_chat_history(chat_id, limit=limit):

        if message.id in seen_ids:
            continue

        content = message.text or message.caption
        if not content:
            continue

        text_lower = content.lower()

        has_subject = any(keyword in text_lower for keyword in keywords)
        has_demand = any(word in text_lower for word in DEMAND_KEYWORDS)
        has_offer = any(word in text_lower for word in OFFER_KEYWORDS)

        if not has_subject:
            continue

        if not has_demand:
            continue

        if has_offer:
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
        seen_ids.add(message.id)

def get_message_link(message) -> str | None:
    chat = message.chat

    if chat.username:
        return f"http://t.me/{chat.username}/{message.id}"

    if chat.id:
        internal_id = str(chat.id).replace("-100", "")
        return f"http://t.me/{internal_id}/{message.id}"

    return None


def analyze_chat(
        app: Client,
        chat_id: str,
        config: dict,
) -> dict:

    keywords = config["KEYWORDS"]
    limit = config["LIMIT_READ_CHATS"]

    logger.info(f"Cheking chat. Reading last {limit} messages from chat: {chat_id}")

    total_messages_all = 0
    total_messages_text = 0
    keyword_hits = {key: 0 for key in keywords}
    count_match = 0
    set_unique_authors = set()
    newest_date = None
    oldest_date = None

    for message in app.get_chat_history(chat_id, limit=limit):

        if newest_date is None:
            newest_date = message.date
        oldest_date = message.date

        total_messages_all += 1
        content = message.text or message.caption
        if not content:
            continue
        total_messages_text += 1

        text_lower = content.lower()

        message_has_matches = False
        for key in keywords:
            count = text_lower.count(key)
            if count > 0:
                keyword_hits[key] += count
                message_has_matches = True

        if message_has_matches:
            count_match += 1
            if message.from_user:
                set_unique_authors.add(message.from_user.id)

    unique_authors = len(set_unique_authors)
    author_diversity_ratio = unique_authors / count_match

    density_all = count_match / total_messages_all if total_messages_all else 0
    density_percent_all = round(density_all * 100, 6)


    density_text = count_match / total_messages_text if total_messages_text else 0
    density_percent_text = round(density_text * 100, 6)

    days_span = (newest_date - oldest_date).days if newest_date and oldest_date else 0
    message_per_day = total_messages_all / days_span if days_span > 0 else total_messages_all

    metrix = {
        "chat_id": chat_id,
        "newest_date": newest_date,
        "oldest_date": oldest_date,
        "total_messages_all": total_messages_all,
        "total_messages_text": total_messages_text,
        "count_match": count_match,
        "unique_authors": unique_authors,
        "keyword_hits": keyword_hits,
        "density_all": density_all,
        "density_percent_all": density_percent_all,
        "density_text": density_text,
        "density_percent_text": density_percent_text,
        "days_span": days_span,
        "message_per_day": message_per_day,
        "author_diversity_ratio": author_diversity_ratio
    }

    decision = decision_engine(metrix, config)
    log_chat_analysis(chat_id, metrix, decision)

    return decision

def decision_engine(metrix: dict, config: dict) -> dict:
    """

    :param metrix: accept metrix drom analyze_chat
    :param config: accept configuration settings
    :return: return the final verdict

    """

    MIN_DENSITY = config["MIN_DENSITY"]
    MIN_MATCH_MESSAGES = config["MIN_MATCH_MESSAGES"]
    MIN_UNIQUE_AUTHORS = config["MIN_UNIQUE_AUTHORS"]

    score = 0
    if metrix["density_text"] >= MIN_DENSITY:
        score += 2
    if metrix["density_all"] >= MIN_DENSITY:
        score += 1
    if metrix["count_match"] >= MIN_MATCH_MESSAGES:
        score += 2
    if metrix["unique_authors"] >= MIN_UNIQUE_AUTHORS:
        score += 2
    if metrix["days_span"] <= 90:
        score += 1
    if metrix["message_per_day"] >= 50:
        score += 1
    if metrix["author_diversity_ratio"] > 0.1:
        score += 1

    if score >= 7:
        verdict = "READ"
    elif score >= 4:
        verdict = "REVIEW"
    else:
        verdict = "SKIP"

    decision = {
        "score": score,
        "verdict": verdict
    }

    return decision



def log_chat_analysis(chat_id: str, metrix: dict, decision: dict) -> None:
    logger.info(
        f"[MATCH][{chat_id}]\n"
        f"newest_date: {metrix['newest_date']}\n"
        f"oldest_date: {metrix['oldest_date']}\n"
        f"total_messages_all: {metrix['total_messages_all']}\n"
        f"total_messages_text: {metrix['total_messages_text']}\n"
        f"count_match: {metrix['count_match']}\n"
        f"unique_authors: {metrix['unique_authors']}\n"
        f"keyword_hits: {metrix['keyword_hits']}\n"
        f"density_percent_all: {metrix['density_percent_all']}%\n"
        f"density_percent_text: {metrix['density_percent_text']}%\n"
        f"days_span: {metrix['days_span']}\n"
        f"message_per_day: {metrix['message_per_day']}\n"
        f"author_diversity_ratio: {metrix['author_diversity_ratio']}\n"
        f"Chat score: {decision['score']}/10\n"
        f"verdict: {decision['verdict']}"
    )
    logger.info(
        f"[DECISION][{chat_id}] "
        f"score={decision['score']} "
        f"verfict={decision['verdict']}\n"
    )
