from telethon import *
from telethon.tl.functions.account import *
from telethon.tl.functions.channels import *
from telethon.tl.functions.photos import *
from telethon.tl.types import *
from KRISTY.events import register
from KRISTY import telethn as borg
from html import *
import logging

logger = logging.getLogger(__name__)



if 1 == 1:
    name = "Profile Photos"
    client = borg

    @register(pattern=("/pfp"))
    async def PPScmd(event):
#        """Gets the profile photos of replied users, channels or chats"""
        try:
            id = "".join(event.raw_text.split(maxsplit=2)[1:]) 
            user = await event.get_reply_message()
            if user:
                photos = await event.client.get_profile_photos(user.sender)
            else:
                photos = await event.client.get_profile_photos(event.chat_id)
            if id.strip() == "":
                try:
                    await event.client.send_file(event.chat.id, photos)
                except a:
                    photo = await event.client.download_profile_photo(event.chat_id)
                    await borg.send_file(event.chat.id, photo)
            else:
                try:
                    id = int(id)
                    if id <= 0:
                        await event.edit("<code>ɪᴅ ɴᴜᴍʙᴇʀ ʏᴏᴜ ᴇɴᴛᴇʀᴇᴅ ɪꜱ ɪɴᴠᴀʟɪᴅ ʙᴀʙʏ🥀</code>")
                        return
                except:
                    await event.edit("<code>ɪᴅ ɴᴜᴍʙᴇʀ ʏᴏᴜ ᴇɴᴛᴇʀᴇᴅ ɪꜱ ɪɴᴠᴀʟɪᴅ ʙᴀʙʏ🥀</code>")
                    return
                if int(id) <= (len(photos)):
                    send_photos = await event.client.download_media(photos[id - 1])
                    await borg.send_file(event.chat.id, send_photos)
                else:
                    await event.edit("<code>ɴᴏ ᴘʜᴏᴛᴏ ꜰᴏᴜɴᴅ ᴡɪᴛʜ ᴛʜᴀᴛ ɪᴅ ʙᴀʙʏ🥀</code>")
                    return
        except:
            await borg.send_message("ʀᴇᴘʟʏ ᴛᴏ ᴜꜱᴇʀ ᴍᴀᴛᴇ ʙᴀʙʏ🥀")
