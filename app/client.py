import os

from dotenv import load_dotenv
from pyrogram import Client

from app.logger import logger

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

logger.info("Initilizing Telegram client")

app = Client(
    name="userbot",
    api_id=api_id,
    api_hash=api_hash
)
