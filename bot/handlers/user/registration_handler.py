from aiogram import Dispatcher, Bot, types
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from bot.keyboards import KB_CONTINUE_REGISTRATION, KB_GENDER_SELECTION, KB_GET_LOCATION, KB_CHOOSE_YES_OR_NOT
from bot.utils.main import decode_callback_data, get_location_by_coordinates, get_location_by_name


class Form(StatesGroup):
    name = State()  # Will be represented in storage as 'Form:name'
    gender = State()  # Will be represented in storage as 'Form:gender'
    age = State()  # Will be represented in storage as 'Form:age'
    target = State() # Will be represented in storage as 'Form:targer'
    location = State() # Will be represented in storage as 'Form:location'
    description = State() # Will be represented in storage as 'Form:description'
    photo = State() # Will be represented in storage as 'Form:description'


async def __start(message: types.Message):
    """
    Conversation's entry point
    """

    bot = message.bot
    user_id = message.from_user.id

    await bot.send_message(user_id, "Привіт, я допоможу тобі знайти ідеальну пару, для цього заповни свою анкету щоб почати знайомитися 👩❤️👨...", reply_markup=KB_CONTINUE_REGISTRATION)


async def __continue_regestration(message: types.Message):
    """
    Start of regestration
    """

    bot = message.bot
    user_id = message.from_user.id

    await Form.name.set()

    await bot.send_message(user_id, "Напишіть мені ваше ім'я, яке усі будуть бачити в анкеті")


async def __register_name(query: CallbackQuery, state: FSMContext):
    """
    Process user name
    """

    bot = query.bot
    user_id = query.from_user.id

    async with state.proxy() as data:
        data['name'] = query.text
        await bot.send_message(user_id, "Чудово, ваше ім'я записано!")
        

    await Form.next()
    await bot.send_message(user_id, "Вкажіть свою стать:", reply_markup=KB_GENDER_SELECTION)


async def __register_gender(query: CallbackQuery, state: FSMContext):
    """
    Process user gender
    """
    print(1)
    bot = query.bot
    user_id = query.from_user.id
    await Form.next()
    await state.update_data(gender=await decode_callback_data(query))
    await bot.send_message(user_id, "Вашу стать вказано!")
        
    
    await bot.send_message(user_id, "Введіть скільки вам років:")


async def __process_age_invalid(message: types.Message):
    """
    If age is invalid
    """
    return await message.reply("Вік повинен бути числом!\nВведіть скільки Вам років:")


async def __process_age_out_of_range(message: types.Message):
    """
    If age is out of range
    """
    return await message.reply("Вік повинен бути в межах від 16 до 50!\nВведіть скільки Вам років:")


async def __process_age(message: types.Message, state: FSMContext):
    """
    Process user age
    """

    bot = message.bot
    user_id = message.from_user.id

    await state.update_data(age=int(message.text))
    await Form.next()

    await bot.send_message(user_id, "Чудово, вік зазначено!")

    await bot.send_message(user_id, "Зараз виберіть кого ви хочете знайти?", reply_markup=KB_GENDER_SELECTION)


async def __register_targer(query: CallbackQuery, state: FSMContext):
    """
    Process user targer gender
    """

    bot = query.bot
    user_id = query.from_user.id

    await state.update_data(target=decode_callback_data(query))
    await bot.send_message(user_id, "Чудово! Дані записані!")
        
    await Form.next()
    await bot.send_message(user_id, "Введіть місто, в якому проживаєте. Для точного визначення місця розташування, можете натиснути на кнопку нижче!:", reply_markup=KB_GET_LOCATION)


async def __process_location(message: types.Message, state: FSMContext):
    """
    Process user location
    """

    bot = message.bot
    user_id = message.from_user.id
    
    user_location = await get_location_by_coordinates(message.location.latitude, message.location.longitude)

    await state.update_data(location=user_location)
    
    await bot.send_message(user_id, f"{user_location} - це ваше місто?", reply_markup=KB_CHOOSE_YES_OR_NOT)


async def __location_correct(message: types.Message, state: FSMContext):
    """
    Called if location correct
    """

    bot = message.bot
    user_id = message.from_user.id

    await Form.next()
    
    await bot.send_message(user_id, f"Ви успішно додали інформацію про місто")


async def __location_incorrect(message: types.Message, state: FSMContext):
    """
    Called if location incorrect
    """

    bot = message.bot
    user_id = message.from_user.id
    
    await bot.send_message(user_id, f"Спробуйте надіслати назву свого населеного пункту")


async def __find_location_by_name(message: types.Message, state: FSMContext):
    """
    Called if location correct
    """

    bot = message.bot
    user_id = message.from_user.id

    user_location = await get_location_by_name(message.text)
    
    if user_location == 'not found':
        bot.send_message(user_id, "Вашого населеного пункту не знайдено, спробуйте ще раз")

    await bot.send_message(user_id, f"{user_location} - це ваше місто?", reply_markup=KB_CHOOSE_YES_OR_NOT)


def register_regestration_handlers(dp: Dispatcher):

    # Message handlers
    
    dp.register_message_handler(__start, commands=["start"])
    dp.register_message_handler(__register_name, state=Form.name)
    dp.register_message_handler(__process_age_invalid, lambda message: not message.text.isdigit(), state=Form.age)
    dp.register_message_handler(__process_age_out_of_range, lambda message: int(message.text) < 16 or int(message.text) > 50, state=Form.age)
    dp.register_message_handler(__process_age, lambda message: message.text.isdigit(), state=Form.age)
    dp.register_message_handler(__process_location, content_types=['location'], state=Form.location)
    dp.register_message_handler(__find_location_by_name, content_types=['text'], state=Form.location)
    
    #dp.register_message_handler(__new_poweroff_schedule, commands=["schedule"])
    #dp.register_message_handler(__new_poweroff_schedule, content_types=['text'], text="Графік відключень🕔")

    # Callback handlers

    dp.register_callback_query_handler(__continue_regestration, text="continue_regestration")
    dp.register_callback_query_handler(__register_gender, Text(startswith='gender_'), state=Form.gender)
    dp.register_callback_query_handler(__register_targer, Text(startswith='gender_'), state=Form.target)
    dp.register_callback_query_handler(__location_correct, text="yes", state=Form.location)
    dp.register_callback_query_handler(__location_incorrect, text="no", state=Form.location)
    #dp.register_callback_query_handler(__select_another_day, Text(startswith='weekday_'))
    #dp.register_callback_query_handler(__change_notification_state, Text(startswith='notification_'))
    #dp.register_callback_query_handler(__what_is_notification, Text(startswith='what_is_notification'))
    #dp.register_callback_query_handler(__developer, Text(startswith='developer'))
    #dp.register_callback_query_handler(__donate, Text(startswith='donate'))