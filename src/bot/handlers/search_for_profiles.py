from enum import Enum
from telegram import Update, Bot
from telegram.ext import ContextTypes
from telegram import KeyboardButton, ReplyKeyboardMarkup

from models import Client
from state import State, SearchForProfilesData
from cache.services import set_state_by_telegram_id
from database.services import get_client_by_id, get_client_by_telegram_id, get_nearest_clients_ids

from .utils import handle_exceptions, get_profile_presentation, create_choose_section_state

from ..translator import T, MESSAGES


class MessageResponse(Enum):
    LIKE = "👍"
    DISLIKE = "️🌈"
    SLEEP = "️💤"


async def get_keyboard_for_profile_search() -> ReplyKeyboardMarkup:
    keyboard = [[KeyboardButton(MessageResponse.DISLIKE.value), KeyboardButton(MessageResponse.LIKE.value)],
                [KeyboardButton(MessageResponse.SLEEP.value)]]
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)


async def send_profile_presentation(profile: Client, bot: Bot, chat_id: int):
    keyboard = await get_keyboard_for_profile_search()
    await bot.send_photo(
        reply_markup=keyboard,
        chat_id=chat_id,
        **await get_profile_presentation(profile)
    )


async def update_search_list_if_needed(state: State, telegram_id: int):
    data = state.data
    if not data.search_list_ids:
        client = await get_client_by_telegram_id(telegram_id)
        data.offset += 1
        data.search_list_ids = await get_nearest_clients_ids(client, offset=data.offset)
    await set_state_by_telegram_id(telegram_id, state)


async def send_next_profile(state: State, update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.message.from_user.id

    data: SearchForProfilesData = state.data
    profile_id = data.pop_next_profile()
    profile = await get_client_by_id(profile_id)

    await send_profile_presentation(profile, context.bot, telegram_id)
    await update_search_list_if_needed(state, telegram_id=telegram_id)


async def like_client(client_to: Client, client_from: Client, bot: Bot, lang: str):
    await bot.send_photo(
        chat_id=705021151,  # client_to.chat_id
        photo=client_from.image_id,
        caption=T(MESSAGES.SOMEONE_LIKED_YOUR_PROFILE, lang=lang) \
            .format(profile=f"[{client_from.name}](tg://user?id={client_from.telegram_id})"),
        parse_mode='MarkdownV2'
    )


@handle_exceptions
async def handle_search_for_profiles(state: State, update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    telegram_id = update.message.from_user.id

    if message == MessageResponse.LIKE.value:
        client_from = await get_client_by_telegram_id(telegram_id)
        client_to = await get_client_by_id(state.data.current_profile)
        await like_client(client_to, client_from, context.bot, update.message.from_user.language_code)
    elif message == MessageResponse.DISLIKE.value:
        ...
    elif message == MessageResponse.SLEEP.value:
        state = await create_choose_section_state()
        await set_state_by_telegram_id(telegram_id, state)
        return state

    await send_next_profile(state, update, context)
