import json
import os

from telethon import TelegramClient
from telethon.tl.types import Channel, Chat, User

from .config import Config


class TelegramAnalyzer:
    def __init__(self):
        if not Config.API_ID or not Config.API_HASH:
            raise ValueError(
                "Please set TELEGRAM_API_ID and TELEGRAM_API_HASH in .env file"
            )

        self.client = TelegramClient(
            Config.SESSION_NAME, Config.API_ID, Config.API_HASH
        )
        os.makedirs("data", exist_ok=True)

    async def connect(self):
        await self.client.start()
        if not await self.client.is_user_authorized():
            phone = input("Please enter your phone number: ")
            await self.client.send_code_request(phone)
            code = input("Please enter the code you received: ")
            await self.client.sign_in(phone, code)

    async def get_groups(self):
        """Get all groups and channels the user is a member of"""
        dialogs = await self.client.get_dialogs()
        groups = []

        for dialog in dialogs:
            entity = dialog.entity
            if isinstance(entity, (Channel, Chat)) and not isinstance(entity, User):
                groups.append(
                    {
                        "id": dialog.id,
                        "name": dialog.entity.title,
                        "members_count": getattr(entity, "participants_count", 0),
                        "type": "channel" if isinstance(entity, Channel) else "group",
                    }
                )

        # Ensure data directory exists
        os.makedirs(os.path.dirname(Config.GROUPS_FILE), exist_ok=True)

        # Save to JSON
        with open(Config.GROUPS_FILE, "w", encoding="utf-8") as f:
            json.dump(groups, f, indent=4, ensure_ascii=False)

        return groups

    async def analyze_group_media(self, group_id):
        """Analyze media in a specific group"""
        total_size = 0
        media_count = {"photos": 0, "videos": 0, "documents": 0, "audio": 0}

        async for message in self.client.iter_messages(group_id, limit=None):
            if message.media:
                if hasattr(message.media, "document"):
                    size = message.media.document.size
                    total_size += size
                    if message.video:
                        media_count["videos"] += 1
                    elif message.document:
                        media_count["documents"] += 1
                    elif message.audio:
                        media_count["audio"] += 1
                elif message.photo:
                    media_count["photos"] += 1
                    # Estimate photo size as 1MB
                    total_size += 1_000_000

        return {"total_size": total_size, "media_count": media_count}
