from typing import Optional
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes

from state import State, SECTION
from database.services import get_client_by_telegram_id
from cache.services import set_state_by_telegram_id

from .utils import (
    create_search_for_profiles_state_by_client,
    create_edit_profiles_state_by_client,
    create_profile_presentation_state
)
from ..translator import T, MESSAGES


SECTION_TO_TEXT_MAPPING = {
    SECTION.SEARCH_FOR_PROFILES: "1",
    SECTION.EDIT_PROFILE: "2",
    SECTION.PROFILE_PRESENTATION: "3"
}


async def get_choose_section_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(SECTION_TO_TEXT_MAPPING[SECTION.SEARCH_FOR_PROFILES]), KeyboardButton(SECTION_TO_TEXT_MAPPING[SECTION.EDIT_PROFILE])],
        [KeyboardButton(SECTION_TO_TEXT_MAPPING[SECTION.PROFILE_PRESENTATION])],
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, one_time_keyboard=True, resize_keyboard=True)


async def get_chosen_section_by_update(update: Update) -> Optional[SECTION]:
    text = update.message.text

    for section, name in SECTION_TO_TEXT_MAPPING.items():
        if name == text:
            return section


async def save_chosen_section(section: SECTION, update: Update, _: ContextTypes.DEFAULT_TYPE) -> State:
    telegram_id = update.message.from_user.id
    client = await get_client_by_telegram_id(telegram_id)

    state = None
    if section is SECTION.SEARCH_FOR_PROFILES:
        state = await create_search_for_profiles_state_by_client(client)
    elif section is SECTION.EDIT_PROFILE:
        state = await create_edit_profiles_state_by_client(client)
    elif section is SECTION.PROFILE_PRESENTATION:
        state = await create_profile_presentation_state()

    if state is None:
        raise ValueError("There was an unimplemented state")
    await set_state_by_telegram_id(telegram_id, state)
    return state


async def handle_choose_section(_: State, update: Update, context: ContextTypes.DEFAULT_TYPE):
    section = await get_chosen_section_by_update(update)
    if section is not None:
        state = await save_chosen_section(section, update, context)
        return state

    chat_id = update.message.from_user.id
    lang = update.message.from_user.language_code
    keyboard = await get_choose_section_keyboard()
    await context.bot.send_message(
        text=T(MESSAGES.CHOOSE_SECTION, lang),
        reply_markup=keyboard,
        chat_id=chat_id
    )
    await context.bot.send_message(
        text=T(MESSAGES.CHOOSE_SECTION_OPTIONS, lang),
        chat_id=chat_id
    )
