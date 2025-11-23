from abc import ABC, abstractmethod
from bot.utils.media_processor import MediaGroup

class BasePublisher(ABC):
    @abstractmethod
    async def publish(self, media_group: MediaGroup):
        pass