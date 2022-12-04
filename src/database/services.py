from typing import List, Optional, Tuple, Union
from models import Client, Point, LocationField

from pypika import CustomFunction
from tortoise.functions import Function
from tortoise.exceptions import DoesNotExist, ValidationError, IntegrityError
from tortoise.expressions import RawSQL


class DistanceFunction(Function):
    database_func = CustomFunction("DISTANCE", ["location", "query"])


async def get_nearest_clients_ids(client: Client, count: int = 10, offset: int = 0) -> List[Client]:
    location = client.location
    sql_point = f"{LocationField.SQL_TYPE}({location.lat}, {location.lon})"
    clients = await Client.all()\
        .exclude(id=client.id) \
        .annotate(distance=DistanceFunction("location", RawSQL(sql_point)))\
        .order_by("distance") \
        .limit(count) \
        .offset(offset * count) \
        .values_list('id') \

    return [item[0] for item in clients]


async def get_client_by_telegram_id(telegram_id: int) -> Optional[Client]:
    try:
        return await Client.get(telegram_id=telegram_id)
    except DoesNotExist:
        return None


async def get_client_by_id(_id: int) -> Optional[Client]:
    try:
        return await Client.get(id=_id)
    except DoesNotExist:
        return None


async def save_client(client: Client):
    await client.save()


async def create_client(
        telegram_id: int,
        name: str,
        surname: str,
        age: int,
        location: Point,
        sex: str,
        target: str,
        description: str,
        image_id: str
) -> Union[Tuple[Client, None], Tuple[None, Exception]]:
    try:
        client = await Client.create(
            telegram_id=telegram_id,
            name=name,
            surname=surname,
            age=age,
            location=location,
            sex=sex,
            target=target,
            description=description,
            image_id=image_id
        )
        return client, None
    except ValidationError as e:
        return None, e
    except IntegrityError as e:
        return None, e
