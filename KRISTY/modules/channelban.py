import html
from typing import Optional
from telegram import (
    ParseMode,
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import CallbackContext, Filters, CommandHandler, run_async, CallbackQueryHandler
from telegram.error import BadRequest
from telegram.ext import CallbackContext, CommandHandler, Filters, run_async
from telegram.utils.helpers import mention_html

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
import KRISTY.modules.sql.users_sql as sql
from KRISTY.modules.disable import DisableAbleCommandHandler
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
)
from KRISTY.modules.helper_funcs.extraction import extract_user_and_text
from KRISTY.modules.helper_funcs.string_handling import extract_time
from KRISTY.modules.log_channel import gloggable, loggable
from KRISTY.modules.helper_funcs.anonymous import user_admin, AdminPerms


UNBAN_IMG= "https://telegra.ph/file/8484d80ea96188e6f5502.mp4"
BAN_IMG= "https://telegra.ph/file/fa5fa39f85af08f9b3c06.mp4"

@run_async
@connection_status
@bot_admin
@can_restrict
@user_admin(AdminPerms.CAN_RESTRICT_MEMBERS)
@loggable
def cban(update: Update, context: CallbackContext) -> Optional[str]: 
    chat = update.effective_chat  
    user = update.effective_user 
    message = update.effective_message 
    args = context.args
    bot = context.bot
    log_message = ""
    reason = ""
    if message.reply_to_message and message.reply_to_message.sender_chat:
        r = bot._request.post(bot.base_url + '/banChatSenderChat', {
            'sender_chat_id': message.reply_to_message.sender_chat.id,
            'chat_id': chat.id
        },
                              )
        if r:
            message.reply_video(BAN_IMG,caption="ᴄʜᴀɴɴᴇʟ {} ᴡᴀꜱ ʙᴀɴɴᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ꜰʀᴏᴍ {} ʙᴀʙʏ🥀".format(
                html.escape(message.reply_to_message.sender_chat.title),
                html.escape(chat.title)
            ),
                parse_mode="html"
            )
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"#ᴄʜᴀɴɴᴇʟ \n"
                f"<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, user.first_name)}\n"
                f"<b>ᴄʜᴀɴɴᴇʟ :</b> {mention_html(channel.id, html.escape(chat.title))} ({message.reply_to_message.sender_chat.id})"
            )
        else:
            message.reply_text("ꜰᴀɪʟᴇᴅ ᴛᴏ ʙᴀɴ ᴄʜᴀɴɴᴇʟ ʙᴀʙʏ🥀")
        return

    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text("ɪ ᴅᴏᴜʙᴛ ᴛʜᴀᴛ'ꜱ ᴀ ᴜꜱᴇʀ ʙᴀʙʏ🥀.")
        return log_message

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message != "User not found":
            raise

        message.reply_text("ᴄᴀɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ꜰɪɴᴅ ᴛʜɪꜱ ᴘᴇʀꜱᴏɴ ʙᴀʙʏ🥀.")
        return log_message
    if user_id == context.bot.id:
        message.reply_text("ᴏʜ ʏᴇᴀʜ, ʙᴀɴ ᴍʏꜱᴇʟꜰ,  ʙᴀʙʏ🥀")
        return log_message

    if is_user_ban_protected(update, user_id, member) and user not in DEV_USERS:
        if user_id == OWNER_ID:
            message.reply_text("ɪ'ᴅ ɴᴇᴠᴇʀ ʙᴀɴ ᴍʏ ᴏᴡɴᴇʀ ʙᴀʙʏ🥀.")
        elif user_id in DEV_USERS:
            message.reply_text("ɪ ᴄᴀɴ'ᴛ ᴀᴄᴛ ᴀɢᴀɪɴꜱᴛ ᴏᴜʀ ᴏᴡɴ ʙᴀʙʏ🥀.")
        elif user_id in DRAGONS:
            message.reply_text("ᴍʏ ꜱᴜᴅᴏꜱ ᴀʀᴇ ʙᴀɴ ɪᴍᴍᴜɴᴇ ʙᴀʙʏ🥀")
        elif user_id in DEMONS:
            message.reply_text("ᴍʏ ꜱᴜᴘᴘᴏʀᴛ ᴜꜱᴇʀꜱ ᴀʀᴇ ʙᴀɴ ɪᴍᴍᴜɴᴇ ʙᴀʙʏ🥀")
        elif user_id in TIGERS:
            message.reply_text("ꜱᴏʀʀʏ, ʜᴇ ɪꜱ ᴛɪɢᴇʀ ʟᴇᴠᴇʟ ᴅɪꜱᴀꜱᴛᴇʀ ʙᴀʙʏ🥀.")
        elif user_id in WOLVES:
            message.reply_text("ɴᴇᴘᴛᴜɴɪᴀɴꜱ ᴀʀᴇ ʙᴀɴ ɪᴍᴍᴜɴᴇ ʙᴀʙʏ🥀!")
        else:
            message.reply_text("ᴛʜɪꜱ ᴜꜱᴇʀ ʜᴀꜱ ɪᴍᴍᴜɴɪᴛʏ ᴀɴᴅ ᴄᴀɴɴᴏᴛ ʙᴇ ʙᴀɴɴᴇᴅ ʙᴀʙʏ🥀.")
        return log_message
    log = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#ʙᴀɴɴᴇᴅ\n"
        f"<b>ʙᴀɴɴᴇᴅ:</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>ᴜꜱᴇʀ:</b> {mention_html(member.user.id, member.user.first_name)}"
    )
    if reason:
        log += "\n<b>ʀᴇᴀꜱᴏɴ:</b> {} ʙᴀʙʏ🥀".format(reason)

    try:
        chat.ban_member(user_id)
        # context.bot.send_sticker(chat.id, BAN_STICKER)  # banhammer marie sticker
        context.bot.sendMessage(
            chat.id,
            "{} ᴡᴀꜱ ʙᴀɴɴᴇᴅ ʙʏ {} ɪɴ <b>{}</ʙ> ʙᴀʙʏ🥀\n<b>ʀᴇᴀꜱᴏɴ</b>: <code>{}</code>".format(
                mention_html(member.user.id, member.user.first_name), mention_html(user.id, user.first_name),
                message.chat.title, reason
            ),
            parse_mode=ParseMode.HTML,
        )
        return log

    except BadRequest as excp:
        if excp.message == "Reply message not found":
            # Do not reply
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
            message.reply_text("ᴡᴇʟʟ ᴅᴀᴍɴ, ɪ ᴄᴀɴ'ᴛ ʙᴀɴ ᴛʜᴀᴛ ᴜꜱᴇʀ ʙᴀʙʏ🥀.")

    return ""
  
