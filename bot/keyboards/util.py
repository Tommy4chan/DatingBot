from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def get_questionnaire_answear_keyboard(user_data):
    kb_questionnaire_answear = InlineKeyboardMarkup(2)
    kb_questionnaire_answear.add(
        InlineKeyboardButton("👍", callback_data=f"like_{user_data['telegram_id']}"),
        InlineKeyboardButton("👎", callback_data="dislike_answear"),
    )
    return kb_questionnaire_answear