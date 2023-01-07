from aiogram import Dispatcher

from bot.handlers.user import register_regestration_handlers


def register_all_handlers(dp: Dispatcher):
    register_regestration_handlers(dp)
