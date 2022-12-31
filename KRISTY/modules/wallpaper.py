from random import randint

import requests as r
from KRISTY import SUPPORT_CHAT, WALL_API, dispatcher
from KRISTY.modules.disable import DisableAbleCommandHandler
from telegram import Update
from telegram.ext import CallbackContext

def wall(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    msg = update.effective_message
    args = context.args
    msg_id = update.effective_message.message_id
    bot = context.bot
    query = " ".join(args)
    if not query:
        msg.reply_text("ᴘʟᴇᴀꜱᴇ ᴇɴᴛᴇʀ ᴀ Qᴜᴇʀʏ ʙᴀʙʏ🥀!")
        return
    caption = query
    term = query.replace(" ", "%20")
    json_rep = r.get(
        f"https://wall.alphacoders.com/api2.0/get.php?auth={WALL_API}&method=search&term={term}",
    ).json()
    if not json_rep.get("success"):
        msg.reply_text(f"ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ! ʀᴇᴘᴏʀᴛ ᴛʜɪꜱ @{SUPPORT_CHAT} ʙᴀʙʏ🥀")
    else:
        wallpapers = json_rep.get("wallpapers")
        if not wallpapers:
            msg.reply_text("ɴᴏ ʀᴇꜱᴜʟᴛꜱ ꜰᴏᴜɴᴅ! ʀᴇꜰɪɴᴇ ʏᴏᴜʀ ꜱᴇᴀʀᴄʜ ʙᴀʙʏ🥀.")
            return
        index = randint(0, len(wallpapers) - 1)  # Choose random index
        wallpaper = wallpapers[index]
        wallpaper = wallpaper.get("url_image")
        wallpaper = wallpaper.replace("\\", "")
        bot.send_photo(
            chat_id,
            photo=wallpaper,
            caption="Preview",
            reply_to_message_id=msg_id,
            timeout=60,
        )
        bot.send_document(
            chat_id,
            document=wallpaper,
            filename="wallpaper",
            caption=caption,
            reply_to_message_id=msg_id,
            timeout=60,
        )


WALLPAPER_HANDLER = DisableAbleCommandHandler("wall", wall, run_async=True)
dispatcher.add_handler(WALLPAPER_HANDLER)


__mod_name__ = "WALLPAPER"
