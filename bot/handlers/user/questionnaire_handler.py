from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from aiogram.dispatcher.filters import Text

from aiogram.dispatcher.filters.state import any_state
from bot.keyboards import get_questionnaire_answear_keyboard
from bot.utils.main import get_questionnaire, delete_old_message
from bot.utils.questionnaire import get_other_questionnaire, send_get_questionnaire_answear

from bot.database.methods.select import get_user_data, get_user_data_by_id

@delete_old_message
async def __like_target_review(query: CallbackQuery):
    """
    Like other user questionaire as review
    """

    bot = query.bot
    chat_id = query.from_user.id

    user_data = await get_user_data(chat_id)

    await bot.send_message(chat_id, "Ваш лайк надісланий користувачу!")

    target_data = await get_user_data_by_id(user_data["last_viewed_user"])
    if target_data != None:
        try:
            await bot.send_photo(target_data["telegram_id"], caption=await get_questionnaire(user_data, 2), photo=str(user_data['photo_id']), reply_markup=await get_questionnaire_answear_keyboard(user_data), parse_mode="HTML")
        except Exception as e:
            pass

    await get_other_questionnaire(query)


@delete_old_message
async def __dislike_target_review(query: CallbackQuery):
    """
    Dislike other user questionaire as review
    """

    await get_other_questionnaire(query)


@delete_old_message
async def __like_answear(query: CallbackQuery):
    """
    Like other user questionaire as answear
    """  

    await send_get_questionnaire_answear(query)


@delete_old_message
async def __dislike_answear(query: CallbackQuery):
    """
    Dislike other user questionaire as answear
    """


def register_questionnaire_handlers(dp: Dispatcher):

    # Callback handlers
    dp.register_callback_query_handler(__like_target_review, text="like")
    dp.register_callback_query_handler(__like_answear, Text(startswith="like_"), state=any_state)
    dp.register_callback_query_handler(__dislike_target_review, text="dislike")
    dp.register_callback_query_handler(__dislike_answear, text="dislike_answear", state=any_state)
