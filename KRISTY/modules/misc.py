import time
import os
import re
import codecs
from typing import List
from random import randint
from KRISTY.modules.helper_funcs.chat_status import user_admin
from KRISTY.modules.disable import DisableAbleCommandHandler
from KRISTY import (
    dispatcher,
    WALL_API,
)
import requests as r
import wikipedia
from requests import get, post
from telegram import (
    Chat,
    ChatAction,
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ParseMode,
    Message,
    MessageEntity,
    TelegramError,
)
from telegram.error import BadRequest
from telegram.ext.dispatcher import run_async
from telegram.ext import CallbackContext, Filters, CommandHandler
from KRISTY import StartTime
from KRISTY.modules.helper_funcs.chat_status import sudo_plus
from KRISTY.modules.helper_funcs.alternate import send_action, typing_action

MARKDOWN_HELP = f"""
Markdown is a very powerful formatting tool supported by telegram. {dispatcher.bot.first_name} has some enhancements, to make sure that \
saved messages are correctly parsed, and to allow you to create buttons.

» <code>_italic_</code>: wrapping text with '_' will produce italic text
» <code>*bold*</code>: wrapping text with '*' will produce bold text
» <code>`code`</code>: wrapping text with '`' will produce monospaced text, also known as 'code'
» <code>[sometext](someURL)</code>: this will create a link - the message will just show <code>sometext</code>, \
and tapping on it will open the page at <code>someURL</code>.
<b>Example:</b><code>[test](example.com)</code>

» <code>[buttontext](buttonurl:someURL)</code>: this is a special enhancement to allow users to have telegram \
buttons in their markdown. <code>buttontext</code> will be what is displayed on the button, and <code>someurl</code> \
will be the url which is opened.
<b>Example:</b> <code>[This is a button](buttonurl:example.com)</code>

If you want multiple buttons on the same line, use :same, as such:
<code>[one](buttonurl://example.com)
[two](buttonurl://google.com:same)</code>
This will create two buttons on a single line, instead of one button per line.

Keep in mind that your message <b>MUST</b> contain some text other than just a button!
"""


@user_admin
def echo(update: Update, context: CallbackContext):
    args = update.effective_message.text.split(None, 1)
    message = update.effective_message

    if message.reply_to_message:
        message.reply_to_message.reply_text(
            args[1], parse_mode="MARKDOWN", disable_web_page_preview=True
        )
    else:
        message.reply_text(
            args[1], quote=False, parse_mode="MARKDOWN", disable_web_page_preview=True
        )
    message.delete()


def markdown_help_sender(update: Update):
    update.effective_message.reply_text(MARKDOWN_HELP, parse_mode=ParseMode.HTML)
    update.effective_message.reply_text(
        "ᴛʀʏ ꜰᴏʀᴡᴀʀᴅɪɴɢ ᴛʜᴇ ꜰᴏʟʟᴏᴡɪɴɢ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ᴍᴇ, ᴀɴᴅ ʏᴏᴜ'ʟʟ ꜱᴇᴇ, ᴀɴᴅ ᴜꜱᴇ #ᴛᴇꜱᴛ ʙᴀʙʏ🥀!"
    )
    update.effective_message.reply_text(
        "/save test This is a markdown test. _italics_, *bold*, code, "
        "[URL](example.com) [button](buttonurl:github.com) "
        "[button2](buttonurl://google.com:same)"
    )


def markdown_help(update: Update, context: CallbackContext):
    if update.effective_chat.type != "private":
        update.effective_message.reply_text(
            "ᴄᴏɴᴛᴀᴄᴛ ᴍᴇ ɪɴ ᴘᴍ",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Markdown help",
                            url=f"t.me/{context.bot.username}?start=markdownhelp",
                        )
                    ]
                ]
            ),
        )
        return
    markdown_help_sender(update)


def wiki(update: Update, context: CallbackContext):
    kueri = re.split(pattern="wiki", string=update.effective_message.text)
    wikipedia.set_lang("en")
    if len(str(kueri[1])) == 0:
        update.effective_message.reply_text("ᴇɴᴛᴇʀ ᴋᴇʏᴡᴏʀᴅꜱ ʙᴀʙʏ🥀!")
    else:
        try:
            pertama = update.effective_message.reply_text("ʟᴏᴀᴅɪɴɢ ʙᴀʙʏ🥀...")
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="ᴍᴏʀᴇ ɪɴꜰᴏ...",
                            url=wikipedia.page(kueri).url,
                        )
                    ]
                ]
            )
            context.bot.editMessageText(
                chat_id=update.effective_chat.id,
                message_id=pertama.message_id,
                text=wikipedia.summary(kueri, sentences=10),
                reply_markup=keyboard,
            )
        except wikipedia.PageError as e:
            update.effective_message.reply_text(f"⚠ ᴇʀʀᴏʀ: {e} ʙᴀʙʏ🥀")
        except BadRequest as et:
            update.effective_message.reply_text(f"⚠ ᴇʀʀᴏʀ: {et} ʙᴀʙʏ🥀")
        except wikipedia.exceptions.DisambiguationError as eet:
            update.effective_message.reply_text(
                f"⚠ ᴇʀʀᴏʀ ʙᴀʙʏ🥀\n ᴛʜᴇʀᴇ ᴀʀᴇ ᴛᴏᴏ ᴍᴀɴʏ Qᴜᴇʀʏ! ᴇxᴘʀᴇꜱꜱ ɪᴛ ᴍᴏʀᴇ!\nᴘᴏꜱꜱɪʙʟᴇ Qᴜᴇʀʏ ʀᴇꜱᴜʟᴛ:\n{eet}"
            )


