from typing import Union
from enum import Enum, auto
from tortoise.exceptions import IntegrityError
from tortoise.validators import ValidationError


class MESSAGES(Enum):
    COMMANDS_HANDLER_ENTER_START = auto()

    ENTER_SEX = auto()
    REGISTRATION_FINISHED = auto()
    PROFILE_UPDATED_SUCCESSFULLY = auto()

    SOMEONE_LIKED_YOUR_PROFILE = auto()

    CHOOSE_SECTION = auto()
    CHOOSE_SECTION_OPTIONS = auto()


class ERRORS(Enum):
    INTEGRITY = auto()
    VALIDATION = auto()
    VALUE_MUST_BY_NUMERIC = auto()
    NO_MORE_PROFILES = auto()


class BUTTONS(Enum):
    SEND_LOCATION = auto()
    CANCEL = auto()
    FEMALE = auto()
    MALE = auto()


AVAILABLE_LANGUAGES = ['en', 'ru']

_TRANSLATIONS = {
    'en': {
        MESSAGES.COMMANDS_HANDLER_ENTER_START: "Write /start to initialize the bot",
        MESSAGES.ENTER_SEX: "1 - Male\n2-Female",
        MESSAGES.REGISTRATION_FINISHED: "Registration finished",
        MESSAGES.SOMEONE_LIKED_YOUR_PROFILE: "Some one liked your profile: {profile}\.\n"
                                             "Have a nice day \n"
                                             "\(if this doesn't work out, go hit the Gym\)\.",
        MESSAGES.CHOOSE_SECTION: "Choose what would you like to to",
        MESSAGES.CHOOSE_SECTION_OPTIONS: "1 - Search for profiles\n2 - Edit profile\n3 - Watch your profile presentation",
        MESSAGES.PROFILE_UPDATED_SUCCESSFULLY: "Your profile was updated successfully",


        ERRORS.VALIDATION: "An error occurred: {error.args[0]}",
        ERRORS.VALUE_MUST_BY_NUMERIC: "Value must be numeric",
        ERRORS.INTEGRITY: "You are already registered",
        ERRORS.NO_MORE_PROFILES: "There are no more profiles",

        BUTTONS.MALE: "Male",
        BUTTONS.FEMALE: "Female",
        BUTTONS.SEND_LOCATION: "Send location",
        BUTTONS.CANCEL: "Cancel"
    },
    'ru': {
        MESSAGES.COMMANDS_HANDLER_ENTER_START: "Напиши /start чтобы начать",
        MESSAGES.ENTER_SEX: "1 - Мужской\n2 - Женский",
        MESSAGES.REGISTRATION_FINISHED: "Регистрация завершена",
        MESSAGES.SOMEONE_LIKED_YOUR_PROFILE: "Кому\-то понравился твой профиль: {profile}\.\n"
                                             "Хорошего дня \n"
                                             "\(Если у тебя не получится, попробуй гим\)\.",
        MESSAGES.CHOOSE_SECTION: "Выбери чтобы тебе хотелось сделать",
        MESSAGES.CHOOSE_SECTION_OPTIONS: "1 - Смотреть профили\n2 - Редактировать свой профиль\n3 - Посмотреть свой профиль",
        MESSAGES.PROFILE_UPDATED_SUCCESSFULLY: "Ваш профиль был успешно отредактирован",

        ERRORS.VALIDATION: "Произошла ошибка: {error.args[0]}",
        ERRORS.VALUE_MUST_BY_NUMERIC: "Значение должно быть числом",
        ERRORS.INTEGRITY: "Вы уже зарегистрированны",
        ERRORS.NO_MORE_PROFILES: "Больше нет профилей",

        BUTTONS.MALE: "Мужской",
        BUTTONS.FEMALE: "Женский",
        BUTTONS.SEND_LOCATION: "Отправиль локацию",
        BUTTONS.CANCEL: "Отменить"
    }
}

_FIELD_ENTER_TRANSLATIONS = {
    'en': {
        "name": "Enter your name",
        "surname": "Enter your surname",
        "age": "Enter your age",
        "sex": "Enter your sex",
        "target": "Enter who are you looking for",
        "location": "Please, send your location",
        "description": "Enter your description",
        "image_id": "Now, send your photo"
    },
    'ru': {
        "name": "Введите своё имя",
        "surname": "Введите свою фамилию",
        "age": "Введите свой возраст",
        "sex": "Введите свой пол",
        "target": "Введите пол того, кого вы ищите",
        "location": "Отправьте свою локацию",
        "description": "Введите своё описание",
        "image_id": "А сейчас, отправьте своё фото"
    }
}


def translate(message: Union[MESSAGES, ERRORS, BUTTONS], lang: str = 'en') -> str:
    lang = lang if lang in AVAILABLE_LANGUAGES else 'en'
    return _TRANSLATIONS[lang][message]


def translate_enter_field(field: str, lang: str = 'en') -> str:
    return _FIELD_ENTER_TRANSLATIONS[lang][field]


def translate_exception(error: Exception, lang: str = 'en'):
    error_type = type(error)
    if error_type is IntegrityError:
        return _TRANSLATIONS[lang][ERRORS.INTEGRITY]
    elif error_type is ValidationError:
        return _TRANSLATIONS[lang][ERRORS.VALIDATION].format(error=error)
    return f"{error}"


def T(message: Union[MESSAGES, ERRORS, BUTTONS], lang: str = 'en') -> str:
    return translate(message, lang)