@run_async
@connection_status
@bot_admin
@can_restrict
@user_admin(AdminPerms.CAN_RESTRICT_MEMBERS)
@loggable
def uncban(update: Update, context: CallbackContext) -> Optional[str]:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    log_message = ""
    bot, args = context.bot, context.args
    if message.reply_to_message and message.reply_to_message.sender_chat:
        r = bot.unban_chat_sender_chat(chat_id=chat.id, sender_chat_id=message.reply_to_message.sender_chat.id)
        if r:
            message.reply_video(UNBAN_IMG,caption="ᴄʜᴀɴɴᴇʟ {} ᴡᴀꜱ ᴜɴʙᴀɴɴᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ꜰʀᴏᴍ {} ʙᴀʙʏ🥀".format(
                html.escape(message.reply_to_message.sender_chat.title),
                html.escape(chat.title)
            ),
                parse_mode="html"
            )
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"#ᴜɴᴄʙᴀɴɴᴇᴅ\n"
                f"<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, user.first_name)}\n"
                f"<b>ᴄʜᴀɴɴᴇʟ:</b> {html.escape(message.reply_to_message.sender_chat.title)} ({message.reply_to_message.sender_chat.id})"
            )
        else:
            message.reply_text("ꜰᴀɪʟᴇᴅ ᴛᴏ ᴜɴʙᴀɴ ᴄʜᴀɴɴᴇʟ ʙᴀʙʏ🥀")
        return
    user_id, reason = extract_user_and_text(message, args)
    if not user_id:
        message.reply_text("ɪ ᴅᴏᴜʙᴛ ᴛʜᴀᴛ'ꜱ ᴀ ᴜꜱᴇʀ ʙᴀʙʏ🥀.")
        return log_message

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message != 'User not found':
            raise
        message.reply_text("ɪ ᴄᴀɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ꜰɪɴᴅ ᴛʜɪꜱ ᴜꜱᴇʀ ʙᴀʙʏ🥀.")
        return log_message
    if user_id == bot.id:
        message.reply_text("ʜᴏᴡ ᴡᴏᴜʟᴅ ɪ ᴜɴʙᴀɴ ᴍʏꜱᴇʟꜰ ɪꜰ ɪ ᴡᴀꜱɴ'ᴛ ʜᴇʀᴇ ʙᴀʙʏ🥀...?")
        return log_message

    if is_user_in_chat(chat, user_id):
        message.reply_text("ɪꜱɴ'ᴛ ᴛʜɪꜱ ᴘᴇʀꜱᴏɴ ᴀʟʀᴇᴀᴅʏ ʜᴇʀᴇ ʙᴀʙʏ🥀??")
        return log_message

    chat.unban_member(user_id)
    bot.sendMessage(
        chat.id,
        "{} ᴡᴀꜱ ᴜɴʙᴀɴɴᴇᴅ ʙʏ {} ɪɴ <b>{}</b> ʙᴀʙʏ🥀\n<b>ʀᴇᴀꜱᴏɴ</b>: <code>{}</code>".format(
            mention_html(member.user.id, member.user.first_name), mention_html(user.id, user.first_name),
            message.chat.title, reason
        ),
        parse_mode=ParseMode.HTML,
    )

    log = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#ᴜɴᴄʙᴀɴɴᴇᴅ\n"
        f"<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>ᴜꜱᴇʀ:</b> {mention_html(member.user.id, member.user.first_name)}"
    )
    if reason:
        log += f"\n<b>ʀᴇᴀꜱᴏɴ:</b> {reason}"

    return log
    
    
UNCBAN_HANDLER = CommandHandler(["channelunban", "uncban"], uncban)
CBAN_HANDLER = CommandHandler(["cban", "channelban"], cban)
    
dispatcher.add_handler(UNCBAN_HANDLER)
dispatcher.add_handler(CBAN_HANDLER)
    
    
    
