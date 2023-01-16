from aiogram import Dispatcher
from aiogram.types import CallbackQuery

from bot.keyboards import KB_QUESTIONNAIRE_MENU, KB_FILTERS_MENU, KB_SUPPORT_MENU_USER
from bot.utils.main import get_questionnaire, delete_old_message, format_filters_data, add_age_filter_ending
from bot.utils.questionnaire import get_other_questionnaire

from bot.database.methods.select import get_user_data


@delete_old_message
async def __user_questionnaire(query: CallbackQuery):
    """
    Show user questionnaire and questionnaire menu
    """

    bot = query.bot
    chat_id = query.from_user.id

    user_data = await get_user_data(chat_id)

    await bot.send_photo(chat_id, caption=await get_questionnaire(user_data, 1), photo=str(user_data['photo_id']), reply_markup=KB_QUESTIONNAIRE_MENU, parse_mode="HTML")


@delete_old_message
async def __user_filters(query: CallbackQuery):
    """
    Show user questionnaire and questionnaire menu
    """

    bot = query.bot
    chat_id = query.from_user.id
    
    user_data = await format_filters_data(await get_user_data(chat_id))

    await bot.send_message(chat_id, f"Фільтр з підбору партнерів:\n\n🚻 Необхідна стать партнера: {user_data[0]}\n🔞 Віковий діапазон: {user_data[1]} - {await add_age_filter_ending(user_data[2])}\n🏙️ Місто партнера: {user_data[3]}", reply_markup=KB_FILTERS_MENU, parse_mode="HTML")


@delete_old_message
async def __find_target(query: CallbackQuery):
    """
    Show other questionnaires
    """

    await get_other_questionnaire(query)


@delete_old_message
async def __support(query: CallbackQuery):
    """
    Show support menu
    """

    bot = query.bot
    chat_id = query.from_user.id

    await bot.send_message(chat_id, f"Хочете зв'язатися з техпідтримкою? Натисніть на кнопку нижче!", reply_markup=KB_SUPPORT_MENU_USER, parse_mode="HTML")



def register_menu_handlers(dp: Dispatcher):

    # Callback handlers
    dp.register_callback_query_handler(__user_questionnaire, text="my_questionnaire")
    dp.register_callback_query_handler(__user_filters, text="filters")
    dp.register_callback_query_handler(__find_target, text="find")
    dp.register_callback_query_handler(__support, text="support")
