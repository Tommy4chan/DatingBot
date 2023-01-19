from aiogram import Dispatcher, types
from aiogram.types import CallbackQuery, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import time

from bot.keyboards import KB_CONTINUE_REGISTRATION, KB_GENDER_SELECTION, KB_GET_LOCATION, KB_CHOOSE_YES_OR_NOT, KB_MENU
from bot.utils.main import decode_callback_data, get_location_by_coordinates, get_location_by_name, get_questionnaire

from bot.database.methods.update import update_user_name, update_user_gender, update_user_age, update_user_location, update_user_photo,\
                                        update_user_description, update_target_gender, update_account_active_status, update_target_city,\
                                        update_user_coordinates
from bot.database.methods.select import get_user_data, is_user_admin
from bot.database.methods.other import register_user
from bot.database.methods.insert import create_fake_user


class Form(StatesGroup):
    chat_id = State() # Will be represented in storage as 'Form:chat_id'
    name = State()  # Will be represented in storage as 'Form:name'
    gender = State()  # Will be represented in storage as 'Form:gender'
    age = State()  # Will be represented in storage as 'Form:age'
    target_gender = State() # Will be represented in storage as 'Form:targer'
    location = State() # Will be represented in storage as 'Form:location'
    description = State() # Will be represented in storage as 'Form:description'
    photo = State() # Will be represented in storage as 'Form:description'

async def __fake_registration(message: types.Message):
    """
    Conversation's entry point
    """

    bot = message.bot
    chat_id = message.from_user.id
    
    if await is_user_admin(chat_id):
        await Form.chat_id.set()
        state = Dispatcher.get_current().current_state()
        await state.update_data(chat_id=(int(time.time())))
        print(state)
        await create_fake_user((await state.get_data())["chat_id"])
        await Form.next()
        await bot.send_message(chat_id, "Реєстрація фейкової анкети розпочата", reply_markup=KB_CONTINUE_REGISTRATION)

async def __start(message: types.Message):
    """
    Conversation's entry point
    """

    bot = message.bot
    chat_id = message.from_user.id

    await Form.chat_id.set()
    state = Dispatcher.get_current().current_state()
    await state.update_data(chat_id=chat_id)
    await Form.next()

    if await register_user(chat_id, message.from_user.username):
        await bot.send_message(chat_id, "Привіт, я допоможу тобі знайти ідеальну пару, для цього заповни свою анкету щоб почати знайомитися 👩❤️👨...", reply_markup=KB_CONTINUE_REGISTRATION)
    else:
        await state.finish()
        user_data = await get_user_data(chat_id)
        await bot.send_photo(chat_id, caption=await get_questionnaire(user_data, 0), photo=str(user_data['photo_id']), reply_markup=KB_MENU, parse_mode="HTML")


async def __continue_regestration(query: CallbackQuery):
    """
    Start of registration
    """

    bot = query.bot
    chat_id = query.from_user.id

    await bot.send_message(chat_id, "Напишіть мені ваше ім'я, яке усі будуть бачити в анкеті")
    await query.answer()


async def __register_name(message: types.Message, state: FSMContext):
    """
    Process user name
    """

    bot = message.bot
    chat_id = message.from_user.id

    await update_user_name((await state.get_data())["chat_id"], message.text)
    
    await Form.next()
    await bot.send_message(chat_id, "Чудово, ваше ім'я записано!")
    await bot.send_message(chat_id, "Вкажіть свою стать:", reply_markup=KB_GENDER_SELECTION)


async def __register_name_invalid(message: types.Message):
    """
    Process user name
    """

    bot = message.bot
    chat_id = message.from_user.id

    await bot.send_message(chat_id, "Ім'я не повинне бути довше 64 символів!")


async def __register_gender(query: CallbackQuery, state: FSMContext):
    """
    Process user gender
    """
    bot = query.bot
    chat_id = query.from_user.id

    await update_user_gender((await state.get_data())["chat_id"], await decode_callback_data(query))
    
    await Form.next()
    await bot.send_message(chat_id, "Вашу стать вказано!")
    await bot.send_message(chat_id, "Введіть скільки вам років:")
    await query.answer()


async def __process_age_invalid(message: types.Message):
    """
    If age is invalid
    """

    bot = message.bot
    chat_id = message.from_user.id

    await bot.send_message(chat_id, "Вік повинен бути числом!\nВведіть скільки Вам років:")


async def __process_age_out_of_range(message: types.Message):
    """
    If age is out of range
    """

    bot = message.bot
    chat_id = message.from_user.id

    await bot.send_message(chat_id, "Вік повинен бути в межах від 16 до 50!\nВведіть скільки Вам років:")


async def __process_age(message: types.Message, state: FSMContext):
    """
    Process user age
    """

    bot = message.bot
    chat_id = message.from_user.id

    await update_user_age((await state.get_data())["chat_id"], int(message.text))

    await Form.next()
    await bot.send_message(chat_id, "Чудово, вік зазначено!")
    await bot.send_message(chat_id, "Зараз виберіть кого ви хочете знайти?", reply_markup=KB_GENDER_SELECTION)


