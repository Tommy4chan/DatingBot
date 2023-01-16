from bot.database.methods.insert import create_user
from bot.database.methods.select import is_user_registered, is_user_verified, get_user_data
from bot.database.methods.update import update_user_phone
from bot.database.methods.delete import delete_user


async def register_user(telegram_id, username):
    user_data = await get_user_data(telegram_id)
    if user_data != None:
        if user_data['is_active'] == 0:
            await delete_user(telegram_id)
        else:
            return False
    await create_user(telegram_id, username)
    return True


async def verify_user(telegram_id, phone_number):
    if not await is_user_verified(telegram_id):
        await update_user_phone(telegram_id, phone_number)
        return True
    else:
        return False