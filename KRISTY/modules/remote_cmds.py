from KRISTY import dispatcher
from KRISTY.modules.helper_funcs.chat_status import (
    bot_admin, is_bot_admin, is_user_ban_protected, is_user_in_chat)
from KRISTY.modules.helper_funcs.extraction import extract_user_and_text
from KRISTY.modules.helper_funcs.filters import CustomFilters
from telegram import Update, ChatPermissions
from telegram.error import BadRequest
from telegram.ext import CallbackContext, CommandHandler, run_async

RBAN_ERRORS = {
    "User is an administrator of the chat", "Chat not found",
    "Not enough rights to restrict/unrestrict chat member",
    "User_not_participant", "Peer_id_invalid", "Group chat was deactivated",
    "Need to be inviter of a user to punch it from a basic group",
    "Chat_admin_required",
    "Only the creator of a basic group can punch group administrators",
    "Channel_private", "Not in the chat"
}

RUNBAN_ERRORS = {
    "User is an administrator of the chat", "Chat not found",
    "Not enough rights to restrict/unrestrict chat member",
    "User_not_participant", "Peer_id_invalid", "Group chat was deactivated",
    "Need to be inviter of a user to punch it from a basic group",
    "Chat_admin_required",
    "Only the creator of a basic group can punch group administrators",
    "Channel_private", "Not in the chat"
}

RKICK_ERRORS = {
    "User is an administrator of the chat", "Chat not found",
    "Not enough rights to restrict/unrestrict chat member",
    "User_not_participant", "Peer_id_invalid", "Group chat was deactivated",
    "Need to be inviter of a user to punch it from a basic group",
    "Chat_admin_required",
    "Only the creator of a basic group can punch group administrators",
    "Channel_private", "Not in the chat"
}

RMUTE_ERRORS = {
    "User is an administrator of the chat", "Chat not found",
    "Not enough rights to restrict/unrestrict chat member",
    "User_not_participant", "Peer_id_invalid", "Group chat was deactivated",
    "Need to be inviter of a user to punch it from a basic group",
    "Chat_admin_required",
    "Only the creator of a basic group can punch group administrators",
    "Channel_private", "Not in the chat"
}

RUNMUTE_ERRORS = {
    "User is an administrator of the chat", "Chat not found",
    "Not enough rights to restrict/unrestrict chat member",
    "User_not_participant", "Peer_id_invalid", "Group chat was deactivated",
    "Need to be inviter of a user to punch it from a basic group",
    "Chat_admin_required",
    "Only the creator of a basic group can punch group administrators",
    "Channel_private", "Not in the chat"
}


