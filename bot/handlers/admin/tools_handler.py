from aiogram import Dispatcher, types

from bot.database.methods.select import is_user_admin
from bot.database.methods.update import update_user_ban_state



async def __ban(message: types.Message):
    """
    Show user questionnaire and questionnaire menu
    """

    bot = message.bot
    chat_id = message.from_user.id

    user_id = message.get_args()

    if await is_user_admin(chat_id) and len(user_id) != 0:
        await update_user_ban_state(user_id, 1)
        await bot.send_message(chat_id, f'Користувач заблокований')


def register_admin_tools_handlers(dp: Dispatcher):

    # Message handlers
    
    dp.register_message_handler(__ban, commands=["ban"])
