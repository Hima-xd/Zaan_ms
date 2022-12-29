import random
from KRISTY.events import register
from KRISTY import telethn

APAKAH_STRING = ["Iya", 
                 "Tidak", 
                 "Mungkin", 
                 "Mungkin Tidak", 
                 "Bisa jadi", 
                 "Mungkin Tidak",
                 "Tidak Mungkin",
                 "YNTKTS",
                 "Pala bapak kau pecah",
                 "Apa iya?",
                 "Tanya aja sama mamak kau tu pler"
                 ]


@register(pattern="^/apakah ?(.*)")
async def apakah(event):
    quew = event.pattern_match.group(1)
    if not quew:
        await event.reply('ɢɪᴠᴇ ᴍᴇ ᴀ Qᴜᴇꜱᴛɪᴏɴ  ʙᴀʙʏ🥀')
        return
    await event.reply(random.choice(APAKAH_STRING))
    
    __help__ = """
 » `/apakah` <question> :  ʀᴇᴘʟɪᴇꜱ ɪɴ ɪɴᴅᴏɴᴇꜱɪᴀɴ
 """
__mod_name__ = "APAKAH"
