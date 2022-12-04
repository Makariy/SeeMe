from models import Client


async def get_key_for_chat_state(_id: int) -> str:
    return f"{_id}_state"

