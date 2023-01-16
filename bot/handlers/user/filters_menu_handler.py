from aiogram import Dispatcher, types
from aiogram.types import CallbackQuery, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot.keyboards import KB_GENDER_SELECTION, KB_CHOOSE_YES_OR_NOT, KB_GET_LOCATION
from bot.utils.main import delete_old_message, decode_callback_data, get_location_by_coordinates, get_location_by_name

from bot.database.methods.update import update_target_city, update_target_age, update_target_gender
from bot.handlers.user.back_button_handler import __back_to_main_menu_manual


class FilterCity(StatesGroup):
    location = State()

class FilterGender(StatesGroup):
    gender = State()

class FilterAge(StatesGroup):
    age_min = State()
    age_max = State()


@delete_old_message
async def __change_target_location(query: CallbackQuery):
    """
    Change user location
    """

    bot = query.bot
    chat_id = query.from_user.id

    await FilterCity.location.set()
    await bot.send_message(chat_id, "Напишіть місто вашого майбутнього партнера:", reply_markup=KB_GET_LOCATION, parse_mode="HTML")


async def __process_target_location_change(message: types.Message, state: FSMContext):
    """
    Process user location
    """

    bot = message.bot
    chat_id = message.from_user.id
    
    user_location = await get_location_by_coordinates(message.location.latitude, message.location.longitude)

    await state.update_data(location=user_location)

    await bot.send_message(chat_id, f"{user_location} - це ваш населений пункт?", reply_markup=KB_CHOOSE_YES_OR_NOT)


async def __location_target_change_correct(query: CallbackQuery, state: FSMContext):
    """
    Called if location correct
    """

    bot = query.bot
    chat_id = query.from_user.id

    await update_target_city(chat_id, (await state.get_data())["location"])

    await bot.send_message(chat_id, f"Ви успішно додали інформацію про населений пункт", reply_markup=ReplyKeyboardRemove())
    await state.finish()
    await query.answer()
    await __back_to_main_menu_manual(query)


async def __location_target_change_incorrect(query: CallbackQuery):
    """
    Called if location incorrect
    """

    bot = query.bot
    chat_id = query.from_user.id
    
    await bot.send_message(chat_id, f"Спробуйте надіслати назву населеного пункту")
    await query.answer()


async def __find_location_target_by_name_change(message: types.Message, state: FSMContext):
    """
    Called to find location by name
    """

    bot = message.bot
    chat_id = message.from_user.id

    user_location = await get_location_by_name(message.text)

    await state.update_data(location=user_location)
    
    if user_location == 'not found':
        await bot.send_message(chat_id, "Вашого населеного пункту не знайдено, спробуйте ще раз")
    else:
        await bot.send_message(chat_id, f"{user_location} - це ваш населений пункт?", reply_markup=KB_CHOOSE_YES_OR_NOT)

@delete_old_message
async def __filter_change_age(query: CallbackQuery):
    """
    Change user target age
    """

    bot = query.bot
    chat_id = query.from_user.id

    await FilterAge.age_min.set()
    await bot.send_message(chat_id, "Напишіть мінімальний вік:", parse_mode="HTML")


async def __filter_process_age_change_invalid(message: types.Message):
    """
    If age is invalid
    """

    bot = message.bot
    chat_id = message.from_user.id

    await bot.send_message(chat_id, "Вік повинен бути числом!")


async def __filter_process_age_change_out_of_range(message: types.Message):
    """
    If age is out of range
    """

    bot = message.bot
    chat_id = message.from_user.id

    await bot.send_message(chat_id, "Вік повинен бути в межах від 16 до 50!")


async def __filter_process_age_min_change(message: types.Message, state: FSMContext):
    """
    Process user target age min change
    """

    bot = message.bot
    chat_id = message.from_user.id

    await state.update_data(age_min=int(message.text))
    await FilterAge.next()
    await bot.send_message(chat_id, "Дані збережено, тепер введіть максимальний вік:")


async def __filter_process_age_max_change(message: types.Message, state: FSMContext):
    """
    Process user target age max change
    """

    bot = message.bot
    chat_id = message.from_user.id

    await state.update_data(age_max=int(message.text))
    age_data = await state.get_data()

    if int(age_data["age_min"]) > int(age_data["age_max"]):
        await bot.send_message(chat_id, "Максимальний вік повинен бути більше мінімального, або рівним мінімальному. Введіть максимальний вік ще раз")
    else:
        await update_target_age(chat_id, int(age_data["age_min"]), 1)
        await update_target_age(chat_id, int(age_data["age_max"]), 0)
        await state.finish()
        await bot.send_message(chat_id, "Дані збережено")
        await __back_to_main_menu_manual(message)


@delete_old_message
async def __change_targer_gender_filter(query: CallbackQuery):
    """
    Change user targer gender
    """

    bot = query.bot
    chat_id = query.from_user.id

    await FilterGender.gender.set()
    await bot.send_message(chat_id, "Виберіть, кого ви хочете знайти:", reply_markup=KB_GENDER_SELECTION)


async def __process_targer_gender_filter(query: CallbackQuery, state: FSMContext):
    """
    Process user targer gender
    """

    bot = query.bot
    chat_id = query.from_user.id

    await update_target_gender(chat_id, await decode_callback_data(query))

    await state.finish()
    await bot.send_message(chat_id, "Дані збережено")
    await query.answer()
    await __back_to_main_menu_manual(query)

def register_filter_menu_handlers(dp: Dispatcher):

    # Message handlers
    dp.register_message_handler(__process_target_location_change, content_types=['location'], state=FilterCity.location)
    dp.register_message_handler(__find_location_target_by_name_change, content_types=['text'], state=FilterCity.location)
    dp.register_message_handler(__filter_process_age_change_invalid, lambda message: not message.text.isdigit(), state=FilterAge)
    dp.register_message_handler(__filter_process_age_change_out_of_range, lambda message: int(message.text) < 16 or int(message.text) > 50, state=FilterAge)
    dp.register_message_handler(__filter_process_age_min_change, lambda message: message.text.isdigit(), state=FilterAge.age_min)
    dp.register_message_handler(__filter_process_age_max_change, lambda message: message.text.isdigit(), state=FilterAge.age_max)

    # Callback handlers
    dp.register_callback_query_handler(__change_target_location, text="targer_city")
    dp.register_callback_query_handler(__filter_change_age, text="target_age")
    dp.register_callback_query_handler(__change_targer_gender_filter, text="target_gender")
    dp.register_callback_query_handler(__location_target_change_correct, text="yes", state=FilterCity.location)
    dp.register_callback_query_handler(__location_target_change_incorrect, text="no", state=FilterCity.location)
    dp.register_callback_query_handler(__process_targer_gender_filter,Text(startswith="gender_"), state=FilterGender.gender)
