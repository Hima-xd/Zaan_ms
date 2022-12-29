import html
import random

from time import sleep
from telegram import (
    ParseMode,
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.error import BadRequest
from telegram.ext import CallbackContext, Filters, CommandHandler, run_async, CallbackQueryHandler
from telegram.utils.helpers import mention_html
from typing import Optional, List
from telegram import TelegramError

import KRISTY.modules.sql.users_sql as sql
from KRISTY.modules.disable import DisableAbleCommandHandler
from KRISTY.modules.helper_funcs.filters import CustomFilters
from KRISTY import (
    DEV_USERS,
    LOGGER,
    OWNER_ID,
    DRAGONS,
    DEMONS,
    TIGERS,
    WOLVES,
    dispatcher,
)
from KRISTY.modules.helper_funcs.chat_status import (
    user_admin_no_reply,
    bot_admin,
    can_restrict,
    connection_status,
    is_user_admin,
    is_user_ban_protected,
    is_user_in_chat,
    user_admin,
    user_can_ban,
    can_delete,
    dev_plus,
)
from KRISTY.modules.helper_funcs.extraction import extract_user_and_text
from KRISTY.modules.helper_funcs.string_handling import extract_time
from KRISTY.modules.log_channel import gloggable, loggable



@connection_status
@bot_admin
@can_restrict
@user_admin
@user_can_ban
@loggable
def ban(update: Update, context: CallbackContext) -> str:
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message
    log_message = ""
    bot = context.bot
    args = context.args
    reason = ""
    if message.reply_to_message and message.reply_to_message.sender_chat:
        r = bot.ban_chat_sender_chat(chat_id=chat.id, sender_chat_id=message.reply_to_message.sender_chat.id)
        if r:
            message.reply_text("ᴄʜᴀɴɴᴇʟ {} ᴡᴀꜱ ʙᴀɴɴᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ꜰʀᴏᴍ {} ʙᴀʙʏ🥀".format(
                html.escape(message.reply_to_message.sender_chat.title),
                html.escape(chat.title)
            ),
                parse_mode="html"
            )
        else:
            message.reply_text("ꜰᴀɪʟᴇᴅ ᴛᴏ ʙᴀɴ ᴄʜᴀɴɴᴇʟ ʙᴀʙʏ🥀")
        return

    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text("ᴜꜱᴇʀ ɴᴏᴛ ꜰᴏᴜɴᴅ ʙᴀʙʏ🥀.")
        return log_message
    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message != "User not found":
            raise
        message.reply_text("ᴄᴀɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ꜰɪɴᴅ ᴛʜɪꜱ ᴘᴇʀꜱᴏɴ ʙᴀʙʏ🥀.")
        return log_message
    if user_id == bot.id:
        message.reply_text("ᴏʜ ʏᴇᴀʜ, ʙᴀɴ ᴍʏꜱᴇʟꜰ, ɴᴏᴏʙ🥀!")
        return log_message

    if is_user_ban_protected(chat, user_id, member) and user not in DEV_USERS:
        if user_id == OWNER_ID:
            message.reply_text("ᴛʀʏɪɴɢ ᴛᴏ ᴘᴜᴛ ᴍᴇ ᴀɢᴀɪɴꜱᴛ ᴀ ᴋɪɴɢ ʜᴜʜ? ʙᴀʙʏ🥀")
        elif user_id in DEV_USERS:
            message.reply_text("ɪ ᴄᴀɴ'ᴛ ᴀᴄᴛ ᴀɢᴀɪɴꜱᴛ ᴏᴜʀ ᴘʀɪɴᴄᴇ ʙᴀʙʏ🥀.")
        elif user_id in DRAGONS:
            message.reply_text(
                "ꜰɪɢʜᴛɪɴɢ ᴛʜɪꜱ ᴇᴍᴘᴇʀᴏʀ ʜᴇʀᴇ ᴡɪʟʟ ᴘᴜᴛ ᴜꜱᴇʀ ʟɪᴠᴇꜱ ᴀᴛ ʀɪꜱᴋ ʙᴀʙʏ🥀."
            )
        elif user_id in DEMONS:
            message.reply_text(
                "ʙʀɪɴɢ ᴀɴ ᴏʀᴅᴇʀ ꜰʀᴏᴍ ᴄᴀᴘᴛᴀɪɴ ᴛᴏ ꜰɪɢʜᴛ ᴀ ᴀꜱꜱᴀꜱɪɴ ꜱᴇʀᴠᴀɴᴛ ʙᴀʙʏ🥀."
            )
        elif user_id in TIGERS:
            message.reply_text(
                "ʙʀɪɴɢ ᴀɴ ᴏʀᴅᴇʀ ꜰʀᴏᴍ ꜱᴏʟᴅɪᴇʀ ᴛᴏ ꜰɪɢʜᴛ ᴀ ʟᴀɴᴄᴇʀ ꜱᴇʀᴠᴀɴᴛ ʙᴀʙʏ🥀."
            )
        elif user_id in WOLVES:
            message.reply_text("ᴛʀᴀᴅᴇʀ ᴀᴄᴄᴇꜱꜱ ᴍᴀᴋᴇ ᴛʜᴇᴍ ʙᴀɴ ɪᴍᴍᴜɴᴇ ʙᴀʙʏ🥀!")
        else:
            message.reply_text("ɪ ᴄᴀɴɴᴏᴛ ʙᴀɴɴᴇᴅ ᴀᴅᴍɪɴ ʙᴀʙʏ🥀.")
        return log_message
    if message.text.startswith("/s"):
        silent = True
        if not can_delete(chat, context.bot.id):
            return ""
    else:
        silent = False
    log = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#{'S' if silent else ''}ʙᴀɴɴᴇᴅ\n"
        f"<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>ᴜꜱᴇʀ:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}"
    )
    if reason:
        log += "<b>ʀᴇᴀꜱᴏɴ:</b> {} ʙᴀʙʏ🥀".format(reason)

    try:
        chat.ban_member(user_id)

        if silent:
            if message.reply_to_message:
                message.reply_to_message.delete()
            message.delete()
            return log

        # bot.send_sticker(chat.id, BAN_STICKER)  # banhammer marie sticker
        reply = (
            f"{mention_html(member.user.id, html.escape(member.user.first_name))} [<code>{member.user.id}</code>] Banned."
        )
        if reason:
            reply += f"\nʀᴇᴀꜱᴏɴ: {html.escape(reason)} ʙᴀʙʏ🥀"

        bot.sendMessage(
            chat.id,
            reply,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="🔄  Unban", callback_data=f"unbanb_unban={user_id}"
                        ),
                        InlineKeyboardButton(text="🗑️  Delete", callback_data="unbanb_del"),
                    ]
                ]
            ),
            parse_mode=ParseMode.HTML,
        )
        return log

    except BadRequest as excp:
        if excp.message == "Reply message not found":
            # Do not reply
            if silent:
                return log
            message.reply_text("ʙᴀɴɴᴇᴅ ʙᴀʙʏ🥀!", quote=False)
            return log
        else:
            LOGGER.warning(update)
            LOGGER.exception(
                "ERROR banning user %s in chat %s (%s) due to %s",
                user_id,
                chat.title,
                chat.id,
                excp.message,
            )
            message.reply_text("ᴜʜᴍ...ᴛʜᴀᴛ ᴅɪᴅɴ'ᴛ ᴡᴏʀᴋ ʙᴀʙʏ🥀...")

    return log_message


