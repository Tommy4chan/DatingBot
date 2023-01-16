from aiogram import Dispatcher, types
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup, any_state
from aiogram.dispatcher import FSMContext

from bot.database.methods.select import is_user_currently_in_support_chat, get_user_support_room_state
from bot.database.methods.update import update_admin_support_chat_state, update_user_support_state

from bot.handlers.user.back_button_handler import __back_to_main_menu_manual

import os
from dotenv import load_dotenv # For local use only

load_dotenv() # For local use only


ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')

class SupportChatUser(StatesGroup):
    support_chat_user = State()


async def __end_support_chat(query: CallbackQuery, state: FSMContext):
    """
    End or exit support chat
    """

    bot = query.bot
    chat_id = query.from_user.id

    admin_user = await is_user_currently_in_support_chat(chat_id)

    await update_user_support_state(chat_id, 0)

    if len(admin_user):
        await bot.send_message(chat_id, f"Чат завершено!", parse_mode="HTML")
        try:
            await bot.send_message(admin_user[0]["telegram_id"], f"Користувач покинув чат!", parse_mode="HTML")
            await update_admin_support_chat_state(admin_user[0]["telegram_id"], None)
        except:
            pass
        await state.finish()
        await __back_to_main_menu_manual(query)
    else:
        await __back_to_main_menu_manual(query)
        try:
            await state.finish()
        except:
            pass


async def __start_support_chat(query: CallbackQuery):
    """
    Start support chat
    """  

    bot = query.bot
    chat_id = query.from_user.id

    await bot.send_message(ADMIN_CHAT_ID, f"Користувач звернувся в тех. підтримку, відкрити чат з ним /start_chat {chat_id}", parse_mode="HTML")
    await bot.send_message(chat_id, f"Зачекайте поки оператор під'єднається до чату", parse_mode="HTML")

    await update_user_support_state(chat_id, 1)

    await SupportChatUser.support_chat_user.set()


async def __send_text_message_to_admin(message: types.Message):
    """
    Send text message to admin
    """  

    bot = message.bot
    chat_id = message.from_user.id

    admin_user = await is_user_currently_in_support_chat(chat_id)

    if len(admin_user):
        admin_chat_id = admin_user[0]["telegram_id"]
        await bot.send_message(admin_chat_id, message.text, parse_mode="HTML")
    else:
        await bot.send_message(chat_id, "Зачекайте, оператор ще не під'єднався до чату")


async def __send_photo_message_to_admin(message: types.Message):
    """
    Send photo message to admin
    """  

    bot = message.bot
    chat_id = message.from_user.id

    admin_user = await is_user_currently_in_support_chat(chat_id)

    if len(admin_user):
        admin_chat_id = admin_user[0]["telegram_id"]
        await bot.send_photo(admin_chat_id, message.photo[-1].file_id, caption=message.caption, parse_mode="HTML")
    else:
        await bot.send_message(chat_id, "Зачекайте, оператор ще не під'єднався до чату")


def register_support_handlers(dp: Dispatcher):

    # Message handlers
    dp.register_message_handler(__send_text_message_to_admin, content_types=['text'], state=SupportChatUser.support_chat_user)
    dp.register_message_handler(__send_photo_message_to_admin, content_types=['photo'], state=SupportChatUser.support_chat_user)

    # Callback handlers
    dp.register_callback_query_handler(__start_support_chat, text="start_support_chat")
    dp.register_callback_query_handler(__end_support_chat, text="end_support_chat", state=any_state)