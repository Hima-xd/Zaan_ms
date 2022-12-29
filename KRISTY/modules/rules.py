from typing import Optional

import KRISTY.modules.sql.rules_sql as sql
from KRISTY import dispatcher
from KRISTY.modules.helper_funcs.chat_status import user_admin
from KRISTY.modules.helper_funcs.string_handling import markdown_parser
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    ParseMode,
    Update,
    User,
)
from telegram.error import BadRequest
from telegram.ext import CallbackContext, CommandHandler, Filters
from telegram.utils.helpers import escape_markdown


def get_rules(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    send_rules(update, chat_id)


# Do not async - not from a handler
def send_rules(update, chat_id, from_pm=False):
    bot = dispatcher.bot
    user = update.effective_user  # type: Optional[User]
    reply_msg = update.message.reply_to_message
    try:
        chat = bot.get_chat(chat_id)
    except BadRequest as excp:
        if excp.message == "chat not found" and from_pm:
            bot.send_message(
                user.id,
                "ᴛʜᴇ ʀᴜʟᴇꜱ ꜱʜᴏʀᴛᴄᴜᴛ ꜰᴏʀ ᴛʜɪꜱ ᴄʜᴀᴛ ʜᴀꜱɴ'ᴛ ʙᴇᴇɴ ꜱᴇᴛ ᴘʀᴏᴘᴇʀʟʏ! ᴀꜱᴋ ᴀᴅᴍɪɴꜱ ᴛᴏ ʙᴀʙʏ🥀"
                "ꜰɪx ᴛʜɪꜱ.\nᴍᴀʏʙᴇ ᴛʜᴇʏ ꜰᴏʀɢᴏᴛ ᴛʜᴇ ʜʏᴘʜᴇɴ ɪɴ ɪᴅ ʙᴀʙʏ🥀",
            )
            return
        raise

    rules = sql.get_rules(chat_id)
    text = f"ᴛʜᴇ ʀᴜʟᴇꜱ ꜰᴏʀ *{escape_markdown(chat.title)}* ᴀʀᴇ:\n\n{rules}"

    if from_pm and rules:
        bot.send_message(
            user.id,
            text,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
    elif from_pm:
        bot.send_message(
            user.id,
            "ᴛʜᴇ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴꜱ ʜᴀᴠᴇɴ'ᴛ ꜱᴇᴛ ᴀɴʏ ʀᴜʟᴇꜱ ꜰᴏʀ ᴛʜɪꜱ ᴄʜᴀᴛ ʏᴇᴛ ʙᴀʙʏ🥀. "
            "ᴛʜɪꜱ ᴘʀᴏʙᴀʙʟʏ ᴅᴏᴇꜱɴ'ᴛ ᴍᴇᴀɴ ɪᴛ'ꜱ ʟᴀᴡʟᴇꜱꜱ ᴛʜᴏᴜɢʜ ʙᴀʙʏ🥀...! ",
        )
    elif rules and reply_msg:
        reply_msg.reply_text(
            "ᴘʟᴇᴀꜱᴇ ᴄʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ꜱᴇᴇ ᴛʜᴇ ʀᴜʟᴇꜱ ʙᴀʙʏ🥀.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Rules",
                            url=f"t.me/{bot.username}?start={chat_id}",
                        ),
                    ],
                ],
            ),
        )
    elif rules:
        update.effective_message.reply_text(
            "ᴘʟᴇᴀꜱᴇ ᴄʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ꜱᴇᴇ ᴛʜᴇ ʀᴜʟᴇꜱ ʙᴀʙʏ🥀.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Rules",
                            url=f"t.me/{bot.username}?start={chat_id}",
                        ),
                    ],
                ],
            ),
        )
    else:
        update.effective_message.reply_text(
            "ᴛʜᴇ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴꜱ ʜᴀᴠᴇɴ'ᴛ ꜱᴇᴛ ᴀɴʏ ʀᴜʟᴇꜱ ꜰᴏʀ ᴛʜɪꜱ ᴄʜᴀᴛ ʏᴇᴛ ʙᴀʙʏ🥀. "
            "ᴛʜɪꜱ ᴘʀᴏʙᴀʙʟʏ ᴅᴏᴇꜱɴ'ᴛ ᴍᴇᴀɴ ɪᴛ'ꜱ ʟᴀᴡʟᴇꜱꜱ ᴛʜᴏᴜɢʜ ʙᴀʙʏ🥀...!",
        )


@user_admin
def set_rules(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    msg = update.effective_message  # type: Optional[Message]
    raw_text = msg.text
    args = raw_text.split(None, 1)  # use python's maxsplit to separate cmd and args
    if len(args) == 2:
        txt = args[1]
        offset = len(txt) - len(raw_text)  # set correct offset relative to command
        markdown_rules = markdown_parser(
            txt,
            entities=msg.parse_entities(),
            offset=offset,
        )

        sql.set_rules(chat_id, markdown_rules)
        update.effective_message.reply_text("ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ꜱᴇᴛ ʀᴜʟᴇꜱ ꜰᴏʀ ᴛʜɪꜱ ɢʀᴏᴜᴘ ʙᴀʙʏ🥀.")


@user_admin
def clear_rules(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    sql.set_rules(chat_id, "")
    update.effective_message.reply_text("ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴄʟᴇᴀʀᴇᴅ ʀᴜʟᴇꜱ ʙᴀʙʏ🥀!")


def __stats__():
    return f"× {sql.num_chats()} ᴄʜᴀᴛꜱ ʜᴀᴠᴇ ʀᴜʟᴇꜱ ꜱᴇᴛ ʙᴀʙʏ🥀."


def __import_data__(chat_id, data):
    # set chat rules
    rules = data.get("info", {}).get("rules", "")
    sql.set_rules(chat_id, rules)


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)


def __chat_settings__(chat_id, user_id):
    return f"ᴛʜɪꜱ ᴄʜᴀᴛ ʜᴀꜱ ʜᴀᴅ ɪᴛ'ꜱ ʀᴜʟᴇꜱ ꜱᴇᴛ: `{bool(sql.get_rules(chat_id))}` ʙᴀʙʏ🥀"


__mod_name__ = "RULES"

GET_RULES_HANDLER = CommandHandler(
    "rules", get_rules, filters=Filters.chat_type.groups, run_async=True
)
SET_RULES_HANDLER = CommandHandler(
    "setrules", set_rules, filters=Filters.chat_type.groups, run_async=True
)
RESET_RULES_HANDLER = CommandHandler(
    "clearrules", clear_rules, filters=Filters.chat_type.groups, run_async=True
)

dispatcher.add_handler(GET_RULES_HANDLER)
dispatcher.add_handler(SET_RULES_HANDLER)
dispatcher.add_handler(RESET_RULES_HANDLER)
