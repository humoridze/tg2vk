from aiogram import Bot
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters.callback_data import CallbackData
from bot.services.telegram_publisher import TelegramPublisher
from bot.services.vk_publisher import VKPublisher
from bot.utils.media_processor import MediaProcessor
from bot.core.logger import setup_logger

class PublishCallback(CallbackData, prefix="publish"):
    action: str

class MessageHandler:
    def __init__(self, bot: Bot):
        self._bot = bot
        self._logger = setup_logger()
        self._media_processor = MediaProcessor(bot)
        self._telegram_publisher = TelegramPublisher(bot)
        self._vk_publisher = VKPublisher()
        self._pending_posts = {}
    
    async def handle_media(self, message: Message):
        try:
            self._logger.info(f"Processing message from user {message.from_user.id}")
            
            media_group = await self._media_processor.process_message(message)
            
            if not media_group.has_media() and not media_group.caption:
                await message.answer("No content found in message")
                return
            
            self._pending_posts[message.from_user.id] = media_group
            
            preview = self._create_preview(media_group)
            keyboard = self._create_confirmation_keyboard()
            
            await message.answer(
                f"Preview:\n\n{preview}\n\n✅ Confirm publication?",
                reply_markup=keyboard
            )
            
        except Exception as e:
            self._logger.error(f"Error handling message: {e}", exc_info=True)
            await message.answer(f"❌ Error: {str(e)}")
    
    async def handle_confirmation(self, callback: CallbackQuery):
        try:
            callback_data = PublishCallback.unpack(callback.data)
            user_id = callback.from_user.id
            
            if callback_data.action == "confirm":
                if user_id not in self._pending_posts:
                    await callback.answer("Post not found", show_alert=True)
                    return
                
                media_group = self._pending_posts[user_id]
                
                await callback.message.edit_text("⏳ Publishing...")
                
                await self._telegram_publisher.publish(media_group)
                self._logger.info("Published to Telegram channel")
                
                await self._vk_publisher.publish(media_group)
                self._logger.info("Published to VK group")
                
                del self._pending_posts[user_id]
                
                await callback.message.edit_text("✅ Successfully published to Telegram and VK")
                
            elif callback_data.action == "cancel":
                if user_id in self._pending_posts:
                    del self._pending_posts[user_id]
                
                await callback.message.edit_text("❌ Publication cancelled")
            
            await callback.answer()
            
        except Exception as e:
            self._logger.error(f"Error handling confirmation: {e}", exc_info=True)
            await callback.message.edit_text(f"❌ Error: {str(e)}")
            await callback.answer()
    
    def _create_preview(self, media_group) -> str:
        preview_parts = []
        
        if media_group.caption:
            preview_parts.append(f"Text: {media_group.caption[:200]}{'...' if len(media_group.caption) > 200 else ''}")
        
        if media_group.has_media():
            media_counts = {}
            for item in media_group.items:
                media_counts[item.type] = media_counts.get(item.type, 0) + 1
            
            media_info = ", ".join([f"{count} {type}(s)" for type, count in media_counts.items()])
            preview_parts.append(f"Media: {media_info}")
        
        return "\n".join(preview_parts) if preview_parts else "Empty post"
    
    def _create_confirmation_keyboard(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Confirm",
                    callback_data=PublishCallback(action="confirm").pack()
                ),
                InlineKeyboardButton(
                    text="❌ Cancel",
                    callback_data=PublishCallback(action="cancel").pack()
                )
            ]
        ])