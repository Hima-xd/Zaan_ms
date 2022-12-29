import requests
import urllib
import asyncio
import os
from pyrogram import filters
from KRISTY import TEMP_DOWNLOAD_DIRECTORY, pbot


@pbot.on_message(filters.command("boobz"))
async def boobs(client, message):
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    pic_loc = os.path.join(TEMP_DOWNLOAD_DIRECTORY, "bobs.jpg")
    a = await message.reply_text("**ʟᴏᴏᴋɪɴɢ ꜰᴏʀ ɴᴜᴅᴇ ɪᴍᴀɢᴇꜱ ʙᴀʙʏ🥀**")
    await asyncio.sleep(0.5)
    await a.edit("`ꜱᴜʙᴍɪᴛᴛɪɴɢ ɴᴜᴅᴇ ᴘʜᴏᴛᴏꜱ ʙᴀʙʏ🥀...`")
    nsfw = requests.get("http://api.oboobs.ru/noise/1").json()[0]["preview"]
    urllib.request.urlretrieve("http://media.oboobs.ru/{}".format(nsfw), pic_loc)
    await client.send_photo(message.chat.id, pic_loc, caption=f"**[ᴋʀɪꜱᴛʏ](https://t.me/Miss_Kristy_bot)**")
    os.remove(pic_loc)
    await a.delete()