@connection_status
@bot_admin
@can_restrict
@user_admin
@user_can_ban
@loggable
def temp_ban(update: Update, context: CallbackContext) -> str:
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message
    log_message = ""
    bot, args = context.bot, context.args
    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text("ᴜꜱᴇʀ ɴᴏᴛ ꜰᴏᴜɴᴅ ʙᴀʙʏ🥀.")
        return log_message

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message != "User not found":
            raise
        message.reply_text("ɪ ᴄᴀɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ꜰɪɴᴅ ᴛʜɪꜱ ᴜꜱᴇʀ ʙᴀʙʏ🥀.")
        return log_message
    if user_id == bot.id:
        message.reply_text("ɪ'ᴍ ɴᴏᴛ ɢᴏɴɴᴀ ʙᴀɴ ᴍʏꜱᴇʟꜰ, ᴀʀᴇ ʏᴏᴜ ᴄʀᴀᴢʏ? ʙᴀʙʏ🥀")
        return log_message

    if is_user_ban_protected(chat, user_id, member):
        message.reply_text("ɪ ᴅᴏɴ'ᴛ ꜰᴇᴇʟ ʟɪᴋᴇ ɪᴛ ʙᴀʙʏ🥀.")
        return log_message

    if not reason:
        message.reply_text("ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ ꜱᴘᴇᴄɪꜰɪᴇᴅ ᴀ ᴛɪᴍᴇ ᴛᴏ ʙᴀɴ ᴛʜɪꜱ ᴜꜱᴇʀ ꜰᴏʀ ʙᴀʙʏ🥀!")
        return log_message

    split_reason = reason.split(None, 1)

    time_val = split_reason[0].lower()
    reason = split_reason[1] if len(split_reason) > 1 else ""
    bantime = extract_time(message, time_val)

    if not bantime:
        return log_message

    log = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        "#ᴛᴇᴍᴘ_ʙᴀɴɴᴇᴅ\n"
        f"<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>ᴜꜱᴇʀ:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}\n"
        f"<b>ᴛɪᴍᴇ:</b> {time_val}"
    )
    if reason:
        log += "\nʀᴇᴀꜱᴏɴ: {} ʙᴀʙʏ🥀".format(reason)

    try:
        chat.ban_member(user_id, until_date=bantime)
        # bot.send_sticker(chat.id, BAN_STICKER)  # banhammer marie sticker

        reply_msg = (
            f"{mention_html(member.user.id, html.escape(member.user.first_name))} [<code>{member.user.id}</code>] ᴛᴇᴍᴘᴏʀᴀʀʏ ʙᴀɴɴᴇᴅ ʙᴀʙʏ🥀"
            f" ꜰᴏʀ (`{time_val}`). ʙᴀʙʏ🥀"
        )

        if reason:
            reply_msg += f"\nʀᴇᴀꜱᴏɴ: `{html.escape(reason)}` ʙᴀʙʏ🥀"

        bot.sendMessage(
            chat.id,
            reply_msg,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="🔄  Unban", callback_data=f"unbanb_unban={user_id}"
                        ),
                        InlineKeyboardButton(text="🗑️  Delete", callback_data="unbanb_del"),
                    ]
                ]
            ),
            parse_mode=ParseMode.HTML,
        )
        return log

    except BadRequest as excp:
        if excp.message == "Reply message not found":
            # Do not reply
            message.reply_text(
                f"{mention_html(member.user.id, html.escape(member.user.first_name))} [<code>{member.user.id}</code>] ʙᴀɴɴᴇᴅ ꜰᴏʀ {time_val} ʙᴀʙʏ🥀.", quote=False
            )
            return log
        else:
            LOGGER.warning(update)
            LOGGER.exception(
                "ERROR banning user %s in chat %s (%s) due to %s",
                user_id,
                chat.title,
                chat.id,
                excp.message,
            )
            message.reply_text("ᴡᴇʟʟ ᴅᴀᴍɴ, ɪ ᴄᴀɴ'ᴛ ʙᴀɴ ᴛʜᴀᴛ ᴜꜱᴇʀ ʙᴀʙʏ🥀.")

    return log_message


