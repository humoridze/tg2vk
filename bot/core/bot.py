from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from bot.config.settings import settings
from bot.handlers.message_handler import MessageHandler, PublishCallback
from bot.middleware.auth_middleware import AuthMiddleware
from bot.core.logger import setup_logger

class TelegramBot:
    def __init__(self):
        self._logger = setup_logger()
        self._bot = Bot(
            token=settings.telegram_bot_token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        self._dp = Dispatcher()
        self._setup()
    
    def _setup(self):
        self._dp.message.middleware(AuthMiddleware())
        self._dp.callback_query.middleware(AuthMiddleware())
        
        message_handler = MessageHandler(self._bot)
        self._dp.message.register(message_handler.handle_media)
        self._dp.callback_query.register(
            message_handler.handle_confirmation,
            PublishCallback.filter()
        )
    
    async def start(self):
        try:
            self._logger.info("Bot started successfully")
            await self._dp.start_polling(self._bot)
        except Exception as e:
            self._logger.error(f"Bot error: {e}")
            raise
        finally:
            await self._bot.session.close()