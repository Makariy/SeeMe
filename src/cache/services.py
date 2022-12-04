from typing import Optional, Type
import json
from state import State, BaseStateData
from .key_manager import get_key_for_chat_state
from .cache import Cache


cache = Cache()


async def _get_raw_state_by_telegram_id(_id: int) -> Optional[str]:
    key = await get_key_for_chat_state(_id)
    raw_state = await cache.get(key)
    return raw_state


async def get_not_validated_state_by_telegram_id(telegram_id: int, data_type: Type[BaseStateData]) -> Optional[State]:
    raw_state = await _get_raw_state_by_telegram_id(telegram_id)
    if not raw_state:
        return None
    dict_state = json.loads(raw_state)
    state = State.construct(**dict_state)
    state.data = data_type.construct(**dict_state['data'])
    return state


async def get_state_by_telegram_id(telegram_id: int) -> Optional[State]:
    raw_state = await _get_raw_state_by_telegram_id(telegram_id)
    if not raw_state:
        return None
    return State.parse_raw(raw_state)


async def set_state_by_telegram_id(telegram_id: int, state: State):
    key = await get_key_for_chat_state(telegram_id)
    return await cache.set(key, state.json())

