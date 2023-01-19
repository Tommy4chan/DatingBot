from aiogram import Dispatcher, types

from bot.database.methods.select import is_user_admin, get_all_users
from bot.database.methods.update import update_user_ban_state
from bot.database.methods.insert import set_user_admin_role


async def __ban(message: types.Message):
    """
    Ban user by chat_id
    """

    bot = message.bot
    chat_id = message.from_user.id

    user_id = message.get_args()

    if await is_user_admin(chat_id) and len(user_id) != 0:
        await update_user_ban_state(user_id, 1)
        await bot.send_message(chat_id, f'Користувач заблокований')

async def __admin(message: types.Message):
    """
    Set user as admin by chat_id
    """

    bot = message.bot
    chat_id = message.from_user.id

    user_id = message.get_args()

    if await is_user_admin(chat_id) and len(user_id) != 0:
        if await is_user_admin(user_id):
            await bot.send_message(chat_id, f'Користувач вже є адміністратором')
        else:
            await set_user_admin_role(user_id, 1)
            await bot.send_message(chat_id, f'Користувач назначений аміністратором')


async def __send_message_to_user(message: types.Message):
    """
    Send message to user by chat_id
    """

    bot = message.bot
    chat_id = message.from_user.id

    user_id = message.get_args().split(" ", 1)[0]

    message_text = message.get_args().split(" ", 1)[1]

    if await is_user_admin(chat_id) and len(user_id) != 0:
        try:
            await bot.send_message(user_id, message_text)
        except:
            await bot.send_message(chat_id, "Повідомлення не надіслано, щось пішло не так")


async def __send_message_to_all_users(message: types.Message):
    """
    Send message to all users
    """

    bot = message.bot
    chat_id = message.from_user.id

    message_text = message.get_args()

    if await is_user_admin(chat_id):
        for user in await get_all_users():
            try:
                await bot.send_message(user['telegram_id'], message_text)
            except:
                pass


def register_admin_tools_handlers(dp: Dispatcher):

    # Message handlers
    
    dp.register_message_handler(__ban, commands=["ban"])
    dp.register_message_handler(__admin, commands=["admin"])
    dp.register_message_handler(__send_message_to_user, commands=["send"])
    dp.register_message_handler(__send_message_to_all_users, commands=["send_all"])
