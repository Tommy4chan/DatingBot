from aiogram import Dispatcher, types
from aiogram.types import CallbackQuery, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot.keyboards import KB_GET_PHONE_NUMBER, KB_CHANGE_QUESTIONNAIRE_MENU
from bot.utils.main import delete_old_message, validate_instagram

from bot.database.methods.select import get_user_data
from bot.database.methods.other import verify_user
from bot.database.methods.update import update_user_instagram
from bot.database.methods.delete import delete_user
from bot.handlers.user.back_button_handler import __back_to_main_menu_manual


class Verify(StatesGroup):
    phone = State()

class Instagram(StatesGroup):
    inst = State()


@delete_old_message
async def __verify_user(query: CallbackQuery):
    """
    Start user verifying
    """

    bot = query.bot
    chat_id = query.from_user.id

    user_data = await get_user_data(chat_id)

    if user_data["is_verified"] == True:
        await bot.send_message(chat_id, f"Ваш профіль уже підтверджено!", reply_markup=ReplyKeyboardRemove(), parse_mode="HTML")
        await __back_to_main_menu_manual(query)
    else:
        await Verify.phone.set()
        await bot.send_message(chat_id, "Щоб пройти верифікацію вам потрібно надіслати свій контакт:", reply_markup=KB_GET_PHONE_NUMBER, parse_mode="HTML")


async def __process_phone_number(message: types.Message, state: FSMContext):
    """
    Process user phone to verify user
    """

    bot = message.bot
    chat_id = message.from_user.id

    user_data = await get_user_data(chat_id)

    phone_number = message.contact.phone_number
    await verify_user(chat_id, phone_number)
    await bot.send_message(chat_id, f"Дякую, {user_data['name']}\nВаш номер {phone_number} було отримано", reply_markup=ReplyKeyboardRemove(), parse_mode="HTML")
    await __back_to_main_menu_manual(message)
    await state.finish()


@delete_old_message
async def __add_instagram(query: CallbackQuery):
    """
    Add instagram to user
    """

    bot = query.bot
    chat_id = query.from_user.id

    await Instagram.inst.set()
    await bot.send_message(chat_id, f"Напишіть ім'я свого акаунта:\n\nПриклади:\n@username\nhttps://www.instagram.com/username", reply_markup=ReplyKeyboardRemove(), parse_mode="HTML")


async def __process_instagram(message: types.Message, state: FSMContext):
    """
    Process instagram account
    """

    bot = message.bot
    chat_id = message.from_user.id

    instagram = await validate_instagram(message.text)

    if not instagram:
        await bot.send_message(chat_id, f"Ваш акаунт недобавлено, можливо Ви ввели щось не так? Спробуйте ще раз", reply_markup=ReplyKeyboardRemove(), parse_mode="HTML")
    else:
        await update_user_instagram(chat_id, instagram) 
        await bot.send_message(chat_id, f"Ваш акаунт успішно добавлено", reply_markup=ReplyKeyboardRemove(), parse_mode="HTML")
        await state.finish()
        await __back_to_main_menu_manual(message)
        


@delete_old_message
async def __change_questionnaire(message: types.Message):
    """
    Change questionnaire data
    """

    bot = message.bot
    chat_id = message.from_user.id

    await bot.send_message(chat_id, f"Виберіть, що ви хочете змінити:", reply_markup=KB_CHANGE_QUESTIONNAIRE_MENU, parse_mode="HTML")


@delete_old_message
async def __delete_questionnaire(message: types.Message):
    """
    Delete user account
    """

    bot = message.bot
    chat_id = message.from_user.id

    await delete_user(chat_id)

    await bot.send_message(chat_id, f"Ви видалили свій акаунт")


def register_questionnaire_menu_handlers(dp: Dispatcher):

    # Message handlers

    #dp.register_message_handler(__user_questionnaire, commands=["user"])
    dp.register_message_handler(__process_phone_number, content_types=['contact'], state=Verify.phone)
    dp.register_message_handler(__process_instagram, content_types=['text'], state=Instagram.inst)
    #dp.register_message_handler(__new_poweroff_schedule, content_types=['text'], text="Графік відключень🕔")

    # Callback handlers
    dp.register_callback_query_handler(__verify_user, text="verify")
    dp.register_callback_query_handler(__add_instagram, text="instagram")
    dp.register_callback_query_handler(__change_questionnaire, text="change_questionnaire")
    dp.register_callback_query_handler(__delete_questionnaire, text="delete_questionnaire")
    #dp.register_callback_query_handler(__select_another_day, Text(startswith='weekday_'))
    #dp.register_callback_query_handler(__change_notification_state, Text(startswith='notification_'))
    #dp.register_callback_query_handler(__what_is_notification, Text(startswith='what_is_notification'))
    #dp.register_callback_query_handler(__developer, Text(startswith='developer'))
    #dp.register_callback_query_handler(__donate, Text(startswith='donate'))