from typing import Final
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

KB_GET_LOCATION: Final = ReplyKeyboardMarkup(1, resize_keyboard=True)
KB_GET_LOCATION.add(
    KeyboardButton("Поділитись місцезнаходження", request_location=True),
)