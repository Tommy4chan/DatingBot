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

KB_QUESTIONNAIRE_MENU: Final = InlineKeyboardMarkup(2)
KB_QUESTIONNAIRE_MENU.add(
    InlineKeyboardButton("✅ Верифікація", callback_data="verify"),
    InlineKeyboardButton("⚙️ Змінити анкету", callback_data="change_questionnaire"),
    InlineKeyboardButton("📸 Інстаграм", callback_data="instagram"),
    InlineKeyboardButton("🚫 Видалити анкету", callback_data="delete_questionnaire"),
    InlineKeyboardButton("🔙 Назад", callback_data="back")
)

KB_CHANGE_QUESTIONNAIRE_MENU: Final = InlineKeyboardMarkup(2)
KB_CHANGE_QUESTIONNAIRE_MENU.add(
    InlineKeyboardButton("Ім'я", callback_data="change_name"),
    InlineKeyboardButton("Стать", callback_data="change_gender"),
    InlineKeyboardButton("Вік", callback_data="change_age"),
    InlineKeyboardButton("Місто", callback_data="change_location"),
    InlineKeyboardButton("Фото", callback_data="change_photo"),
    InlineKeyboardButton("Про себе", callback_data="change_description"),
    InlineKeyboardButton("🔙 Назад", callback_data="back")
)

KB_FILTERS_MENU: Final = InlineKeyboardMarkup(2)
KB_FILTERS_MENU.add(
    InlineKeyboardButton("🏙️️ Місто партнера", callback_data="targer_city"),
    InlineKeyboardButton("🚻 Стать партнера", callback_data="target_gender"),
    InlineKeyboardButton("🔞 Віковий діапазон", callback_data="target_age"),
    InlineKeyboardButton("🔙 Назад", callback_data="back")
)

KB_QUESTIONNAIRE_REVIEW: Final = InlineKeyboardMarkup(2)
KB_QUESTIONNAIRE_REVIEW.add(
    InlineKeyboardButton("👍", callback_data="like"),
    InlineKeyboardButton("👎", callback_data="dislike"),
    InlineKeyboardButton("🔙 Назад", callback_data="back")
)

KB_SUPPORT_MENU_USER: Final = InlineKeyboardMarkup(1)
KB_SUPPORT_MENU_USER.add(
    InlineKeyboardButton("Написати оператору", callback_data="start_support_chat"),
    InlineKeyboardButton("Завершити сеанс", callback_data="end_support_chat"),
)

KB_SUPPORT_MENU_USER_END: Final = InlineKeyboardMarkup(1)
KB_SUPPORT_MENU_USER_END.add(
    InlineKeyboardButton("Завершити сеанс", callback_data="end_support_chat"),
)