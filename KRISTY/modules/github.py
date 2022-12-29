import aiohttp
from pyrogram import filters
from KRISTY import pbot
from KRISTY.services.emror import capture_err


__mod_name__ = "GITHUB"

__help__ = """

ɪ ᴡɪʟʟ ɢɪᴠᴇ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ɢɪᴛʜᴜʙ ᴘʀᴏꜰɪʟᴇ

 » `/github` <username>*:* ɢᴇᴛ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴀ ɢɪᴛʜᴜʙ ᴜꜱᴇʀ.
"""

@pbot.on_message(filters.command('github'))
@capture_err
async def github(_, message):
    if len(message.command) != 2:
        await message.reply_text("/github Username")
        return
    username = message.text.split(None, 1)[1]
    URL = f'https://api.github.com/users/{username}'
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as request:
            if request.status == 404:
                return await message.reply_text("ERROR BABY🥀")

            result = await request.json()
            try:
                url = result['html_url']
                name = result['name']
                company = result['company']
                bio = result['bio']
                created_at = result['created_at']
                avatar_url = result['avatar_url']
                blog = result['blog']
                location = result['location']
                repositories = result['public_repos']
                followers = result['followers']
                following = result['following']
                caption = f"""**Info Of {name}**
**ᴜꜱᴇʀɴᴀᴍᴇ:** `{username}`
**ʙɪᴏ:** `{bio}`
**ᴘʀᴏꜰɪʟᴇ ʟɪɴᴋ:** [ʜᴇʀᴇ]({url})
**ᴄᴏᴍᴘᴀɴʏ:** `{company}`
**ᴄʀᴇᴀᴛᴇᴅ ᴏɴ:** `{created_at}`
**ʀᴇᴘᴏꜱɪᴛᴏʀɪᴇꜱ:** `{repositories}`
**ʙʟᴏɢ:** `{blog}`
**ʟᴏᴄᴀᴛɪᴏɴ:** `{location}`
**ꜰᴏʟʟᴏᴡᴇʀꜱ:** `{followers}`
**ꜰᴏʟʟᴏᴡɪɴɢ:** `{following}`"""
            except Exception as e:
                print(str(e))
                pass
    await message.reply_photo(photo=avatar_url, caption=caption)
