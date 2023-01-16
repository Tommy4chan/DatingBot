#THIS FILE IS USED ONLY FOR LOCAL DEVELOPMENT

import os
import asyncio
import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.handlers.main import register_all_handlers
from bot.middleware.is_user_exist import IsUserExist
from bot.middleware.last_user_activity import LastUserActivity

from dotenv import load_dotenv # For local use only

load_dotenv() # For local use only


BOT_TOKEN = os.getenv('BOT_TOKEN')
async def __on_start_up(dp: Dispatcher):
    #await update_all_unregistered_active_status('2')
    dp.middleware.setup(IsUserExist())
    dp.middleware.setup(LastUserActivity())
    register_all_handlers(dp)
    logging.info("Bot launched!")


def start_local_bot():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot, storage=MemoryStorage())

    executor.start_polling(dp, skip_updates=True, on_startup=__on_start_up)