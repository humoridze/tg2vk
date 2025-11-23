from aiogram import Bot
from aiogram.types import Message, PhotoSize, Video
from typing import List, Optional
from dataclasses import dataclass, field
import io

@dataclass
class MediaItem:
    type: str
    file_id: str
    file_bytes: Optional[bytes] = None
    width: Optional[int] = None
    height: Optional[int] = None
    
    def is_vertical(self) -> bool:
        if self.width and self.height:
            return self.height > self.width
        return False

@dataclass
class MediaGroup:
    items: List[MediaItem] = field(default_factory=list)
    caption: Optional[str] = None
    
    def has_media(self) -> bool:
        return len(self.items) > 0
    
    def add_item(self, item: MediaItem):
        self.items.append(item)

class MediaProcessor:
    def __init__(self, bot: Bot):
        self._bot = bot
    
    async def process_message(self, message: Message) -> MediaGroup:
        media_group = MediaGroup()
        
        if message.caption:
            media_group.caption = message.caption
        elif message.text:
            media_group.caption = message.text
        
        if message.photo:
            await self._process_photos(message.photo, media_group)
        
        if message.video:
            await self._process_video(message.video, media_group)
        
        return media_group
    
    async def process_media_group(self, messages: List[Message]) -> MediaGroup:
        media_group = MediaGroup()
        
        for message in messages:
            if message.caption and not media_group.caption:
                media_group.caption = message.caption
            
            if message.photo:
                await self._process_photos(message.photo, media_group)
            
            if message.video:
                await self._process_video(message.video, media_group)
        
        return media_group
    
    async def _process_photos(self, photos: List[PhotoSize], media_group: MediaGroup):
        largest_photo = max(photos, key=lambda p: p.width * p.height)
        file_bytes = await self._download_file(largest_photo.file_id)
        
        media_item = MediaItem(
            type="photo",
            file_id=largest_photo.file_id,
            file_bytes=file_bytes,
            width=largest_photo.width,
            height=largest_photo.height
        )
        media_group.add_item(media_item)
    
    async def _process_video(self, video: Video, media_group: MediaGroup):
        file_bytes = await self._download_file(video.file_id)
        
        media_item = MediaItem(
            type="video",
            file_id=video.file_id,
            file_bytes=file_bytes,
            width=video.width,
            height=video.height
        )
        media_group.add_item(media_item)
    
    async def _download_file(self, file_id: str) -> bytes:
        file = await self._bot.get_file(file_id)
        file_bytes = io.BytesIO()
        await self._bot.download_file(file.file_path, file_bytes)
        return file_bytes.getvalue()