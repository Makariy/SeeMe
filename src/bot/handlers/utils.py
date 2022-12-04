from typing import Any, Optional

from telegram import KeyboardButton, ReplyKeyboardMarkup, Bot, Update, Message
from telegram.ext import ContextTypes

from tortoise.validators import ValidationError

from models import Point, Client, SEXES
from state import State, SearchForProfilesData, EditProfileData, ProfileData

from cache.services import set_state_by_telegram_id
from database.services import get_nearest_clients_ids

from .exceptions import NoMoreProfilesException
from ..translator import T, translate_exception, translate_enter_field, MESSAGES, ERRORS, BUTTONS


def handle_validation_errors(func):
    async def _wrapper(state: State, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            return await func(state, update, context)
        except ValidationError as e:
            await context.bot.send_message(
                text=e.args[0],
                chat_id=update.message.chat_id
            )

    return _wrapper


def handle_exceptions(func):
    async def _wrapper(state: State, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            return await func(state, update, context)
        except NoMoreProfilesException as e:
            await context.bot.send_message(
                text=T(ERRORS.NO_MORE_PROFILES, update.message.from_user.language_code),
                chat_id=update.message.chat_id
            )

    return _wrapper


async def is_update_is_start(update: Update) -> bool:
    text = update.message.text
    message = update.message
    if text and "/start" in text:
        return True

    if not text and not message.location and not message.photo:
        return True

    return False


async def _ask_to_enter_location(bot: Bot, lang: str, chat_id: int):
    keyboard = [[KeyboardButton(T(BUTTONS.SEND_LOCATION, lang), request_location=True, )],
                [KeyboardButton(T(BUTTONS.CANCEL, lang))]]
    await bot.send_message(
        text=translate_enter_field("location", lang),
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True),
        chat_id=chat_id
    )


async def _ask_to_enter_sex(bot: Bot, field: str, lang: str, chat_id: int):
    keyboard = [[KeyboardButton("1")], [KeyboardButton("2")]]
    await bot.send_message(
        text=translate_enter_field(field, lang),
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True),
        chat_id=chat_id
    )
    await bot.send_message(
        text=T(MESSAGES.ENTER_SEX, lang),
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True),
        chat_id=chat_id
    )


async def _ask_to_enter_text(bot: Bot, field: str, lang: str, chat_id: int):
    await bot.send_message(
        text=translate_enter_field(field, lang),
        chat_id=chat_id
    )


async def _ask_to_enter_image(bot: Bot, lang: str, chat_id: int):
    await bot.send_message(
        text=translate_enter_field("photo", lang),
        chat_id=chat_id
    )


async def ask_to_enter_field(bot: Bot, field: str, lang: str, chat_id: int):
    if field == 'location':
        return await _ask_to_enter_location(bot, lang, chat_id)
    elif field in ['sex', 'target']:
        return await _ask_to_enter_sex(bot, field, lang, chat_id)
    elif field in ['photo']:
        return await _ask_to_enter_image(bot, lang, chat_id)
    else:
        return await _ask_to_enter_text(bot, field, lang, chat_id)


async def format_error(error: Exception, lang: str) -> str:
    return translate_exception(error, lang)


async def _cast_age(message: Message) -> int:
    try:
        return int(message.text)
    except ValueError:
        raise ValidationError(T(ERRORS.VALUE_MUST_BY_NUMERIC, message.from_user.language_code))


async def _cast_location(message: Message) -> Optional[Point]:
    location = message.location
    if location is not None:
        return Point(lat=location.latitude, lon=location.longitude)


async def _cast_sex(message: Message) -> SEXES:
    try:
        value = int(message.text) - 1
        return SEXES[value]
    except ValueError:
        raise ValidationError(T(ERRORS.VALIDATION, message.from_user.language_code))
    except IndexError:
        ...


async def cast_message_for_field(message: Message, field: str):
    if field == 'location':
        return await _cast_location(message)
    elif field == 'age':
        return await _cast_age(message)
    elif field in ['sex', 'target']:
        return await _cast_sex(message)

    return message.text


async def set_state_field(state: State, telegram_id: int, field: str, value: Any) -> State:
    setattr(state.data, field, value)
    state.data.validate_initialized_fields()

    await set_state_by_telegram_id(telegram_id, state)
    return state


async def update_state_by_client_message(state: State, message: Message, field: str):
    if field == 'image_id':
        image_file = await message.photo[-1].get_file()
        file_id = image_file.file_id
        return await set_state_field(state, message.chat_id, field, file_id)
    else:
        value = await cast_message_for_field(message, field)
        return await set_state_field(state, message.chat_id, field, value)


async def create_search_for_profiles_state_by_client(client: Client) -> State:
    nearest_clients = await get_nearest_clients_ids(client)
    return State(data=SearchForProfilesData(
        search_list_ids=nearest_clients,
        current_profile=nearest_clients[0] if nearest_clients else -1
    ))


async def create_edit_profiles_state_by_client(client: Client) -> State:
    return State(data=EditProfileData.construct(
        previous_profile_data=ProfileData(
            name=client.name,
            surname=client.surname,
            age=client.age,
            sex=client.sex,
            target=client.target,
            location=client.location,
            description=client.description,
            image_filename=client.image_url
        )
    ))