async def __process_targer_gender(query: CallbackQuery, state: FSMContext):
    """
    Process user targer gender
    """

    bot = query.bot
    chat_id = query.from_user.id

    await update_target_gender((await state.get_data())["chat_id"], await decode_callback_data(query))

    await Form.next()
    await bot.send_message(chat_id, "Чудово! Дані записані!")
    await bot.send_message(chat_id, "Введіть місто, в якому проживаєте. Для точного визначення місця розташування, можете натиснути на кнопку нижче!:", reply_markup=KB_GET_LOCATION)
    await query.answer()

async def __process_location(message: types.Message, state: FSMContext):
    """
    Process user location
    """

    bot = message.bot
    chat_id = message.from_user.id
    
    user_location = await get_location_by_coordinates(message.location.latitude, message.location.longitude)
    await update_user_coordinates((await state.get_data())["chat_id"], message.location.latitude, message.location.longitude)
    await state.update_data(location=user_location)

    await bot.send_message(chat_id, f"{user_location} - це ваш населений пункт?", reply_markup=KB_CHOOSE_YES_OR_NOT)


async def __location_correct(query: CallbackQuery, state: FSMContext):
    """
    Called if location correct
    """

    bot = query.bot
    chat_id = query.from_user.id

    await update_user_location((await state.get_data())["chat_id"], (await state.get_data())["location"])
    await update_target_city((await state.get_data())["chat_id"], (await state.get_data())["location"])
    
    await Form.next()
    await bot.send_message(chat_id, f"Ви успішно додали інформацію про населений пункт", reply_markup=ReplyKeyboardRemove())
    await bot.send_message(chat_id, f"Тепер напишіть трохи про себе: (255 символів макс.)")
    await query.answer()


async def __location_incorrect(query: CallbackQuery):
    """
    Called if location incorrect
    """

    bot = query.bot
    chat_id = query.from_user.id
    
    await bot.send_message(chat_id, f"Спробуйте надіслати назву свого населеного пункту")
    await query.answer()


async def __find_location_by_name(message: types.Message, state: FSMContext):
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


async def __process_description_invalid(message: types.Message):
    """
    Called to process description
    """

    bot = message.bot
    chat_id = message.from_user.id

    await bot.send_message(chat_id, f"Опис про себе повинен бути менше 255 символів")


async def __process_description(message: types.Message, state: FSMContext):
    """
    Called to process description
    """

    bot = message.bot
    chat_id = message.from_user.id
    
    await update_user_description((await state.get_data())["chat_id"], message.text)

    await Form.next()
    await bot.send_message(chat_id, f"Ви успішно додали інформацію про себе")
    await bot.send_message(chat_id, f"Останнє, надішліть мені вашу фотографію:")


async def __process_photo(message: types.Message, state: FSMContext):
    """
    Called to process photo
    """

    bot = message.bot
    chat_id = message.from_user.id
    
    await update_user_photo((await state.get_data())["chat_id"], str(message.photo[-1].file_id))
    
    await bot.send_message(chat_id, f"Фото принято!")

    await update_account_active_status((await state.get_data())["chat_id"], 1)

    
    await bot.send_message(chat_id, f"Ура!! 🎉 Реєстрація пройшла успішно! Введіть /help , якщо вам потрібна допомога з ботом. 😎")

    user_data = await get_user_data((await state.get_data())["chat_id"])
    await bot.send_photo(chat_id, caption=await get_questionnaire(user_data, 0), photo=str(user_data['photo_id']), reply_markup=KB_MENU, parse_mode="HTML")
    await state.finish()

def register_regestration_handlers(dp: Dispatcher):

    # Message handlers
    
    dp.register_message_handler(__fake_registration, commands=["register_fake"])
    dp.register_message_handler(__start, commands=["start", "menu"])
    dp.register_message_handler(__register_name, content_types=['text'], state=Form.name)
    dp.register_message_handler(__register_name_invalid, lambda message: len(message.text) > 64, content_types=['text'], state=Form.name)
    dp.register_message_handler(__process_age_invalid, lambda message: not message.text.isdigit(), state=Form.age)
    dp.register_message_handler(__process_age_out_of_range, lambda message: int(message.text) < 16 or int(message.text) > 50, state=Form.age)
    dp.register_message_handler(__process_age, lambda message: message.text.isdigit(), state=Form.age)
    dp.register_message_handler(__process_location, content_types=['location'], state=Form.location)
    dp.register_message_handler(__find_location_by_name, content_types=['text'], state=Form.location)
    dp.register_message_handler(__process_description_invalid, lambda message: len(message.text) > 255, state=Form.description)
    dp.register_message_handler(__process_description, content_types=['text'], state=Form.description)
    dp.register_message_handler(__process_photo, content_types=['photo'], state=Form.photo)

    # Callback handlers

    dp.register_callback_query_handler(__continue_regestration, text="continue_regestration", state=Form.name)
    dp.register_callback_query_handler(__register_gender, Text(startswith='gender_'), state=Form.gender)
    dp.register_callback_query_handler(__process_targer_gender, Text(startswith='gender_'), state=Form.target_gender)
    dp.register_callback_query_handler(__location_correct, text="yes", state=Form.location)
    dp.register_callback_query_handler(__location_incorrect, text="no", state=Form.location)