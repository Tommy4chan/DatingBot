from typing import Final
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

KB_GET_LOCATION: Final = ReplyKeyboardMarkup(1, resize_keyboard=True)
KB_GET_LOCATION.add(
    KeyboardButton("Поділитись місцезнаходження", request_location=True),
)


KB_GET_PHONE_NUMBER: Final = ReplyKeyboardMarkup(1, resize_keyboard=True)
KB_GET_PHONE_NUMBER.add(
    KeyboardButton("Поділитись номер", request_contact=True),
)


KB_END_CHAT: Final = ReplyKeyboardMarkup(1, resize_keyboard=True)
KB_END_CHAT.add(
    KeyboardButton("Закінчити переписку"),
)