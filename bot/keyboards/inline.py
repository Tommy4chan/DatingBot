from typing import Final
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

KB_CONTINUE_REGISTRATION: Final = InlineKeyboardMarkup(1)
KB_CONTINUE_REGISTRATION.add(
    InlineKeyboardButton("Продовжити", callback_data="continue_regestration")
)

KB_GENDER_SELECTION: Final = InlineKeyboardMarkup(2)
KB_GENDER_SELECTION.add(
    InlineKeyboardButton("🙎‍♂️ Чоловік", callback_data="gender_male"),
    InlineKeyboardButton("🙎‍♀️ Жінка", callback_data="gender_female")
)

KB_CHOOSE_YES_OR_NOT: Final = InlineKeyboardMarkup(2)
KB_CHOOSE_YES_OR_NOT.add(
    InlineKeyboardButton("Так", callback_data="yes"),
    InlineKeyboardButton("НІ", callback_data="no")
)

KB_MENU: Final = InlineKeyboardMarkup(2)
KB_MENU.add(
    InlineKeyboardButton("👤️ Моя анкета", callback_data="my_questionnaire"),
    InlineKeyboardButton("⚙️ Фільтри", callback_data="filters"),
    InlineKeyboardButton("💌 Знайти пару", callback_data="find"),
    InlineKeyboardButton("🆘 Підтримка", callback_data="support")
)