@run_async
@bot_admin
def rban(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message

    if not args:
        message.reply_text("ʏᴏᴜ ᴅᴏɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ʙᴇ ʀᴇꜰᴇʀʀɪɴɢ ᴛᴏ ᴀ ᴄʜᴀᴛ/ᴜꜱᴇʀ ʙᴀʙʏ🥀.")
        return

    user_id, chat_id = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text(
            "ʏᴏᴜ ᴅᴏɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ʙᴇ ʀᴇꜰᴇʀʀɪɴɢ ᴛᴏ ᴀ ᴜꜱᴇʀ ᴏʀ ᴛʜᴇ ɪᴅ ꜱᴘᴇᴄɪꜰɪᴇᴅ ɪꜱ ɪɴᴄᴏʀʀᴇᴄᴛ ʙᴀʙʏ🥀.."
        )
        return
    elif not chat_id:
        message.reply_text("ʏᴏᴜ ᴅᴏɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ʙᴇ ʀᴇꜰᴇʀʀɪɴɢ ᴛᴏ ᴀ ᴄʜᴀᴛ ʙᴀʙʏ🥀.")
        return

    try:
        chat = bot.get_chat(chat_id.split()[0])
    except BadRequest as excp:
        if excp.message == "Chat not found":
            message.reply_text(
                "ᴄʜᴀᴛ ɴᴏᴛ ꜰᴏᴜɴᴅ! ᴍᴀᴋᴇ ꜱᴜʀᴇ ʏᴏᴜ ᴇɴᴛᴇʀᴇᴅ ᴀ ᴠᴀʟɪᴅ ᴄʜᴀᴛ ɪᴅ ᴀɴᴅ ɪ'ᴍ ᴘᴀʀᴛ ᴏꜰ ᴛʜᴀᴛ ᴄʜᴀᴛ ʙᴀʙʏ🥀."
            )
            return
        else:
            raise

    if chat.type == 'private':
        message.reply_text("ɪ'ᴍ ꜱᴏʀʀʏ, ʙᴜᴛ ᴛʜᴀᴛ'ꜱ ᴀ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ ʙᴀʙʏ🥀!")
        return

    if not is_bot_admin(chat, bot.id) or not chat.get_member(
            bot.id).can_restrict_members:
        message.reply_text(
            "ɪ ᴄᴀɴ'ᴛ ʀᴇꜱᴛʀɪᴄᴛ ᴘᴇᴏᴘʟᴇ ᴛʜᴇʀᴇ! ᴍᴀᴋᴇ ꜱᴜʀᴇ ɪ'ᴍ ᴀᴅᴍɪɴ ᴀɴᴅ ᴄᴀɴ ʙᴀɴ ᴜꜱᴇʀꜱ ʙᴀʙʏ🥀."
        )
        return

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "User not found":
            message.reply_text("ɪ ᴄᴀɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ꜰɪɴᴅ ᴛʜɪꜱ ᴜꜱᴇʀ ʙᴀʙʏ🥀")
            return
        else:
            raise

    if is_user_ban_protected(chat, user_id, member):
        message.reply_text("ɪ ʀᴇᴀʟʟʏ ᴡɪꜱʜ ɪ ᴄᴏᴜʟᴅ ʙᴀɴ ᴀᴅᴍɪɴꜱ ʙᴀʙʏ🥀...")
        return

    if user_id == bot.id:
        message.reply_text("ɪ'ᴍ ɴᴏᴛ ɢᴏɴɴᴀ ʙᴀɴ ᴍʏꜱᴇʟꜰ, ᴀʀᴇ ʏᴏᴜ ᴄʀᴀᴢʏ ʙᴀʙʏ🥀?")
        return

    try:
        chat.kick_member(user_id)
        message.reply_text("ʙᴀɴɴᴇᴅ ꜰʀᴏᴍ ᴄʜᴀᴛ ʙᴀʙʏ🥀!")
    except BadRequest as excp:
        if excp.message == "Reply message not found":
            # Do not reply
            message.reply_text('Banned!', quote=False)
        elif excp.message in RBAN_ERRORS:
            message.reply_text(excp.message)
        else:
            LOGGER.warning(update)
            LOGGER.exception("ERROR banning user %s in chat %s (%s) due to %s",
                             user_id, chat.title, chat.id, excp.message)
            message.reply_text("ᴡᴇʟʟ ᴅᴀᴍɴ, ɪ ᴄᴀɴ'ᴛ ʙᴀɴ ᴛʜᴀᴛ ᴜꜱᴇʀ ʙᴀʙʏ🥀.")


@run_async
@bot_admin
def runban(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message

    if not args:
        message.reply_text("ʏᴏᴜ ᴅᴏɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ʙᴇ ʀᴇꜰᴇʀʀɪɴɢ ᴛᴏ ᴀ ᴄʜᴀᴛ/ᴜꜱᴇʀ ʙᴀʙʏ🥀.")
        return

    user_id, chat_id = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text(
            "ʏᴏᴜ ᴅᴏɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ʙᴇ ʀᴇꜰᴇʀʀɪɴɢ ᴛᴏ ᴀ ᴜꜱᴇʀ ᴏʀ ᴛʜᴇ ɪᴅ ꜱᴘᴇᴄɪꜰɪᴇᴅ ɪꜱ ɪɴᴄᴏʀʀᴇᴄᴛ ʙᴀʙʏ🥀.."
        )
        return
    elif not chat_id:
        message.reply_text("ʏᴏᴜ ᴅᴏɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ʙᴇ ʀᴇꜰᴇʀʀɪɴɢ ᴛᴏ ᴀ ᴄʜᴀᴛ ʙᴀʙʏ🥀.")
        return

    try:
        chat = bot.get_chat(chat_id.split()[0])
    except BadRequest as excp:
        if excp.message == "Chat not found":
            message.reply_text(
                "ᴄʜᴀᴛ ɴᴏᴛ ꜰᴏᴜɴᴅ! ᴍᴀᴋᴇ ꜱᴜʀᴇ ʏᴏᴜ ᴇɴᴛᴇʀᴇᴅ ᴀ ᴠᴀʟɪᴅ ᴄʜᴀᴛ ɪᴅ ᴀɴᴅ ɪ'ᴍ ᴘᴀʀᴛ ᴏꜰ ᴛʜᴀᴛ ᴄʜᴀᴛ ʙᴀʙʏ🥀."
            )
            return
        else:
            raise

    if chat.type == 'private':
        message.reply_text("ɪ'ᴍ ꜱᴏʀʀʏ, ʙᴜᴛ ᴛʜᴀᴛ'ꜱ ᴀ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ ʙᴀʙʏ🥀!")
        return

    if not is_bot_admin(chat, bot.id) or not chat.get_member(
            bot.id).can_restrict_members:
        message.reply_text(
            "ɪ ᴄᴀɴ'ᴛ ᴜɴʀᴇꜱᴛʀɪᴄᴛ ᴘᴇᴏᴘʟᴇ ᴛʜᴇʀᴇ! ᴍᴀᴋᴇ ꜱᴜʀᴇ ɪ'ᴍ ᴀᴅᴍɪɴ ᴀɴᴅ ᴄᴀɴ ᴜɴʙᴀɴ ᴜꜱᴇʀꜱ ʙᴀʙʏ🥀.",
        )
        return

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "User not found":
            message.reply_text("ɪ ᴄᴀɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ꜰɪɴᴅ ᴛʜɪꜱ ᴜꜱᴇʀ ʙᴀʙʏ🥀 there")
            return
        else:
            raise

    if is_user_in_chat(chat, user_id):
        message.reply_text(
            "ᴡʜʏ ᴀʀᴇ ʏᴏᴜ ᴛʀʏɪɴɢ ᴛᴏ ʀᴇᴍᴏᴛᴇʟʏ ᴜɴʙᴀɴ ꜱᴏᴍᴇᴏɴᴇ ᴛʜᴀᴛ'ꜱ ᴀʟʀᴇᴀᴅʏ ɪɴ ᴛʜᴀᴛ ᴄʜᴀᴛ ʙᴀʙʏ🥀?"
        )
        return

    if user_id == bot.id:
        message.reply_text("ɪ'ᴍ ɴᴏᴛ ɢᴏɴɴᴀ ᴜɴʙᴀɴ ᴍʏꜱᴇʟꜰ, ɪ'ᴍ ᴀɴ ᴀᴅᴍɪɴ ᴛʜᴇʀᴇ ʙᴀʙʏ🥀!")
        return

    try:
        chat.unban_member(user_id)
        message.reply_text("ʏᴇᴘ, ᴛʜɪꜱ ᴜꜱᴇʀ ᴄᴀɴ ᴊᴏɪɴ ᴛʜᴀᴛ ᴄʜᴀᴛ ʙᴀʙʏ🥀!")
    except BadRequest as excp:
        if excp.message == "Reply message not found":
            # Do not reply
            message.reply_text('Unbanned!', quote=False)
        elif excp.message in RUNBAN_ERRORS:
            message.reply_text(excp.message)
        else:
            LOGGER.warning(update)
            LOGGER.exception(
                "ERROR unbanning user %s in chat %s (%s) due to %s", user_id,
                chat.title, chat.id, excp.message)
            message.reply_text("ᴡᴇʟʟ ᴅᴀᴍɴ, ɪ ᴄᴀɴ'ᴛ ᴜɴʙᴀɴ ᴛʜᴀᴛ ᴜꜱᴇʀ ʙᴀʙʏ🥀.")


@run_async
@bot_admin
def rkick(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message

    if not args:
        message.reply_text("ʏᴏᴜ ᴅᴏɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ʙᴇ ʀᴇꜰᴇʀʀɪɴɢ ᴛᴏ ᴀ ᴄʜᴀᴛ/ᴜꜱᴇʀ ʙᴀʙʏ🥀.")
        return

    user_id, chat_id = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text(
            "ʏᴏᴜ ᴅᴏɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ʙᴇ ʀᴇꜰᴇʀʀɪɴɢ ᴛᴏ ᴀ ᴜꜱᴇʀ ᴏʀ ᴛʜᴇ ɪᴅ ꜱᴘᴇᴄɪꜰɪᴇᴅ ɪꜱ ɪɴᴄᴏʀʀᴇᴄᴛ ʙᴀʙʏ🥀.."
        )
        return
    elif not chat_id:
        message.reply_text("ʏᴏᴜ ᴅᴏɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ʙᴇ ʀᴇꜰᴇʀʀɪɴɢ ᴛᴏ ᴀ ᴄʜᴀᴛ ʙᴀʙʏ🥀.")
        return

    try:
        chat = bot.get_chat(chat_id.split()[0])
    except BadRequest as excp:
        if excp.message == "Chat not found":
            message.reply_text(
                "ᴄʜᴀᴛ ɴᴏᴛ ꜰᴏᴜɴᴅ! ᴍᴀᴋᴇ ꜱᴜʀᴇ ʏᴏᴜ ᴇɴᴛᴇʀᴇᴅ ᴀ ᴠᴀʟɪᴅ ᴄʜᴀᴛ ɪᴅ ᴀɴᴅ ɪ'ᴍ ᴘᴀʀᴛ ᴏꜰ ᴛʜᴀᴛ ᴄʜᴀᴛ ʙᴀʙʏ🥀."
            )
            return
        else:
            raise

    if chat.type == 'private':
        message.reply_text("ɪ'ᴍ ꜱᴏʀʀʏ, ʙᴜᴛ ᴛʜᴀᴛ'ꜱ ᴀ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ ʙᴀʙʏ🥀!")
        return

    if not is_bot_admin(chat, bot.id) or not chat.get_member(
            bot.id).can_restrict_members:
        message.reply_text(
            "ɪ ᴄᴀɴ'ᴛ ʀᴇꜱᴛʀɪᴄᴛ ᴘᴇᴏᴘʟᴇ ᴛʜᴇʀᴇ! ᴍᴀᴋᴇ ꜱᴜʀᴇ ɪ'ᴍ ᴀᴅᴍɪɴ ᴀɴᴅ ᴄᴀɴ ᴘᴜɴᴄʜ ᴜꜱᴇʀꜱ ʙᴀʙʏ🥀.",
        )
        return

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "User not found":
            message.reply_text("ɪ ᴄᴀɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ꜰɪɴᴅ ᴛʜɪꜱ ᴜꜱᴇʀ ʙᴀʙʏ🥀")
            return
        else:
            raise

    if is_user_ban_protected(chat, user_id, member):
        message.reply_text("ɪ ʀᴇᴀʟʟʏ ᴡɪꜱʜ ɪ ᴄᴏᴜʟᴅ ᴘᴜɴᴄʜ ᴀᴅᴍɪɴꜱ ʙᴀʙʏ🥀...")
        return

    if user_id == bot.id:
        message.reply_text("ɪ'ᴍ ɴᴏᴛ ɢᴏɴɴᴀ ᴘᴜɴᴄʜ ᴍʏꜱᴇʟꜰ, ᴀʀᴇ ʏᴏᴜ ᴄʀᴀᴢʏ ʙᴀʙʏ🥀?")
        return

    try:
        chat.unban_member(user_id)
        message.reply_text("ᴘᴜɴᴄʜᴇᴅ ꜰʀᴏᴍ ᴄʜᴀᴛ ʙᴀʙʏ🥀!")
    except BadRequest as excp:
        if excp.message == "Reply message not found":
            # Do not reply
            message.reply_text('ᴘᴜɴᴄʜᴇᴅ ʙᴀʙʏ🥀!', quote=False)
        elif excp.message in RKICK_ERRORS:
            message.reply_text(excp.message)
        else:
            LOGGER.warning(update)
            LOGGER.exception("ERROR punching user %s in chat %s (%s) due to %s",
                             user_id, chat.title, chat.id, excp.message)
            message.reply_text("ᴡᴇʟʟ ᴅᴀᴍɴ, ɪ ᴄᴀɴ'ᴛ ᴘᴜɴᴄʜ ᴛʜᴀᴛ ᴜꜱᴇʀ ʙᴀʙʏ🥀.")


@run_async
@bot_admin
def rmute(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message

    if not args:
        message.reply_text("ʏᴏᴜ ᴅᴏɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ʙᴇ ʀᴇꜰᴇʀʀɪɴɢ ᴛᴏ ᴀ ᴄʜᴀᴛ/ᴜꜱᴇʀ ʙᴀʙʏ🥀.")
        return

    user_id, chat_id = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text(
            "ʏᴏᴜ ᴅᴏɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ʙᴇ ʀᴇꜰᴇʀʀɪɴɢ ᴛᴏ ᴀ ᴜꜱᴇʀ ᴏʀ ᴛʜᴇ ɪᴅ ꜱᴘᴇᴄɪꜰɪᴇᴅ ɪꜱ ɪɴᴄᴏʀʀᴇᴄᴛ ʙᴀʙʏ🥀.."
        )
        return
    elif not chat_id:
        message.reply_text("ʏᴏᴜ ᴅᴏɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ʙᴇ ʀᴇꜰᴇʀʀɪɴɢ ᴛᴏ ᴀ ᴄʜᴀᴛ ʙᴀʙʏ🥀.")
        return

    try:
        chat = bot.get_chat(chat_id.split()[0])
    except BadRequest as excp:
        if excp.message == "Chat not found":
            message.reply_text(
                "ᴄʜᴀᴛ ɴᴏᴛ ꜰᴏᴜɴᴅ! ᴍᴀᴋᴇ ꜱᴜʀᴇ ʏᴏᴜ ᴇɴᴛᴇʀᴇᴅ ᴀ ᴠᴀʟɪᴅ ᴄʜᴀᴛ ɪᴅ ᴀɴᴅ ɪ'ᴍ ᴘᴀʀᴛ ᴏꜰ ᴛʜᴀᴛ ᴄʜᴀᴛ ʙᴀʙʏ🥀."
            )
            return
        else:
            raise

    if chat.type == 'private':
        message.reply_text("ɪ'ᴍ ꜱᴏʀʀʏ, ʙᴜᴛ ᴛʜᴀᴛ'ꜱ ᴀ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ ʙᴀʙʏ🥀!")
        return

    if not is_bot_admin(chat, bot.id) or not chat.get_member(
            bot.id).can_restrict_members:
        message.reply_text(
            "ɪ ᴄᴀɴ'ᴛ ʀᴇꜱᴛʀɪᴄᴛ ᴘᴇᴏᴘʟᴇ ᴛʜᴇʀᴇ! ᴍᴀᴋᴇ ꜱᴜʀᴇ ɪ'ᴍ ᴀᴅᴍɪɴ ᴀɴᴅ ᴄᴀɴ ᴍᴜᴛᴇ ᴜꜱᴇʀꜱ ʙᴀʙʏ🥀.",
        )
        return

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "User not found":
            message.reply_text("ɪ ᴄᴀɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ꜰɪɴᴅ ᴛʜɪꜱ ᴜꜱᴇʀ ʙᴀʙʏ🥀")
            return
        else:
            raise

    if is_user_ban_protected(chat, user_id, member):
        message.reply_text("ɪ ʀᴇᴀʟʟʏ ᴡɪꜱʜ ɪ ᴄᴏᴜʟᴅ ᴍᴜᴛᴇ ᴀᴅᴍɪɴꜱ ʙᴀʙʏ🥀...")
        return

    if user_id == bot.id:
        message.reply_text("ɪ'ᴍ ɴᴏᴛ ɢᴏɴɴᴀ ᴍᴜᴛᴇ ᴍʏꜱᴇʟꜰ, ᴀʀᴇ ʏᴏᴜ ᴄʀᴀᴢʏ ʙᴀʙʏ🥀?")
        return

    try:
        bot.restrict_chat_member(
            chat.id,
            user_id,
            permissions=ChatPermissions(can_send_messages=False))
        message.reply_text("ᴍᴜᴛᴇᴅ ꜰʀᴏᴍ ᴛʜᴇ ᴄʜᴀᴛ ʙᴀʙʏ🥀!")
    except BadRequest as excp:
        if excp.message == "Reply message not found":
            # Do not reply
            message.reply_text('Muted!', quote=False)
        elif excp.message in RMUTE_ERRORS:
            message.reply_text(excp.message)
        else:
            LOGGER.warning(update)
            LOGGER.exception("ERROR mute user %s in chat %s (%s) due to %s",
                             user_id, chat.title, chat.id, excp.message)
            message.reply_text("ᴡᴇʟʟ ᴅᴀᴍɴ, ɪ ᴄᴀɴ'ᴛ ᴍᴜᴛᴇ ᴛʜᴀᴛ ᴜꜱᴇʀ ʙᴀʙʏ🥀.")


@run_async
@bot_admin
def runmute(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message

    if not args:
        message.reply_text("ʏᴏᴜ ᴅᴏɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ʙᴇ ʀᴇꜰᴇʀʀɪɴɢ ᴛᴏ ᴀ ᴄʜᴀᴛ/ᴜꜱᴇʀ ʙᴀʙʏ🥀.")
        return

    user_id, chat_id = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text(
            "ʏᴏᴜ ᴅᴏɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ʙᴇ ʀᴇꜰᴇʀʀɪɴɢ ᴛᴏ ᴀ ᴜꜱᴇʀ ᴏʀ ᴛʜᴇ ɪᴅ ꜱᴘᴇᴄɪꜰɪᴇᴅ ɪꜱ ɪɴᴄᴏʀʀᴇᴄᴛ ʙᴀʙʏ🥀.."
        )
        return
    elif not chat_id:
        message.reply_text("ʏᴏᴜ ᴅᴏɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ʙᴇ ʀᴇꜰᴇʀʀɪɴɢ ᴛᴏ ᴀ ᴄʜᴀᴛ ʙᴀʙʏ🥀.")
        return

    try:
        chat = bot.get_chat(chat_id.split()[0])
    except BadRequest as excp:
        if excp.message == "Chat not found":
            message.reply_text(
                "ᴄʜᴀᴛ ɴᴏᴛ ꜰᴏᴜɴᴅ! ᴍᴀᴋᴇ ꜱᴜʀᴇ ʏᴏᴜ ᴇɴᴛᴇʀᴇᴅ ᴀ ᴠᴀʟɪᴅ ᴄʜᴀᴛ ɪᴅ ᴀɴᴅ ɪ'ᴍ ᴘᴀʀᴛ ᴏꜰ ᴛʜᴀᴛ ᴄʜᴀᴛ ʙᴀʙʏ🥀."
            )
            return
        else:
            raise

    if chat.type == 'private':
        message.reply_text("ɪ'ᴍ ꜱᴏʀʀʏ, ʙᴜᴛ ᴛʜᴀᴛ'ꜱ ᴀ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ ʙᴀʙʏ🥀!")
        return

    if not is_bot_admin(chat, bot.id) or not chat.get_member(
            bot.id).can_restrict_members:
        message.reply_text(
            "ɪ ᴄᴀɴ'ᴛ ᴜɴʀᴇꜱᴛʀɪᴄᴛ ᴘᴇᴏᴘʟᴇ ᴛʜᴇʀᴇ! ᴍᴀᴋᴇ ꜱᴜʀᴇ ɪ'ᴍ ᴀᴅᴍɪɴ ᴀɴᴅ ᴄᴀɴ ᴜɴʙᴀɴ ᴜꜱᴇʀꜱ ʙᴀʙʏ🥀.",
        )
        return

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "User not found":
            message.reply_text("ɪ ᴄᴀɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ꜰɪɴᴅ ᴛʜɪꜱ ᴜꜱᴇʀ ʙᴀʙʏ🥀 there")
            return
        else:
            raise

    if is_user_in_chat(chat, user_id):
        if member.can_send_messages and member.can_send_media_messages \
           and member.can_send_other_messages and member.can_add_web_page_previews:
            message.reply_text(
                "ᴛʜɪꜱ ᴜꜱᴇʀ ᴀʟʀᴇᴀᴅʏ ʜᴀꜱ ᴛʜᴇ ʀɪɢʜᴛ ᴛᴏ ꜱᴘᴇᴀᴋ ɪɴ ᴛʜᴀᴛ ᴄʜᴀᴛ ʙᴀʙʏ🥀.")
            return

    if user_id == bot.id:
        message.reply_text("ɪ'ᴍ ɴᴏᴛ ɢᴏɴɴᴀ ᴜɴᴍᴜᴛᴇ ᴍʏꜱᴇʟꜰ, ɪ'ᴍ ᴀɴ ᴀᴅᴍɪɴ ᴛʜᴇʀᴇ ʙᴀʙʏ🥀!")
        return

    try:
        bot.restrict_chat_member(
            chat.id,
            int(user_id),
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True))
        message.reply_text("ʏᴇᴘ, ᴛʜɪꜱ ᴜꜱᴇʀ ᴄᴀɴ ᴛᴀʟᴋ ɪɴ ᴛʜᴀᴛ ᴄʜᴀᴛ ʙᴀʙʏ🥀!")
    except BadRequest as excp:
        if excp.message == "Reply message not found":
            # Do not reply
            message.reply_text('ᴜɴᴍᴜᴛᴇᴅ ʙᴀʙʏ🥀!', quote=False)
        elif excp.message in RUNMUTE_ERRORS:
            message.reply_text(excp.message)
        else:
            LOGGER.warning(update)
            LOGGER.exception(
                "ERROR unmnuting user %s in chat %s (%s) due to %s", user_id,
                chat.title, chat.id, excp.message)
            message.reply_text("ᴡᴇʟʟ ᴅᴀᴍɴ, ɪ ᴄᴀɴ'ᴛ ᴜɴᴍᴜᴛᴇ ᴛʜᴀᴛ ᴜꜱᴇʀ ʙᴀʙʏ🥀.")


RBAN_HANDLER = CommandHandler("rban", rban, filters=CustomFilters.sudo_filter)
RUNBAN_HANDLER = CommandHandler(
    "runban", runban, filters=CustomFilters.sudo_filter)
RKICK_HANDLER = CommandHandler(
    "rpunch", rkick, filters=CustomFilters.sudo_filter)
RMUTE_HANDLER = CommandHandler(
    "rmute", rmute, filters=CustomFilters.sudo_filter)
RUNMUTE_HANDLER = CommandHandler(
    "runmute", runmute, filters=CustomFilters.sudo_filter)

dispatcher.add_handler(RBAN_HANDLER)
dispatcher.add_handler(RUNBAN_HANDLER)
dispatcher.add_handler(RKICK_HANDLER)
dispatcher.add_handler(RMUTE_HANDLER)
dispatcher.add_handler(RUNMUTE_HANDLER)
