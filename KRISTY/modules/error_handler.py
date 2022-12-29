import html
import io
import random
import sys
import traceback

import pretty_errors
import requests
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, CommandHandler

from KRISTY import dispatcher, ERROR_LOG, DEV_USERS

pretty_errors.mono()


class ErrorsDict(dict):
    """A custom dict to store errors and their count"""

    def __init__(self, *args, **kwargs):
        self.raw = []
        super().__init__(*args, **kwargs)

    def __contains__(self, error):
        self.raw.append(error)
        error.identifier = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=5))
        for e in self:
            if type(e) is type(error) and e.args == error.args:
                self[e] += 1
                return True
        self[error] = 0
        return False

    def __len__(self):
        return len(self.raw)


errors = ErrorsDict()


def error_callback(update: Update, context: CallbackContext):
    if not update:
        return
    if context.error not in errors:
        try:
            stringio = io.StringIO()
            pretty_errors.output_stderr = stringio
            output = pretty_errors.excepthook(
                type(context.error),
                context.error,
                context.error.__traceback__,
            )
            pretty_errors.output_stderr = sys.stderr
            pretty_error = stringio.getvalue()
            stringio.close()
        except:
            pretty_error = "ꜰᴀɪʟᴇᴅ ᴛᴏ ᴄʀᴇᴀᴛᴇ ᴘʀᴇᴛᴛʏ ᴇʀʀᴏʀ ʙᴀʙʏ🥀."
        tb_list = traceback.format_exception(
            None,
            context.error,
            context.error.__traceback__,
        )
        tb = "".join(tb_list)
        pretty_message = (
            "{}\n"
            "-------------------------------------------------------------------------------\n"
            "ᴀɴ ᴇxᴄᴇᴘᴛɪᴏɴ ᴡᴀꜱ ʀᴀɪꜱᴇᴅ ᴡʜɪʟᴇ ʜᴀɴᴅʟɪɴɢ ᴀɴ ᴜᴘᴅᴀᴛᴇ ʙᴀʙʏ🥀\n"
            "ᴜꜱᴇʀ: {}\n"
            "ᴄʜᴀᴛ: {} {}\n"
            "ᴄᴀʟʟʙᴀᴄᴋ ᴅᴀᴛᴀ: {}\n"
            "ᴍᴇꜱꜱᴀɢᴇ: {}\n\n"
            "ꜰᴜʟʟ ᴛʀᴀᴄᴇʙᴀᴄᴋ: {}"
        ).format(
            pretty_error,
            update.effective_user.id,
            update.effective_chat.title if update.effective_chat else "",
            update.effective_chat.id if update.effective_chat else "",
            update.callback_query.data if update.callback_query else "None",
            update.effective_message.text if update.effective_message else "No message",
            tb,
        )
        key = requests.post(
            "https://www.toptal.com/developers/hastebin/documents",
            data=pretty_message.encode("UTF-8"),
        ).json()
        e = html.escape(f"{context.error}")
        if not key.get("key"):
            with open("error.txt", "w+") as f:
                f.write(pretty_message)
            context.bot.send_document(
                ERROR_LOG,
                open("error.txt", "rb"),
                caption=f"#{context.error.identifier}\n<b>ʏᴏᴜʀ ꜰᴇᴀᴛᴜʀᴇ'ꜱ ᴍᴀᴋᴇ ᴀɴ ᴇʀʀᴏʀ ꜰᴏʀ ʏᴏᴜ, ᴄʜᴇᴄᴋ ᴛʜɪꜱ ʙᴀʙʏ🥀:"
                f"</b>\n<code>{e}</code>",
                parse_mode="html",
            )
            return
        key = key.get("key")
        url = f"https://www.toptal.com/developers/hastebin/{key}"
        context.bot.send_message(
            ERROR_LOG,
            text=f"#{context.error.identifier}\n<b>ʏᴏᴜʀ ꜰᴇᴀᴛᴜʀᴇ'ꜱ ᴍᴀᴋᴇ ᴀɴ ᴇʀʀᴏʀ ꜰᴏʀ ʏᴏᴜ, ᴄʜᴇᴄᴋ ᴛʜɪꜱ ʙᴀʙʏ🥀:"
            f"</b>\n<code>{e}</code>",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Cursed Errors", url=url)]],
            ),
            parse_mode="html",
        )


def list_errors(update: Update, context: CallbackContext):
    if update.effective_user.id not in DEV_USERS:
        return
    e = dict(sorted(errors.items(), key=lambda item: item[1], reverse=True))
    msg = "<b>ᴇʀʀᴏʀꜱ ʟɪꜱᴛ:</b>\n"
    for x, value in e.items():
        msg += f"• <code>{x}:</code> <b>{value}</b> #{x.identifier}\n"
    msg += f"{len(errors)} ʜᴀᴠᴇ ᴏᴄᴄᴜʀʀᴇᴅ ꜱɪɴᴄᴇ ꜱᴛᴀʀᴛᴜᴘ ʙᴀʙʏ🥀."
    if len(msg) > 4096:
        with open("errors_msg.txt", "w+") as f:
            f.write(msg)
        context.bot.send_document(
            update.effective_chat.id,
            open("errors_msg.txt", "rb"),
            caption="ᴛᴏᴏ ᴍᴀɴʏ ᴇʀʀᴏʀꜱ ʜᴀᴠᴇ ᴏᴄᴄᴜʀᴇᴅ ʙᴀʙʏ🥀...",
            parse_mode="html",
        )
        return
    update.effective_message.reply_text(msg, parse_mode="html")


dispatcher.add_error_handler(error_callback)
dispatcher.add_handler(CommandHandler("errors", list_errors))
