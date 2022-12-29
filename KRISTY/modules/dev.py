import os
import subprocess
import sys

from contextlib import suppress
from time import sleep

import KRISTY

from KRISTY import dispatcher
from KRISTY.modules.helper_funcs.chat_status import dev_plus
from telegram import TelegramError, Update
from telegram.error import Unauthorized
from telegram.ext import CallbackContext, CommandHandler


@dev_plus
def allow_groups(update: Update, context: CallbackContext):
    args = context.args
    if not args:
        state = "Lockdown is " + "on" if not KRISTY.ALLOW_CHATS else "off"
        update.effective_message.reply_text(f"Current state: {state}")
        return
    if args[0].lower() in ["off", "no"]:
        KRISTY.ALLOW_CHATS = True
    elif args[0].lower() in ["yes", "on"]:
        KRISTY.ALLOW_CHATS = False
    else:
        update.effective_message.reply_text("Format: /lockdown Yes/No or Off/On ʙᴀʙʏ🥀")
        return
    update.effective_message.reply_text("ᴅᴏɴᴇ! ʟᴏᴄᴋᴅᴏᴡɴ ᴠᴀʟᴜᴇ ᴛᴏɢɢʟᴇᴅ ʙᴀʙʏ🥀.")


@dev_plus
def leave(update: Update, context: CallbackContext):
    bot = context.bot
    args = context.args
    if args:
        chat_id = str(args[0])
        try:
            bot.leave_chat(int(chat_id))
        except TelegramError:
            update.effective_message.reply_text(
                "ʙᴇᴇᴘ ʙᴏᴏᴘ, ɪ ᴄᴏᴜʟᴅ ɴᴏᴛ ʟᴇᴀᴠᴇ ᴛʜᴀᴛ ɢʀᴏᴜᴘ(ᴅᴜɴɴᴏ ᴡʜʏ ᴛʜᴏ) ʙᴀʙʏ🥀.",
            )
            return
        with suppress(Unauthorized):
            update.effective_message.reply_text("ʙᴇᴇᴘ ʙᴏᴏᴘ, ɪ ʟᴇꜰᴛ ᴛʜᴀᴛ ꜱᴏᴜᴘ ʙᴀʙʏ🥀!.")
    else:
        update.effective_message.reply_text("ꜱᴇɴᴅ ᴀ ᴠᴀʟɪᴅ ᴄʜᴀᴛ ɪᴅ ʙᴀʙʏ🥀")


@dev_plus
def gitpull(update: Update, context: CallbackContext):
    sent_msg = update.effective_message.reply_text(
        "ᴘᴜʟʟɪɴɢ ᴀʟʟ ᴄʜᴀɴɢᴇꜱ ꜰʀᴏᴍ ʀᴇᴍᴏᴛᴇ ᴀɴᴅ ᴛʜᴇɴ ᴀᴛᴛᴇᴍᴘᴛɪɴɢ ᴛᴏ ʀᴇꜱᴛᴀʀᴛ ʙᴀʙʏ🥀.",
    )
    subprocess.Popen("git pull", stdout=subprocess.PIPE, shell=True)

    sent_msg_text = sent_msg.text + "\n\nᴄʜᴀɴɢᴇꜱ ᴘᴜʟʟᴇᴅ ʙᴀʙʏ🥀...ɪ ɢᴜᴇꜱꜱ.. ʀᴇꜱᴛᴀʀᴛɪɴɢ ɪɴ "

    for i in reversed(range(5)):
        sent_msg.edit_text(sent_msg_text + str(i + 1))
        sleep(1)

    sent_msg.edit_text("ʀᴇꜱᴛᴀʀᴛᴇᴅ ʙᴀʙʏ🥀.")

    os.system("restart.bat")
    os.execv("start.bat", sys.argv)


@dev_plus
def restart(update: Update, context: CallbackContext):
    update.effective_message.reply_text(
        "ꜱᴛᴀʀᴛɪɴɢ ᴀ ɴᴇᴡ ɪɴꜱᴛᴀɴᴄᴇ ᴀɴᴅ ꜱʜᴜᴛᴛɪɴɢ ᴅᴏᴡɴ ᴛʜɪꜱ ᴏɴᴇ ʙᴀʙʏ🥀",
    )

    os.system("restart.bat")
    os.execv("start.bat", sys.argv)


LEAVE_HANDLER = CommandHandler("leave", leave, run_async=True)
GITPULL_HANDLER = CommandHandler("gitpull", gitpull, run_async=True)
RESTART_HANDLER = CommandHandler("reboot", restart, run_async=True)
ALLOWGROUPS_HANDLER = CommandHandler("lockdown", allow_groups, run_async=True)

dispatcher.add_handler(ALLOWGROUPS_HANDLER)
dispatcher.add_handler(LEAVE_HANDLER)
dispatcher.add_handler(GITPULL_HANDLER)
dispatcher.add_handler(RESTART_HANDLER)

__mod_name__ = "DEV"
__handlers__ = [LEAVE_HANDLER, GITPULL_HANDLER, RESTART_HANDLER, ALLOWGROUPS_HANDLER]