@connection_status
@bot_admin
@can_restrict
@user_admin_no_reply
@user_can_ban
@loggable
def unbanb_btn(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    query = update.callback_query
    chat = update.effective_chat
    user = update.effective_user
    if query.data != "unbanb_del":
        splitter = query.data.split("=")
        query_match = splitter[0]
        if query_match == "unbanb_unban":
            user_id = splitter[1]
            if not is_user_admin(chat, int(user.id)):
                bot.answer_callback_query(
                    query.id,
                    text="ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ʀɪɢʜᴛꜱ ᴛᴏ ᴜɴᴍᴜᴛᴇ ᴘᴇᴏᴘʟᴇ ʙᴀʙʏ🥀",
                    show_alert=True,
                )
                return ""
            log_message = ""
            try:
                member = chat.get_member(user_id)
            except BadRequest:
                pass
            chat.unban_member(user_id)
            query.message.edit_text(
                f"{member.user.first_name} [{member.user.id}] ᴜɴʙᴀɴɴᴇᴅ ʙᴀʙʏ🥀."
            )
            bot.answer_callback_query(query.id, text="ᴜɴʙᴀɴɴᴇᴅ ʙᴀʙʏ🥀!")
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"#ᴜɴʙᴀɴɴᴇᴅ\n"
                f"<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, user.first_name)}\n"
                f"<b>ᴜꜱᴇʀ:</b> {mention_html(member.user.id, member.user.first_name)}"
            )

    else:
        if not is_user_admin(chat, int(user.id)):
            bot.answer_callback_query(
                query.id,
                text="ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ʀɪɢʜᴛꜱ ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴛʜɪꜱ ᴍᴇꜱꜱᴀɢᴇ ʙᴀʙʏ🥀.",
                show_alert=True,
            )
            return ""
        query.message.delete()
        bot.answer_callback_query(query.id, text="ᴅᴇʟᴇᴛᴇᴅ ʙᴀʙʏ🥀!")
        return ""

    
