from aiogram import Bot
from aiogram.types import InputMediaPhoto, InputMediaVideo
from bot.services.base_publisher import BasePublisher
from bot.utils.media_processor import MediaGroup
from bot.config.settings import settings
from typing import List

class TelegramPublisher(BasePublisher):
    def __init__(self, bot: Bot):
        self._bot = bot
        self._channel_id = settings.telegram_channel_id
    
    async def publish(self, media_group: MediaGroup):
        if not media_group.has_media() and not media_group.caption:
            raise ValueError("Cannot publish empty message")
        
        if not media_group.has_media():
            await self._publish_text_only(media_group)
        elif len(media_group.items) == 1:
            await self._publish_single_media(media_group)
        else:
            await self._publish_media_group(media_group)
    
    async def _publish_text_only(self, media_group: MediaGroup):
        await self._bot.send_message(
            chat_id=self._channel_id,
            text=media_group.caption
        )
    
    async def _publish_single_media(self, media_group: MediaGroup):
        item = media_group.items[0]
        
        if item.type == "photo":
            await self._bot.send_photo(
                chat_id=self._channel_id,
                photo=item.file_id,
                caption=media_group.caption
            )
        elif item.type == "video":
            await self._bot.send_video(
                chat_id=self._channel_id,
                video=item.file_id,
                caption=media_group.caption
            )
    
    async def _publish_media_group(self, media_group: MediaGroup):
        media_list = self._build_media_list(media_group)
        
        await self._bot.send_media_group(
            chat_id=self._channel_id,
            media=media_list
        )
    
    def _build_media_list(self, media_group: MediaGroup) -> List:
        media_list = []
        
        for i, item in enumerate(media_group.items):
            caption = media_group.caption if i == 0 else None
            
            if item.type == "photo":
                media_list.append(
                    InputMediaPhoto(
                        media=item.file_id,
                        caption=caption
                    )
                )
            elif item.type == "video":
                media_list.append(
                    InputMediaVideo(
                        media=item.file_id,
                        caption=caption
                    )
                )
        
        return media_list