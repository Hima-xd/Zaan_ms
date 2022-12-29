from pyrogram import filters

from KRISTY import pbot, arq, BOT_NAME


@pbot.on_message(filters.command("arq"))
async def arq_stats(_, message):
    data = await arq.stats()
    if not data.ok:
        return await message.reply_text(data.result)
    data = data.result
    uptime = data.uptime
    requests = data.requests
    cpu = data.cpu
    server_mem = data.memory.server
    api_mem = data.memory.api
    disk = data.disk
    platform = data.platform
    python_version = data.python
    users = data.users
    statistics = f"""
**>-< ꜱʏꜱᴛᴇᴍ >-<**
**ᴜᴘᴛɪᴍᴇ:** `{uptime}`
**ʀᴇQᴜᴇꜱᴛꜱ ꜱɪɴᴄᴇ ᴜᴘᴛɪᴍᴇ:** `{requests}`
**ᴄᴘᴜ:** `{cpu}`
**ᴍᴇᴍᴏʀʏ:**
    **ᴛᴏᴛᴀʟ ᴜꜱᴇᴅ:** `{server_mem}`
    **ᴀᴘɪ:** `{api_mem}`
**ᴅɪꜱᴋ:** `{disk}`
**ᴘʟᴀᴛꜰᴏʀᴍ:** `{platform}`
**ᴘʏᴛʜᴏɴ:** `{python_version}`

**ᴀʀQ ꜱᴛᴀᴛɪꜱᴛɪᴄꜱ:**
**ᴜꜱᴇʀꜱ:** `{users}`

**@{BOT_NAME} ꜱᴏᴍᴇ ᴍᴏᴅᴜʟᴇꜱ ʀᴜɴɴɪɴɢ ᴏɴ ᴀʀQ**
"""
    await message.reply_text(statistics, disable_web_page_preview=True)