@connection_status
@bot_admin
@can_restrict
@user_admin
@user_can_ban
@loggable
def punch(update: Update, context: CallbackContext) -> str:
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message
    log_message = ""
    bot, args = context.bot, context.args
    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text("ᴜꜱᴇʀ ɴᴏᴛ ꜰᴏᴜɴᴅ ʙᴀʙʏ🥀")
        return log_message

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message != "User not found":
            raise

        message.reply_text("ɪ ᴄᴀɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ꜰɪɴᴅ ᴛʜɪꜱ ᴜꜱᴇʀ ʙᴀʙʏ🥀.")
        return log_message
    if user_id == bot.id:
        message.reply_text("ʏᴇᴀʜʜʜ ɪ'ᴍ ɴᴏᴛ ɢᴏɴɴᴀ ᴅᴏ ᴛʜᴀᴛ ʙᴀʙʏ🥀.")
        return log_message

    if is_user_ban_protected(chat, user_id):
        message.reply_text("ɪ ʀᴇᴀʟʟʏ ᴡɪꜱʜ ɪ ᴄᴏᴜʟᴅ ᴘᴜɴᴄʜ ᴛʜɪꜱ ᴜꜱᴇʀ ʙᴀʙʏ🥀...")
        return log_message

    res = chat.unban_member(user_id)  # unban on current user = kick
    if res:
        # bot.send_sticker(chat.id, BAN_STICKER)  # banhammer marie sticker
        bot.sendMessage(
            chat.id,
            f"{mention_html(member.user.id, html.escape(member.user.first_name))} [<code>{member.user.id}</code>] ᴋɪᴄᴋᴇᴅ ʙᴀʙʏ🥀.",
            parse_mode=ParseMode.HTML
        )
        log = (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"#ᴋɪᴄᴋᴇᴅ\n"
            f"<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>ᴜꜱᴇʀ:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}"
        )
        if reason:
            log += f"\n<b>ʀᴇᴀꜱᴏɴ:</b> {reason} ʙᴀʙʏ🥀"

        return log

    else:
        message.reply_text("ᴡᴇʟʟ ᴅᴀᴍɴ, ɪ ᴄᴀɴ'ᴛ ᴘᴜɴᴄʜ ᴛʜᴀᴛ ᴜꜱᴇʀ ʙᴀʙʏ🥀.")

    return log_message



@bot_admin
@can_restrict
def punchme(update: Update, context: CallbackContext):
    user_id = update.effective_message.from_user.id
    if is_user_admin(update.effective_chat, user_id):
        update.effective_message.reply_text("ɪ ᴡɪꜱʜ ɪ ᴄᴏᴜʟᴅ... ʙᴜᴛ ʏᴏᴜ'ʀᴇ ᴀɴ ᴀᴅᴍɪɴ ʙᴀʙʏ🥀.")
        return

    res = update.effective_chat.unban_member(user_id)  # unban on current user = kick
    if res:
        update.effective_message.reply_text(
            "ᴘᴜɴᴄʜᴇꜱ ʏᴏᴜ ᴏᴜᴛ ᴏꜰ ᴛʜᴇ ɢʀᴏᴜᴘ ʙᴀʙʏ🥀!!",
        )
    else:
        update.effective_message.reply_text("ʜᴜʜ? ɪ ᴄᴀɴ'ᴛ ʙᴀʙʏ🥀")


