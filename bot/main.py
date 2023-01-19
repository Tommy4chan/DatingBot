import os
import asyncio
import logging
from aiogram.utils.executor import start_webhook

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.handlers.main import register_all_handlers
from bot.middleware.is_user_exist import IsUserExist
from bot.middleware.last_user_activity import LastUserActivity

from dotenv import load_dotenv # For local use only

load_dotenv() # For local use only

BOT_TOKEN = os.getenv('BOT_TOKEN')
APP_NAME = os.getenv('APP_NAME')

WEBHOOK_HOST = f'https://{APP_NAME}.ondigitalocean.app'
WEBHOOK_PATH = f'/webhook/{BOT_TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)


async def __on_start_up(dp: Dispatcher):
    await dp.bot.set_webhook(WEBHOOK_URL)
    dp.middleware.setup(IsUserExist())
    dp.middleware.setup(LastUserActivity())
    register_all_handlers(dp)
    logging.info("Bot launched!")


def start_local_bot():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot, storage=MemoryStorage())

    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=__on_start_up,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )