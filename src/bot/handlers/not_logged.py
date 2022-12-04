from typing import Optional

from telegram import Update
from telegram.ext import ContextTypes

from state import State, CreateProfileData
from database.services import create_client
from cache.services import get_not_validated_state_by_telegram_id, set_state_by_telegram_id

from .utils import (
    is_update_is_start,
    ask_to_enter_field,
    format_error,
    update_state_by_client_message,
    cast_message_for_field,
    handle_validation_errors,
    create_search_for_profiles_state_by_client
)
from ..translator import T, MESSAGES


async def _finish_registration(state: State, update: Update, context: ContextTypes.DEFAULT_TYPE) -> Optional[State]:
    telegram_id = update.message.from_user.id
    lang = update.message.from_user.language_code

    state.data.validate_model()
    client, error = await create_client(
        **state.data.dict()
    )
    if error is not None:
        await context.bot.send_message(
            text=await format_error(error, lang),
            chat_id=telegram_id
        )
        return
    await context.bot.send_message(text=T(MESSAGES.REGISTRATION_FINISHED, lang), chat_id=telegram_id)
    state = await create_search_for_profiles_state_by_client(client)
    await set_state_by_telegram_id(telegram_id, state)
    return state


@handle_validation_errors
async def handle_not_logged(_: State, update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.message.from_user.id
    # As the data is not entirely filled,
    # pydantic does not parse it as CreateProfileData,
    # so I need to explicitly construct it myself
    state = await get_not_validated_state_by_telegram_id(telegram_id, data_type=CreateProfileData)
    if not await is_update_is_start(update):
        from .utils import update_state_by_client_message
        null_field = state.data.get_unfilled_field()
        state = await update_state_by_client_message(state, update.message, null_field)

    null_field = state.data.get_unfilled_field()
    if null_field is not None:
        lang = update.message.from_user.language_code
        return await ask_to_enter_field(context.bot, null_field, lang, telegram_id)
    else:
        return await _finish_registration(state, update, context)