@connection_status
@bot_admin
@can_restrict
@user_admin
@user_can_ban
@loggable
def unban(update: Update, context: CallbackContext) -> Optional[str]:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    log_message = ""
    bot, args = context.bot, context.args
    if message.reply_to_message and message.reply_to_message.sender_chat:
        r = bot.unban_chat_sender_chat(chat_id=chat.id, sender_chat_id=message.reply_to_message.sender_chat.id)
        if r:
            message.reply_text("ᴄʜᴀɴɴᴇʟ {} ᴡᴀꜱ ᴜɴʙᴀɴɴᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ꜰʀᴏᴍ {} ʙᴀʙʏ🥀".format(
                html.escape(message.reply_to_message.sender_chat.title),
                html.escape(chat.title)
            ),
                parse_mode="html"
            )
        else:
            message.reply_text("ꜰᴀɪʟᴇᴅ ᴛᴏ ᴜɴʙᴀɴ ᴄʜᴀɴɴᴇʟ ʙᴀʙʏ🥀")
        return

    user_id, reason = extract_user_and_text(message, args)
    if not user_id:
        message.reply_text("ᴜꜱᴇʀ ɴᴏᴛ ꜰᴏᴜɴᴅ ʙᴀʙʏ🥀.")
        return log_message

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message != "User not found":
            raise
        message.reply_text("ɪ ᴄᴀɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ꜰɪɴᴅ ᴛʜɪꜱ ᴜꜱᴇʀ ʙᴀʙʏ🥀.")
        return log_message
    if user_id == bot.id:
        message.reply_text("ʜᴏᴡ ᴡᴏᴜʟᴅ ɪ ᴜɴʙᴀɴ ᴍʏꜱᴇʟꜰ ɪꜰ ɪ ᴡᴀꜱɴ'ᴛ ʜᴇʀᴇ...? ʙᴀʙʏ🥀")
        return log_message

    if is_user_in_chat(chat, user_id):
        message.reply_text(f"ᴜꜱᴇʀ ɴᴏᴛ ꜰᴏᴜɴᴅ ʙᴀʙʏ🥀.")
        return log_message

    chat.unban_member(user_id)
    message.reply_text(
        f"{member.user.first_name} [{member.user.id}] ᴜɴʙᴀɴɴᴇᴅ ʙᴀʙʏ🥀."
    )

    log = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#UNBANNED\n"
        f"<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>ᴜꜱᴇʀ:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}"
    )
    if reason:
        log += f"\n<b>ʀᴇᴀꜱᴏɴ:</b> {reason} ʙᴀʙʏ🥀"

    return log


@connection_status
@bot_admin
@can_restrict
@gloggable
def selfunban(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    bot, args = context.bot, context.args
    if user.id not in DRAGONS or user.id not in TIGERS:
        return

    try:
        chat_id = int(args[0])
    except:
        message.reply_text("ɢɪᴠᴇ ᴀ ᴠᴀʟɪᴅ ᴄʜᴀᴛ ɪᴅ ʙᴀʙʏ🥀.")
        return

    chat = bot.getChat(chat_id)

    try:
        member = chat.get_member(user.id)
    except BadRequest as excp:
        if excp.message == "User not found":
            message.reply_text("ɪ ᴄᴀɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ꜰɪɴᴅ ᴛʜɪꜱ ᴜꜱᴇʀ ʙᴀʙʏ🥀.")
            return
        else:
            raise

    if is_user_in_chat(chat, user.id):
        message.reply_text("ᴀʀᴇɴ'ᴛ ʏᴏᴜ ᴀʟʀᴇᴀᴅʏ ɪɴ ᴛʜᴇ ᴄʜᴀᴛ?? ʙᴀʙʏ🥀")
        return

    chat.unban_member(user.id)
    message.reply_text(f"ʏᴇᴘ, ɪ ʜᴀᴠᴇ ᴜɴʙᴀɴɴᴇᴅ ᴛʜᴇ ᴜꜱᴇʀ ʙᴀʙʏ🥀.")

    log = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#UNBANNED\n"
        f"<b>ᴜꜱᴇʀ:</b> {mention_html(member.user.id, html.escape(member.user.first_name))} ʙᴀʙʏ🥀"
    )

    return log


