from typing import Callable, Dict, Any, Awaitable, Union
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from bot.config.settings import settings
from bot.core.logger import setup_logger

class AuthMiddleware(BaseMiddleware):
    def __init__(self):
        self._logger = setup_logger()
        super().__init__()
    
    async def __call__(
        self,
        handler: Callable[[Union[Message, CallbackQuery], Dict[str, Any]], Awaitable[Any]],
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        
        if user_id not in settings.allowed_user_ids:
            self._logger.warning(f"Unauthorized access attempt from user {user_id}")
            
            if isinstance(event, Message):
                await event.answer("Access denied")
            elif isinstance(event, CallbackQuery):
                await event.answer("Access denied", show_alert=True)
            
            return
        
        self._logger.info(f"Authorized user {user_id}")
        return await handler(event, data)