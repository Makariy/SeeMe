import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler
from telegram.ext.filters import BaseFilter
import config
from .commands_handler import handle_start, handle_message


class TelegramBot:
    def __init__(self):
        self.application = ApplicationBuilder().token(config.TELEGRAM_BOT_TOKEN).build()
        self.application.add_handler(CommandHandler("start", handle_start))
        self.application.add_handler(MessageHandler(BaseFilter(), handle_message))

    async def run_updater(self,
                          poll_interval: float = 0.0,
                          timeout: int = 10,
                          bootstrap_retries: int = -1,
                          read_timeout: float = 2,
                          write_timeout=None,
                          connect_timeout=None,
                          pool_timeout=None,
                          allowed_updates=None,
                          drop_pending_updates: bool = None,
                          ):
        """
            У python-telegram-bot модуль ext не предостовляет возможности запустить бота в моём event_loop,
            так что приходится самому писать такой запуск
        """
        def error_callback(exc: Exception) -> None:
            self.application.create_task(self.application.process_error(error=exc, update=None))

        await self.application.updater.start_polling(
            poll_interval=poll_interval,
            timeout=timeout,
            bootstrap_retries=bootstrap_retries,
            read_timeout=read_timeout,
            write_timeout=write_timeout,
            connect_timeout=connect_timeout,
            pool_timeout=pool_timeout,
            allowed_updates=allowed_updates,
            drop_pending_updates=drop_pending_updates,
            error_callback=error_callback
        )

    async def start(self):
        await self.application.initialize()
        await self.run_updater()
        await self.application.start()