@bot_admin
@can_restrict
@loggable
def banme(update: Update, context: CallbackContext):
    user_id = update.effective_message.from_user.id
    chat = update.effective_chat
    user = update.effective_user
    if is_user_admin(update.effective_chat, user_id):
        update.effective_message.reply_text("ɪ ᴄᴀɴɴᴏᴛ ʙᴀɴɴᴇᴅ ᴀᴅᴍɪɴ ʙᴀʙʏ🥀.")
        return

    res = update.effective_chat.ban_member(user_id)
    if res:
        update.effective_message.reply_text("ʏᴇꜱ, ʏᴏᴜ'ʀᴇ ʀɪɢʜᴛ! ʙᴀʙʏ🥀")
        return (
            "<b>{}:</b>"
            "\n#ʙᴀɴᴍᴇ"
            "\n<b>ᴜꜱᴇʀ:</b> {}"
            "\n<b>ID:</b> <code>{}</code>".format(
                html.escape(chat.title),
                mention_html(user.id, user.first_name),
                user_id,
            )
        )

    else:
        update.effective_message.reply_text("ʜᴜʜ? ɪ ᴄᴀɴ'ᴛ ʙᴀʙʏ🥀")


@dev_plus
def snipe(update: Update, context: CallbackContext):
    args = context.args
    bot = context.bot
    try:
        chat_id = str(args[0])
        del args[0]
    except TypeError:
        update.effective_message.reply_text("ᴘʟᴇᴀꜱᴇ ɢɪᴠᴇ ᴍᴇ ᴀ ᴄʜᴀᴛ ᴛᴏ ᴇᴄʜᴏ ᴛᴏ ʙᴀʙʏ🥀!")
    to_send = " ".join(args)
    if len(to_send) >= 2:
        try:
            bot.sendMessage(int(chat_id), str(to_send))
        except TelegramError:
            LOGGER.warning("Couldn't send to group %s", str(chat_id))
            update.effective_message.reply_text(
                "ᴄᴏᴜʟᴅɴ'ᴛ ꜱᴇɴᴅ ᴛʜᴇ ᴍᴇꜱꜱᴀɢᴇ. ᴘᴇʀʜᴀᴘꜱ ɪ'ᴍ ɴᴏᴛ ᴘᴀʀᴛ ᴏꜰ ᴛʜᴀᴛ ɢʀᴏᴜᴘ? ʙᴀʙʏ🥀"
            )


