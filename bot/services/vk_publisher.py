import aiohttp
from bot.services.base_publisher import BasePublisher
from bot.utils.media_processor import MediaGroup
from bot.config.settings import settings
from typing import List, Dict, Any

class VKPublisher(BasePublisher):
    def __init__(self):
        self._token = settings.vk_user_token
        self._group_id = settings.vk_group_id
        self._api_version = "5.131"
        self._base_url = "https://api.vk.com/method/"
    
    async def publish(self, media_group: MediaGroup):
        if not media_group.has_media() and not media_group.caption:
            raise ValueError("Cannot publish empty message")
        
        if media_group.has_media():
            attachments = await self._prepare_attachments(media_group)
            
            await self._api_request("wall.post", {
                "owner_id": f"-{self._group_id}",
                "message": media_group.caption or "",
                "attachments": ",".join(attachments)
            })
        else:
            await self._api_request("wall.post", {
                "owner_id": f"-{self._group_id}",
                "message": media_group.caption
            })
    
    async def _prepare_attachments(self, media_group: MediaGroup) -> List[str]:
        attachments = []
        
        for item in media_group.items:
            if item.type == "photo":
                attachment = await self._upload_photo(item.file_bytes)
                attachments.append(attachment)
            elif item.type == "video":
                attachment = await self._upload_video(item.file_bytes, media_group.caption)
                attachments.append(attachment)
        
        return attachments
    
    async def _upload_photo(self, file_bytes: bytes) -> str:
        upload_server = await self._api_request("photos.getWallUploadServer", {
            "group_id": self._group_id
        })
        
        upload_url = upload_server["response"]["upload_url"]
        
        async with aiohttp.ClientSession() as session:
            form = aiohttp.FormData()
            form.add_field("photo", file_bytes, filename="photo.jpg", content_type="image/jpeg")
            
            async with session.post(upload_url, data=form) as resp:
                upload_result = await resp.json()
        
        save_result = await self._api_request("photos.saveWallPhoto", {
            "group_id": self._group_id,
            "photo": upload_result["photo"],
            "server": upload_result["server"],
            "hash": upload_result["hash"]
        })
        
        photo = save_result["response"][0]
        return f"photo{photo['owner_id']}_{photo['id']}"
    
    async def _upload_video(self, file_bytes: bytes, description: str = None) -> str:
        video_server = await self._api_request("video.save", {
            "name": "Video",
            "description": description or "",
            "group_id": self._group_id,
            "is_private": 0,
            "wallpost": 1,
            "no_comments": 0,
            "repeat": 0
        })
        
        upload_url = video_server["response"]["upload_url"]
        video_id = video_server["response"]["video_id"]
        owner_id = video_server["response"]["owner_id"]
        
        async with aiohttp.ClientSession() as session:
            form = aiohttp.FormData()
            form.add_field("video_file", file_bytes, filename="video.mp4", content_type="video/mp4")
            
            async with session.post(upload_url, data=form) as resp:
                await resp.text()
        
        return f"video{owner_id}_{video_id}"
    
    async def _api_request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        params["access_token"] = self._token
        params["v"] = self._api_version
        
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self._base_url}{method}", data=params) as resp:
                result = await resp.json()
                
                if "error" in result:
                    raise Exception(f"VK API Error: {result['error']['error_msg']}")
                
                return result