@send_action(ChatAction.UPLOAD_PHOTO)
def wall(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    msg = update.effective_message
    msg_id = update.effective_message.message_id
    args = context.args
    query = " ".join(args)
    if not query:
        msg.reply_text("ᴘʟᴇᴀꜱᴇ ᴇɴᴛᴇʀ ᴀ Qᴜᴇʀʏ ʙᴀʙʏ🥀!")
        return
    caption = query
    term = query.replace(" ", "%20")
    json_rep = r.get(
        f"https://wall.alphacoders.com/api2.0/get.php?auth={WALL_API}&method=search&term={term}"
    ).json()
    if not json_rep.get("success"):
        msg.reply_text("ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ʙᴀʙʏ🥀!")

    else:
        wallpapers = json_rep.get("wallpapers")
        if not wallpapers:
            msg.reply_text("ɴᴏ ʀᴇꜱᴜʟᴛꜱ ꜰᴏᴜɴᴅ! ʀᴇꜰɪɴᴇ ʏᴏᴜʀ ꜱᴇᴀʀᴄʜ ʙᴀʙʏ🥀.")
            return
        index = randint(0, len(wallpapers) - 1)  # Choose random index
        wallpaper = wallpapers[index]
        wallpaper = wallpaper.get("url_image")
        wallpaper = wallpaper.replace("\\", "")
        context.bot.send_photo(
            chat_id,
            photo=wallpaper,
            caption="Preview",
            reply_to_message_id=msg_id,
            timeout=60,
        )
        context.bot.send_document(
            chat_id,
            document=wallpaper,
            filename="wallpaper",
            caption=caption,
            reply_to_message_id=msg_id,
            timeout=60,
        )


__help__ = """
» `/markdownhelp`*:* Qᴜɪᴄᴋ ꜱᴜᴍᴍᴀʀʏ ᴏꜰ ʜᴏᴡ ᴍᴀʀᴋᴅᴏᴡɴ ᴡᴏʀᴋꜱ ɪɴ ᴛᴇʟᴇɢʀᴀᴍ - ᴄᴀɴ ᴏɴʟʏ ʙᴇ ᴄᴀʟʟᴇᴅ ɪɴ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛꜱ
» `/react`*:* ʀᴇᴀᴄᴛꜱ ᴡɪᴛʜ ᴀ ʀᴀɴᴅᴏᴍ ʀᴇᴀᴄᴛɪᴏɴ
 » `/reverse`*:* ᴅᴏᴇꜱ ᴀ ʀᴇᴠᴇʀꜱᴇ ɪᴍᴀɢᴇ ꜱᴇᴀʀᴄʜ ᴏꜰ ᴛʜᴇ ᴍᴇᴅɪᴀ ᴡʜɪᴄʜ ɪᴛ ᴡᴀꜱ ʀᴇᴘʟɪᴇᴅ ᴛᴏ.
 » `/wiki` <Qᴜᴇʀʏ>*:* ᴡɪᴋɪᴘᴇᴅɪᴀ ʏᴏᴜʀ Qᴜᴇʀʏ
 » `/wall` <Qᴜᴇʀʏ>*:* ɢᴇᴛ ᴀ ᴡᴀʟʟᴘᴀᴘᴇʀ ꜰʀᴏᴍ ᴡᴀʟʟ.ᴀʟᴘʜᴀᴄᴏᴅᴇʀꜱ.ᴄᴏᴍ
 » `/cash`*:* ᴄᴜʀʀᴇɴᴄʏ ᴄᴏɴᴠᴇʀᴛᴇʀ 
 ᴇxᴀᴍᴘʟᴇ: `/cash 1 ᴜꜱᴅ ɪɴʀ`   
      _ᴏʀ_ 
      `/cash 1 ᴜꜱᴅ ɪɴʀ` ᴏᴜᴛᴘᴜᴛ: `1.0 ᴜꜱᴅ = 75.505 ɪɴʀ` 
      
         *ᴍᴜꜱɪᴄ ᴍᴏᴅᴜʟᴇꜱ:*
         » `/video` ᴏʀ `/vsong` (Qᴜᴇʀʏ): ᴅᴏᴡɴʟᴏᴀᴅ ᴠɪᴅᴇᴏ ꜰʀᴏᴍ ʏᴏᴜᴛᴜʙᴇ
         » `/music` ᴏʀ `/song` (Qᴜᴇʀʏ): ᴅᴏᴡɴʟᴏᴀᴅ ꜱᴏɴɢ ꜰʀᴏᴍ ʏᴛ ꜱᴇʀᴠᴇʀꜱ. (ᴀᴘɪ ʙᴀꜱᴇᴅ)
"""

ECHO_HANDLER = DisableAbleCommandHandler(
    "echo", echo, filters=Filters.chat_type.groups, run_async=True)
MD_HELP_HANDLER = CommandHandler("markdownhelp", markdown_help, run_async=True)
WIKI_HANDLER = DisableAbleCommandHandler("wiki", wiki)
WALLPAPER_HANDLER = DisableAbleCommandHandler("wall", wall, run_async=True)

dispatcher.add_handler(ECHO_HANDLER)
dispatcher.add_handler(MD_HELP_HANDLER)
dispatcher.add_handler(WIKI_HANDLER)
dispatcher.add_handler(WALLPAPER_HANDLER)

__mod_name__ = "EXTRAS"
__command_list__ = ["id", "echo", "wiki", "wall"]
__handlers__ = [
    ECHO_HANDLER,
    MD_HELP_HANDLER,
    WIKI_HANDLER,
    WALLPAPER_HANDLER,
]