__help__ = """
*ᴜꜱᴇʀ ᴄᴏᴍᴍᴀɴᴅꜱ:*

» `/kickme`*:* ᴋɪᴄᴋꜱ ᴛʜᴇ ᴜꜱᴇʀ ᴡʜᴏ ɪꜱꜱᴜᴇᴅ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ

*ᴀᴅᴍɪɴꜱ ᴏɴʟʏ:*

» `/ban` <ᴜꜱᴇʀʜᴀɴᴅʟᴇ>*:* ʙᴀɴꜱ ᴀ ᴜꜱᴇʀ. (ᴠɪᴀ ʜᴀɴᴅʟᴇ, ᴏʀ ʀᴇᴘʟʏ)
» `/sban` <ᴜꜱᴇʀʜᴀɴᴅʟᴇ>*:* ꜱɪʟᴇɴᴛʟʏ ʙᴀɴ ᴀ ᴜꜱᴇʀ. ᴅᴇʟᴇᴛᴇꜱ ᴄᴏᴍᴍᴀɴᴅ, ʀᴇᴘʟɪᴇᴅ ᴍᴇꜱꜱᴀɢᴇ ᴀɴᴅ ᴅᴏᴇꜱɴ'ᴛ ʀᴇᴘʟʏ. (ᴠɪᴀ ʜᴀɴᴅʟᴇ, ᴏʀ ʀᴇᴘʟʏ)
» `/tban` <ᴜꜱᴇʀʜᴀɴᴅʟᴇ> x(ᴍ/ʜ/ᴅ)*:* ʙᴀɴꜱ ᴀ ᴜꜱᴇʀ ꜰᴏʀ x ᴛɪᴍᴇ. (ᴠɪᴀ ʜᴀɴᴅʟᴇ, ᴏʀ ʀᴇᴘʟʏ). ᴍ = ᴍɪɴᴜᴛᴇꜱ, ʜ = ʜᴏᴜʀꜱ, ᴅ = ᴅᴀʏꜱ.
» `/unban` <ᴜꜱᴇʀʜᴀɴᴅʟᴇ>*:* ᴜɴʙᴀɴꜱ ᴀ ᴜꜱᴇʀ. (ᴠɪᴀ ʜᴀɴᴅʟᴇ, ᴏʀ ʀᴇᴘʟʏ)
» `/kick` <ᴜꜱᴇʀʜᴀɴᴅʟᴇ>*:* ᴋɪᴄᴋꜱ ᴀ ᴜꜱᴇʀ ᴏᴜᴛ ᴏꜰ ᴛʜᴇ ɢʀᴏᴜᴘ, (ᴠɪᴀ ʜᴀɴᴅʟᴇ, ᴏʀ ʀᴇᴘʟʏ)
» `/mute` <ᴜꜱᴇʀʜᴀɴᴅʟᴇ>*:* ꜱɪʟᴇɴᴄᴇꜱ ᴀ ᴜꜱᴇʀ. ᴄᴀɴ ᴀʟꜱᴏ ʙᴇ ᴜꜱᴇᴅ ᴀꜱ ᴀ ʀᴇᴘʟʏ, ᴍᴜᴛɪɴɢ ᴛʜᴇ ʀᴇᴘʟɪᴇᴅ ᴛᴏ ᴜꜱᴇʀ.
» `/tmute` <ᴜꜱᴇʀʜᴀɴᴅʟᴇ> x(ᴍ/ʜ/ᴅ)*:* ᴍᴜᴛᴇꜱ ᴀ ᴜꜱᴇʀ ꜰᴏʀ x ᴛɪᴍᴇ. (ᴠɪᴀ ʜᴀɴᴅʟᴇ, ᴏʀ ʀᴇᴘʟʏ). ᴍ = ᴍɪɴᴜᴛᴇꜱ, ʜ = ʜᴏᴜʀꜱ, ᴅ = ᴅᴀʏꜱ.
» `/unmute` <ᴜꜱᴇʀʜᴀɴᴅʟᴇ>*:* ᴜɴᴍᴜᴛᴇꜱ ᴀ ᴜꜱᴇʀ. ᴄᴀɴ ᴀʟꜱᴏ ʙᴇ ᴜꜱᴇᴅ ᴀꜱ ᴀ ʀᴇᴘʟʏ, ᴍᴜᴛɪɴɢ ᴛʜᴇ ʀᴇᴘʟɪᴇᴅ ᴛᴏ ᴜꜱᴇʀ.

*ᴄʜᴀɴɴᴇʟ ʙᴀɴꜱ*

`/channelban`*:* ʙᴀɴꜱ ᴄʜᴀɴɴᴇʟ ᴀᴄᴛɪᴏɴ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ
`/cban`*:* ʙᴀɴꜱ ᴄʜᴀɴɴᴇʟ ᴀᴄᴛɪᴏɴ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ
`/channelunban`*:* ʙᴀɴꜱ ᴄʜᴀɴɴᴇʟ ᴀᴄᴛɪᴏɴ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ
`/uncban`*:* ʙᴀɴꜱ ᴄʜᴀɴɴᴇʟ ᴀᴄᴛɪᴏɴ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ

*ɢʟᴏʙᴀʟ~ʙᴀɴꜱ*

`/gmute`*:* ɢʟᴏʙᴀʟʟʏ ᴍᴜᴛᴇꜱ ᴜꜱᴇʀ ᴡʜɪᴄʜ ʜᴀꜱ ʙᴇᴇɴ ᴛᴀɢɢᴇᴅ
`/ungmute`*:* ɢʟᴏʙᴀʟʟʏ ᴜɴᴍᴜᴛᴇꜱ ᴜꜱᴇʀ ᴡʜɪᴄʜ ʜᴀꜱ ʙᴇᴇɴ ᴛᴀɢɢᴇᴅ
`/gmutelist`*:* ʟɪꜱᴛ ᴏꜰ ɢ-ᴍᴜᴛᴇ ᴜꜱᴇʀꜱ ɪɴ ᴛʜᴇ ᴅᴀᴛᴀʙᴀꜱᴇ
`/gmutespam`*:* ɢ-ᴍᴜᴛᴇ ꜰᴏʀ ꜱᴘᴀᴍᴍᴇʀꜱ
`/gban`*:* ɢʟᴏʙᴀʟʟʏ ʙᴀɴꜱ ᴀ ᴜꜱᴇʀ ᴡʜɪᴄʜ ʜᴀꜱ ʙᴇᴇɴ ᴛᴀɢɢᴇᴅ
`/ungban`*:* ɢʟᴏʙᴀʟʟʏ ᴜɴʙᴀɴꜱ ᴀ ᴜꜱᴇʀ ᴡʜɪᴄʜ ʜᴀꜱ ʙᴇᴇɴ ᴛᴀɢɢᴇᴅ
`/gbanlist`*:* ʟɪꜱᴛ ᴏꜰ ᴀʟʟ ɢ-ʙᴀɴ ᴜꜱᴇʀꜱ ɪɴ ᴛʜᴇ ᴅᴀᴛᴀʙᴀꜱᴇ

*Remote commands:*

 » `/rban`*:* user group*:* ʀᴇᴍᴏᴛᴇ ʙᴀɴ 
 » `/runban`*:* user group*:* ʀᴇᴍᴏᴛᴇ ᴜɴʙᴀɴ
 » `/rpunch`*:* user group*:* ʀᴇᴍᴏᴛᴇ ᴋɪᴄᴋ
 » `/rmute`*:* user group*:* ʀᴇᴍᴏᴛᴇ ᴍᴜᴛᴇ
 » `/runmute`*:* user group*:* ʀᴇᴍᴏᴛᴇ ᴜɴᴍᴜᴛᴇ
"""


