import asyncio

from database.init import init_database
from bot.bot import TelegramBot
# from generate_random_clients import generate_random_clients


async def main():
    await init_database()
    bot = TelegramBot()
    await bot.start()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
    loop.run_forever()
