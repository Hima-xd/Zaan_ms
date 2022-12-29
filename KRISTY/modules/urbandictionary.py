import requests
from telegram import ParseMode, Update
from telegram.ext import CallbackContext, run_async

from KRISTY import dispatcher
from KRISTY.modules.disable import DisableAbleCommandHandler


@run_async
def ud(update: Update, context: CallbackContext):
    message = update.effective_message
    text = message.text[len("/ud ") :]
    results = requests.get(
        f"https://api.urbandictionary.com/v0/define?term={text}"
    ).json()
    try:
        reply_text = f'*{text}*\n\n{results["list"][0]["definition"]}\n\n_{results["list"][0]["example"]}_'
    except:
        reply_text = "ɴᴏ ʀᴇꜱᴜʟᴛꜱ ꜰᴏᴜɴᴅ ʙᴀʙʏ🥀."
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN)


UD_HANDLER = DisableAbleCommandHandler(["ud"], ud)

dispatcher.add_handler(UD_HANDLER)

__help__ = """
» `/ud` (text) *:* ꜱᴇᴀʀᴄʜꜱ ᴛʜᴇ ɢɪᴠᴇɴ ᴛᴇxᴛ ᴏɴ ᴜʀʙᴀɴ ᴅɪᴄᴛɪᴏɴᴀʀʏ ᴀɴᴅ ꜱᴇɴᴅꜱ ʏᴏᴜ ᴛʜᴇ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ.
"""
__mod_name__ = "URBAN-DICTIONARY"
__command_list__ = ["ud"]
__handlers__ = [UD_HANDLER]
