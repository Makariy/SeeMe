from telegram import Update
from telegram.ext import ContextTypes

from models import Client
from cache.services import get_not_validated_state_by_telegram_id, set_state_by_telegram_id
from database.services import get_client_by_telegram_id, save_client
from state import State, EditProfileData
from ..translator import T, MESSAGES


from .utils import (
    is_update_is_start,
    cast_message_for_field,
    ask_to_enter_field,
    set_state_field,
    handle_validation_errors,
    create_search_for_profiles_state_by_client
)


async def _update_client_fields(client: Client, data: EditProfileData):
    fields = data.__fields_set__
    for field in fields:
        value = getattr(data, field)
        setattr(client, field, value)
    await save_client(client)


async def _finish_editing_profile(state: State, update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.message.from_user.id
    lang = update.message.from_user.language_code
    state = State(**state.dict())  # Validate the state
    client = await get_client_by_telegram_id(telegram_id)

    await _update_client_fields(client, state.data)
    await context.bot.send_message(
        text=T(MESSAGES.PROFILE_UPDATED_SUCCESSFULLY, lang),
        chat_id=telegram_id
    )
    state = await create_search_for_profiles_state_by_client(client)
    await set_state_by_telegram_id(telegram_id, state)
    return state


@handle_validation_errors
async def handle_edit_profile(_: State, update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.message.from_user.id
    state = await get_not_validated_state_by_telegram_id(telegram_id, data_type=EditProfileData)

    if not await is_update_is_start(update):
        null_field = state.data.get_unfilled_field()
        from .utils import update_state_by_client_message
        state = await update_state_by_client_message(state, update.message, null_field)

    null_field = state.data.get_unfilled_field()
    if null_field is not None:
        bot = context.bot
        lang = update.message.from_user.language_code
        await ask_to_enter_field(bot, null_field, lang, telegram_id)
    else:
        return await _finish_editing_profile(state, update, context)


