from telegram import Update
from telegram.ext import ContextTypes

from state import State
from database.services import get_client_by_telegram_id
from .utils import get_profile_presentation, create_choose_section_state, set_state_by_telegram_id


async def handle_profile_presentation(_: State, update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.message.chat_id
    profile = await get_client_by_telegram_id(telegram_id)
    await context.bot.send_photo(
        chat_id=telegram_id,
        **await get_profile_presentation(profile)
    )
    state = await create_choose_section_state()
    await set_state_by_telegram_id(telegram_id, state)
    return state

