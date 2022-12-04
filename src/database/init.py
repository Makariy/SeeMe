import tortoise
import config


async def init_database():
    """Connect tortoise to the database. The function is being called before the server is started"""
    await tortoise.Tortoise.init(
        db_url=f'postgres://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}?minsize=2&maxsize=10',
        modules={
            'models': ["models"],
        }
    )
    await tortoise.Tortoise.generate_schemas()
