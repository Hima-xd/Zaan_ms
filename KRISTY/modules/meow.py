from pyrogram import filters

from KRISTY import pbot
from KRISTY.utils.errors import capture_err
from KRISTY.utils.http import get, resp_get

__MODULE__ = "CAT"
__HELP__ = """
 » /meow - ᴛᴏ ɢᴇᴛ ʀᴀɴᴅᴏᴍ ᴘʜᴏᴛᴏ ᴏꜰ ᴄᴀᴛ.
"""


@pbot.on_message(filters.command("meow"))
@capture_err
async def randomcat(_, message):
    cat = await get("https://aws.random.cat/meow")
    await message.reply_photo(cat.get("file"))
