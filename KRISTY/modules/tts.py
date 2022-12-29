from typing import Optional, List
from gtts import gTTS
import os
import requests
import json

from telegram import ChatAction
from telegram.ext import run_async

from KRISTY import dispatcher
from KRISTY.modules.disable import DisableAbleCommandHandler
from KRISTY.modules.helper_funcs.alternate import typing_action, send_action

@run_async
@send_action(ChatAction.RECORD_AUDIO)
def gtts(update, context):
    msg = update.effective_message
    reply = " ".join(context.args)
    if not reply:
        if msg.reply_to_message:
            reply = msg.reply_to_message.text
        else:
            return msg.reply_text(
                "ʀᴇᴘʟʏ ᴛᴏ ꜱᴏᴍᴇ ᴍᴇꜱꜱᴀɢᴇ ᴏʀ ᴇɴᴛᴇʀ ꜱᴏᴍᴇ ᴛᴇxᴛ ᴛᴏ ᴄᴏɴᴠᴇʀᴛ ɪᴛ ɪɴᴛᴏ ᴀᴜᴅɪᴏ ꜰᴏʀᴍᴀᴛ ʙᴀʙʏ🥀!"
            )
        for x in "\n":
            reply = reply.replace(x, "")
    try:
        tts = gTTS(reply)
        tts.save("k.mp3")
        with open("k.mp3", "rb") as speech:
            msg.reply_audio(speech)
    finally:
        if os.path.isfile("k.mp3"):
            os.remove("k.mp3")


# Open API key
API_KEY = "6ae0c3a0-afdc-4532-a810-82ded0054236"
URL = "http://services.gingersoftware.com/Ginger/correct/json/GingerTheText"


@run_async
@typing_action
def spellcheck(update, context):
    if update.effective_message.reply_to_message:
        msg = update.effective_message.reply_to_message

        params = dict(lang="US", clientVersion="2.0", apiKey=API_KEY, text=msg.text)

        res = requests.get(URL, params=params)
        changes = json.loads(res.text).get("LightGingerTheTextResult")
        curr_string = ""
        prev_end = 0

        for change in changes:
            start = change.get("From")
            end = change.get("To") + 1
            suggestions = change.get("Suggestions")
            if suggestions:
                sugg_str = suggestions[0].get("Text")  # should look at this list more
                curr_string += msg.text[prev_end:start] + sugg_str
                prev_end = end

        curr_string += msg.text[prev_end:]
        update.effective_message.reply_text(curr_string)
    else:
        update.effective_message.reply_text(
            "ʀᴇᴘʟʏ ᴛᴏ ꜱᴏᴍᴇ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ɢᴇᴛ ɢʀᴀᴍᴍᴀʀ ᴄᴏʀʀᴇᴄᴛᴇᴅ ᴛᴇxᴛ ʙᴀʙʏ🥀!"
        )

dispatcher.add_handler(DisableAbleCommandHandler("tts", gtts, pass_args=True))
dispatcher.add_handler(DisableAbleCommandHandler("splcheck", spellcheck))

__help__ = """
 » `/tts` <reply to msg> :  ᴛᴜʀɴꜱ ᴛᴇxᴛ ᴛᴏ ꜱᴘᴇᴇᴄʜ
 """
__mod_name__ = "TTS"
