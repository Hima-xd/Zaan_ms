import os

from gtts import gTTS
from gtts import gTTSError
from telethon import *
from telethon.tl import functions
from telethon.tl import types
from telethon.tl.types import *

from KRISTY import *

from KRISTY import telethn as tbot
from KRISTY.events import register


@register(pattern="^/tts (.*)")
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        text = previous_message.message
        lan = input_str
    elif "|" in input_str:
        lan, text = input_str.split("|")
    else:
        await event.reply(
            "ɪɴᴠᴀʟɪᴅ ꜱʏɴᴛᴀx\nꜰᴏʀᴍᴀᴛ `/tts lang | text`\nFor eg: `/tts en | hello` ʙᴀʙʏ🥀"
        )
        return
    text = text.strip()
    lan = lan.strip()
    try:
        tts = gTTS(text, tld="com", lang=lan)
        tts.save("k.mp3")
    except AssertionError:
        await event.reply(
            "ᴛʜᴇ ᴛᴇxᴛ ɪꜱ ᴇᴍᴘᴛʏ ʙᴀʙʏ🥀.\n"
            "ɴᴏᴛʜɪɴɢ ʟᴇꜰᴛ ᴛᴏ ꜱᴘᴇᴀᴋ ᴀꜰᴛᴇʀ ᴘʀᴇ-ᴘʀᴇᴄᴇꜱꜱɪɴɢ ʙᴀʙʏ🥀,\n "
            "ᴛᴏᴋᴇɴɪᴢɪɴɢ ᴀɴᴅ ᴄʟᴇᴀɴɪɴɢ ʙᴀʙʏ🥀."
        )
        return
    except ValueError:
        await event.reply("ʟᴀɴɢᴜᴀɢᴇ ɪꜱ ɴᴏᴛ ꜱᴜᴘᴘᴏʀᴛᴇᴅ ʙᴀʙʏ🥀.")
        return
    except RuntimeError:
        await event.reply("ᴇʀʀᴏʀ ʟᴏᴀᴅɪɴɢ ᴛʜᴇ ʟᴀɴɢᴜᴀɢᴇꜱ ᴅɪᴄᴛɪᴏɴᴀʀʏ ʙᴀʙʏ🥀.")
        return
    except gTTSError:
        await event.reply("ᴇʀʀᴏʀ ɪɴ ɢᴏᴏɢʟᴇ ᴛᴇxᴛ-ᴛᴏ-ꜱᴘᴇᴇᴄʜ ᴀᴘɪ ʀᴇQᴜᴇꜱᴛ ʙᴀʙʏ🥀!")
        return
    with open("k.mp3", "r"):
        await tbot.send_file(
            event.chat_id, "k.mp3", voice_note=True, reply_to=reply_to_id
        )
        os.remove("k.mp3")