__mod_name__ = "BANS/MUTES"

BAN_HANDLER = CommandHandler(["ban", "sban"], ban, run_async=True)
TEMPBAN_HANDLER = CommandHandler(["tban"], temp_ban, run_async=True)
KICK_HANDLER = CommandHandler(["kick", "punch"], punch, run_async=True)
UNBAN_HANDLER = CommandHandler("unban", unban, run_async=True)
ROAR_HANDLER = CommandHandler("roar", selfunban, run_async=True)
UNBAN_BUTTON_HANDLER = CallbackQueryHandler(unbanb_btn, pattern=r"unbanb_")
KICKME_HANDLER = DisableAbleCommandHandler(["kickme", "punchme"], punchme, filters=Filters.chat_type.groups, run_async=True)
SNIPE_HANDLER = CommandHandler("snipe", snipe, pass_args=True, filters=CustomFilters.sudo_filter, run_async=True)
BANME_HANDLER = CommandHandler("banme", banme, run_async=True)

dispatcher.add_handler(BAN_HANDLER)
dispatcher.add_handler(TEMPBAN_HANDLER)
dispatcher.add_handler(KICK_HANDLER)
dispatcher.add_handler(UNBAN_HANDLER)
dispatcher.add_handler(ROAR_HANDLER)
dispatcher.add_handler(KICKME_HANDLER)
dispatcher.add_handler(UNBAN_BUTTON_HANDLER)
dispatcher.add_handler(SNIPE_HANDLER)
dispatcher.add_handler(BANME_HANDLER)

__handlers__ = [
    BAN_HANDLER,
    TEMPBAN_HANDLER,
    KICK_HANDLER,
    UNBAN_HANDLER,
    ROAR_HANDLER,
    KICKME_HANDLER,
    UNBAN_BUTTON_HANDLER,
    SNIPE_HANDLER,
    BANME_HANDLER,
]
