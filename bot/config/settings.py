import os
from dotenv import load_dotenv
from typing import List

load_dotenv()

class Settings:
    def __init__(self):
        self._telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self._telegram_channel_id = os.getenv("TELEGRAM_CHANNEL_ID")
        self._vk_user_token = os.getenv("VK_USER_TOKEN")
        self._vk_group_id = os.getenv("VK_GROUP_ID")
        self._allowed_user_ids = self._parse_allowed_users(os.getenv("ALLOWED_USER_IDS", ""))
        
        self._validate()
    
    def _parse_allowed_users(self, users_str: str) -> List[int]:
        if not users_str:
            return []
        return [int(uid.strip()) for uid in users_str.split(",") if uid.strip()]
    
    def _validate(self):
        required = [
            self._telegram_bot_token,
            self._telegram_channel_id,
            self._vk_user_token,
            self._vk_group_id
        ]
        if not all(required):
            raise ValueError("Missing required environment variables")
    
    @property
    def telegram_bot_token(self) -> str:
        return self._telegram_bot_token
    
    @property
    def telegram_channel_id(self) -> str:
        return self._telegram_channel_id
    
    @property
    def vk_user_token(self) -> str:
        return self._vk_user_token
    
    @property
    def vk_group_id(self) -> str:
        return self._vk_group_id
    
    @property
    def allowed_user_ids(self) -> List[int]:
        return self._allowed_user_ids

settings = Settings()