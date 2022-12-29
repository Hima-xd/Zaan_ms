import sre_constants

import regex
import telegram
from KRISTY import LOGGER, dispatcher
from KRISTY.modules.disable import DisableAbleMessageHandler
from KRISTY.modules.helper_funcs.regex_helper import infinite_loop_check
from telegram import Update
from telegram.ext import CallbackContext, Filters, run_async

DELIMITERS = ("/", ":", "|", "_")


def separate_sed(sed_string):
    if (
        len(sed_string) >= 3
        and sed_string[1] in DELIMITERS
        and sed_string.count(sed_string[1]) >= 2
    ):
        delim = sed_string[1]
        start = counter = 2
        while counter < len(sed_string):
            if sed_string[counter] == "\\":
                counter += 1

            elif sed_string[counter] == delim:
                replace = sed_string[start:counter]
                counter += 1
                start = counter
                break

            counter += 1

        else:
            return None

        while counter < len(sed_string):
            if (
                sed_string[counter] == "\\"
                and counter + 1 < len(sed_string)
                and sed_string[counter + 1] == delim
            ):
                sed_string = sed_string[:counter] + sed_string[counter + 1 :]

            elif sed_string[counter] == delim:
                replace_with = sed_string[start:counter]
                counter += 1
                break

            counter += 1
        else:
            return replace, sed_string[start:], ""

        flags = ""
        if counter < len(sed_string):
            flags = sed_string[counter:]
        return replace, replace_with, flags.lower()


@run_async
def sed(update: Update, context: CallbackContext):
    sed_result = separate_sed(update.effective_message.text)
    if sed_result and update.effective_message.reply_to_message:
        if update.effective_message.reply_to_message.text:
            to_fix = update.effective_message.reply_to_message.text
        elif update.effective_message.reply_to_message.caption:
            to_fix = update.effective_message.reply_to_message.caption
        else:
            return

        repl, repl_with, flags = sed_result
        if not repl:
            update.effective_message.reply_to_message.reply_text(
                "ʏᴏᴜ'ʀᴇ ᴛʀʏɪɴɢ ᴛᴏ ʀᴇᴘʟᴀᴄᴇ... " "ɴᴏᴛʜɪɴɢ ᴡɪᴛʜ ꜱᴏᴍᴇᴛʜɪɴɢ? ʙᴀʙʏ🥀"
            )
            return

        try:
            try:
                check = regex.match(repl, to_fix, flags=regex.IGNORECASE, timeout=5)
            except TimeoutError:
                return
            if check and check.group(0).lower() == to_fix.lower():
                update.effective_message.reply_to_message.reply_text(
                    "ʜᴇʏ ᴇᴠᴇʀʏᴏɴᴇ, {} ɪꜱ ᴛʀʏɪɴɢ ᴛᴏ ᴍᴀᴋᴇ "
                    "ᴍᴇ ꜱᴀʏ ꜱᴛᴜꜰꜰ ɪ ᴅᴏɴ'ᴛ ᴡᴀɴɴᴀ "
                    "ꜱᴀʏ ʙᴀʙʏ🥀!".format(update.effective_user.first_name)
                )
                return
            if infinite_loop_check(repl):
                update.effective_message.reply_text(
                    "ɪ'ᴍ ᴀꜰʀᴀɪᴅ ɪ ᴄᴀɴ'ᴛ ʀᴜɴ ᴛʜᴀᴛ ʀᴇɢᴇx ʙᴀʙʏ🥀."
                )
                return
            if "i" in flags and "g" in flags:
                text = regex.sub(
                    repl, repl_with, to_fix, flags=regex.I, timeout=3
                ).strip()
            elif "i" in flags:
                text = regex.sub(
                    repl, repl_with, to_fix, count=1, flags=regex.I, timeout=3
                ).strip()
            elif "g" in flags:
                text = regex.sub(repl, repl_with, to_fix, timeout=3).strip()
            else:
                text = regex.sub(repl, repl_with, to_fix, count=1, timeout=3).strip()
        except TimeoutError:
            update.effective_message.reply_text("Timeout")
            return
        except sre_constants.error:
            LOGGER.warning(update.effective_message.text)
            LOGGER.exception("SRE constant error")
            update.effective_message.reply_text("ᴅᴏ ʏᴏᴜ ᴇᴠᴇɴ ꜱᴇᴅ? ᴀᴘᴘᴀʀᴇɴᴛʟʏ ɴᴏᴛ ʙᴀʙʏ🥀.")
            return

        # empty string errors -_-
        if len(text) >= telegram.MAX_MESSAGE_LENGTH:
            update.effective_message.reply_text(
                "ᴛʜᴇ ʀᴇꜱᴜʟᴛ ᴏꜰ ᴛʜᴇ ꜱᴇᴅ ᴄᴏᴍᴍᴀɴᴅ ᴡᴀꜱ ᴛᴏᴏ ʟᴏɴɢ ꜰᴏʀ \
                                                  ᴛᴇʟᴇɢʀᴀᴍ ʙᴀʙʏ🥀!"
            )
        elif text:
            update.effective_message.reply_to_message.reply_text(text)


__mod_name__ = "Sed/Regex"

SED_HANDLER = DisableAbleMessageHandler(
    Filters.regex(r"s([{}]).*?\1.*".format("".join(DELIMITERS))), sed, friendly="sed"
)

dispatcher.add_handler(SED_HANDLER)
