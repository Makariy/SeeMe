from telegram import Update
from telegram.ext import ContextTypes

from state import CreateProfileData, State, SECTION
from database.services import get_client_by_telegram_id
from cache.services import set_state_by_telegram_id, get_state_by_telegram_id

from .handlers.utils import create_search_for_profiles_state_by_client

from .handlers.choose_section import handle_choose_section
from .handlers.search_for_profiles import handle_search_for_profiles
from .handlers.not_logged import handle_not_logged
from .handlers.edit_profile import handle_edit_profile

from bot.translator import T, MESSAGES


async def _handle_message_by_state_if_state_returned(func, state: State, update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = await func(state, update, context)
    if state is not None:
        update.message.text = None
        return await handle_message_by_state(state, update, context)


async def handle_message_by_state(state: State, update: Update, context: ContextTypes.DEFAULT_TYPE):
    if state.section == SECTION.CHOOSE_SECTION:
        await _handle_message_by_state_if_state_returned(handle_choose_section, state, update, context)
    elif state.section == SECTION.NOT_LOGGED:
        await _handle_message_by_state_if_state_returned(handle_not_logged, state, update, context)
    elif state.section == SECTION.SEARCH_FOR_PROFILES:
        await _handle_message_by_state_if_state_returned(handle_search_for_profiles, state, update, context)
    elif state.section == SECTION.EDIT_PROFILE:
        await _handle_message_by_state_if_state_returned(handle_edit_profile, state, update, context)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    telegram_id = user.id

    state = await get_state_by_telegram_id(telegram_id)
    if state is None:
        await context.bot.send_message(
            text=T(MESSAGES.COMMANDS_HANDLER_ENTER_START, user.language_code),
            chat_id=telegram_id
        )
        return

    await handle_message_by_state(state, update, context)


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.message.from_user.id
    client = await get_client_by_telegram_id(telegram_id)
    if client is None:
        state = State(data=CreateProfileData.construct(telegram_id=telegram_id))
    else:
        state = await create_search_for_profiles_state_by_client(client)

    await set_state_by_telegram_id(telegram_id, state)
    await handle_message_by_state(state, update, context)
