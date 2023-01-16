from bot.database.methods.select import get_user_data, get_target_data, get_last_user_id
from bot.database.methods.update import update_last_viewed_user
from bot.handlers.user.back_button_handler import __back_to_main_menu_manual
from bot.utils.main import get_questionnaire, decode_callback_data, create_user_link
from bot.keyboards import KB_QUESTIONNAIRE_REVIEW

import random

async def get_other_questionnaire(message):
    bot = message.bot
    telegram_id = message.from_user.id
    user_data = await get_user_data(telegram_id)
    if int(user_data["last_viewed_user"]) == 0:
        await update_last_viewed_user(telegram_id, random.randint(0, await get_last_user_id()))
        
    target_data = await get_target_data(user_data, 1)
    if target_data != None:
        await bot.send_photo(telegram_id, caption=await get_questionnaire(target_data, 1), photo=str(target_data['photo_id']), reply_markup=KB_QUESTIONNAIRE_REVIEW, parse_mode="HTML")
        await update_last_viewed_user(telegram_id, target_data["id"])
        return target_data
    else:
        target_data = await get_target_data(user_data, 0)
        if target_data != None:
            await update_last_viewed_user(telegram_id, 0)
            await get_other_questionnaire(message)
        else:
            await bot.send_message(telegram_id, "Немає людей, які задовільняють ваші фільтри(")
            await __back_to_main_menu_manual(message)
            return None


async def send_get_questionnaire_answear(query):
    bot = query.bot
    telegram_id = query.from_user.id
    target_id = await decode_callback_data(query)

    user_data = await get_user_data(telegram_id)
    target_data = await get_user_data(target_id)

    await bot.send_message(telegram_id, f"Контактні дані - {await create_user_link(target_data)}", parse_mode="HTML")
    try:
        await bot.send_message(target_id, f"Користувач якого ви лайкнули відповіді взаємністю.\n\nКонтактні дані - {await create_user_link(user_data)}", parse_mode="HTML")
    except:
        pass
        



