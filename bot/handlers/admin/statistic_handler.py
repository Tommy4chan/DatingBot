from aiogram import Dispatcher, types

from bot.database.methods.select import get_new_users_count_by_data, get_active_users_count_by_data, is_user_admin, get_user_count



async def __stats(message: types.Message):
    """
    Show bot statistic
    """

    bot = message.bot
    chat_id = message.from_user.id

    date = message.get_args()

    if await is_user_admin(chat_id) and len(date) != 0:
        new_users = await get_new_users_count_by_data(date)
        active_users = await get_active_users_count_by_data(date)
        total_users = await get_user_count()

        await bot.send_message(chat_id, f'Дата: {date}\n\nНових користувачів: {new_users}\nАктивних користувачів: {active_users}\nЗагалом користувачів: {total_users}')


def register_admin_statisctic_handlers(dp: Dispatcher):

    # Message handlers
    
    dp.register_message_handler(__stats, commands=["stats"])
