from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from bot.database.methods.select import get_admin_data, is_user_admin, get_user_support_room_state
from bot.database.methods.update import update_admin_support_chat_state, update_user_support_state

from bot.keyboards import KB_END_CHAT, KB_SUPPORT_MENU_USER_END

import os
from dotenv import load_dotenv # For local use only

load_dotenv() # For local use only


ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')

class SupportChatAdmin(StatesGroup):
    support_chat_admin = State()


async def __process_support_chat_connection(message: types.Message):
    """
    Processing admin connection to support chat
    """

    bot = message.bot
    chat_id = message.from_user.id

    user_chat_id = message.get_args()
    if user_chat_id != None and await is_user_admin(chat_id):
        if await get_user_support_room_state(user_chat_id) == 1:
            await update_user_support_state(user_chat_id, 2)
            await update_admin_support_chat_state(chat_id, user_chat_id)

            await bot.send_message(user_chat_id, f"Оператор під'єднався до чату!", parse_mode="HTML")
            await bot.send_message(chat_id, f"Ви були з'єднані з користувачем", reply_markup=KB_END_CHAT, parse_mode="HTML")

            await SupportChatAdmin.support_chat_admin.set()
        else:
            await bot.send_message(chat_id, f"Користувач відмінив запит або інший адміністратор йому помагає", parse_mode="HTML")


async def __process_support_chat_end(message: types.Message, state: FSMContext):
    """
    Processing admin end of support chat
    """

    bot = message.bot
    chat_id = message.from_user.id


    if await is_user_admin(chat_id):
        user_chat_id = (await get_admin_data(chat_id))["support_chat"]
        try:
            await update_user_support_state(user_chat_id, 0)
            await bot.send_message(user_chat_id, f"Оператор від'єднався від чату! Завершіть сеанс, щоб повернутись до головного меню", reply_markup=KB_SUPPORT_MENU_USER_END, parse_mode="HTML")
        except:
            pass
        await bot.send_message(chat_id, f"Ви були роз'єднані з користувачем", reply_markup=ReplyKeyboardRemove(), parse_mode="HTML")
        await update_admin_support_chat_state(chat_id, None)

        await state.finish()


async def __send_text_message_to_user(message: types.Message):
    """
    Send text message to user
    """  

    bot = message.bot
    chat_id = message.from_user.id

    admin_user = await get_admin_data(chat_id)
    user_chat_id = admin_user["support_chat"]

    if user_chat_id != None:
        await bot.send_message(user_chat_id, message.text, parse_mode="HTML")
    else:
        await bot.send_message(chat_id, "Користувач від'єднався!")


def register_admin_support_handlers(dp: Dispatcher):

    # Message handlers

    dp.register_message_handler(__process_support_chat_connection, commands=["start_chat"])
    dp.register_message_handler(__process_support_chat_end, content_types=['text'], text="Закінчити переписку", state=SupportChatAdmin.support_chat_admin)
    dp.register_message_handler(__send_text_message_to_user, content_types=['text'], state=SupportChatAdmin.support_chat_admin)