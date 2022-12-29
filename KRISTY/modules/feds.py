import ast
import csv
import json
import os
import re
import time
import uuid
from io import BytesIO

import KRISTY.modules.sql.feds_sql as sql
from KRISTY import (
    EVENT_LOGS,
    LOGGER,
    SUPPORT_CHAT,
    OWNER_ID,
    DRAGONS,
    TIGERS,
    WOLVES,
    dispatcher,
)
from KRISTY.modules.disable import DisableAbleCommandHandler
from KRISTY.modules.helper_funcs.alternate import send_message
from KRISTY.modules.helper_funcs.chat_status import is_user_admin
from KRISTY.modules.helper_funcs.extraction import (
    extract_unt_fedban,
    extract_user,
    extract_user_fban,
)
from KRISTY.modules.helper_funcs.string_handling import markdown_parser
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    MessageEntity,
    ParseMode,
    Update,
)
from telegram.error import BadRequest, TelegramError, Unauthorized
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    run_async,
)
from telegram.utils.helpers import mention_html, mention_markdown

# Hello bot owner, I spended for feds many hours of my life, Please don't remove this if you still respect MrYacha and peaktogoo and AyraHikari too
# Federation by MrYacha 2018-2019
# Federation rework by Mizukito Akito 2019
# Federation update v2 by Ayra Hikari 2019
# Time spended on feds = 10h by #MrYacha
# Time spended on reworking on the whole feds = 22+ hours by @peaktogoo
# Time spended on updating version to v2 = 26+ hours by @AyraHikari
# Total spended for making this features is 68+ hours
# LOGGER.info("Original federation module by MrYacha, reworked by Mizukito Akito (@peaktogoo) on Telegram.")

FBAN_ERRORS = {
    "User is an administrator of the chat",
    "Chat not found",
    "Not enough rights to restrict/unrestrict chat member",
    "User_not_participant",
    "Peer_id_invalid",
    "Group chat was deactivated",
    "Need to be inviter of a user to kick it from a basic group",
    "Chat_admin_required",
    "Only the creator of a basic group can kick group administrators",
    "Channel_private",
    "Not in the chat",
    "Have no rights to send a message",
}

UNFBAN_ERRORS = {
    "User is an administrator of the chat",
    "Chat not found",
    "Not enough rights to restrict/unrestrict chat member",
    "User_not_participant",
    "Method is available for supergroup and channel chats only",
    "Not in the chat",
    "Channel_private",
    "Chat_admin_required",
    "Have no rights to send a message",
}


def new_fed(update: Update, context: CallbackContext):
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message
    if chat.type != "private":
        update.effective_message.reply_text(
            "ꜰᴇᴅᴇʀᴀᴛɪᴏɴꜱ ᴄᴀɴ ᴏɴʟʏ ʙᴇ ᴄʀᴇᴀᴛᴇᴅ ʙʏ ᴘʀɪᴠᴀᴛᴇʟʏ ᴍᴇꜱꜱᴀɢɪɴɢ ᴍᴇ ʙᴀʙʏ🥀.",
        )
        return
    if len(message.text) == 1:
        send_message(
            update.effective_message,
            "ᴘʟᴇᴀꜱᴇ ᴡʀɪᴛᴇ ᴛʜᴇ ɴᴀᴍᴇ ᴏꜰ ᴛʜᴇ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ʙᴀʙʏ🥀!",
        )
        return
    fednam = message.text.split(None, 1)[1]
    if not fednam == "":
        fed_id = str(uuid.uuid4())
        fed_name = fednam
        LOGGER.info(fed_id)

        # Currently only for creator
        # if fednam == 'Team Nusantara Disciplinary Circle':
        # fed_id = "TeamNusantaraDevs"

        x = sql.new_fed(user.id, fed_name, fed_id)
        if not x:
            update.effective_message.reply_text(
                f"ᴄᴀɴ'ᴛ ꜰᴇᴅᴇʀᴀᴛᴇ! ᴘʟᴇᴀꜱᴇ ᴄᴏɴᴛᴀᴄᴛ @{SUPPORT_CHAT} ɪꜰ ᴛʜᴇ ᴘʀᴏʙʟᴇᴍ ᴘᴇʀꜱɪꜱᴛ ʙᴀʙʏ🥀.",
            )
            return

        update.effective_message.reply_text(
            "*ʏᴏᴜ ʜᴀᴠᴇ ꜱᴜᴄᴄᴇᴇᴅᴇᴅ ɪɴ ᴄʀᴇᴀᴛɪɴɢ ᴀ ɴᴇᴡ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ʙᴀʙʏ🥀!*"
            "\nɴᴀᴍᴇ: `{}`"
            "\nɪᴅ: `{}`"
            "\n\nᴜꜱᴇ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ ʙᴇʟᴏᴡ ᴛᴏ ᴊᴏɪɴ ᴛʜᴇ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ:"
            "\n`/joinfed {}`".format(fed_name, fed_id, fed_id),
            parse_mode=ParseMode.MARKDOWN,
        )
        try:
            bot.send_message(
                EVENT_LOGS,
                "ɴᴇᴡ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ: <b>{}</b>\nɪᴅ: <pre>{}</pre>".format(fed_name, fed_id),
                parse_mode=ParseMode.HTML,
            )
        except:
            LOGGER.warning("Cannot send a message to EVENT_LOGS")
    else:
        update.effective_message.reply_text(
            "ᴘʟᴇᴀꜱᴇ ᴡʀɪᴛᴇ ᴅᴏᴡɴ ᴛʜᴇ ɴᴀᴍᴇ ᴏꜰ ᴛʜᴇ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ʙᴀʙʏ🥀",
        )


def del_fed(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    chat = update.effective_chat
    user = update.effective_user
    if chat.type != "private":
        update.effective_message.reply_text(
            "ꜰᴇᴅᴇʀᴀᴛɪᴏɴꜱ ᴄᴀɴ ᴏɴʟʏ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ ʙʏ ᴘʀɪᴠᴀᴛᴇʟʏ ᴍᴇꜱꜱᴀɢɪɴɢ ᴍᴇ ʙᴀʙʏ🥀.",
        )
        return
    if args:
        is_fed_id = args[0]
        getinfo = sql.get_fed_info(is_fed_id)
        if getinfo is False:
            update.effective_message.reply_text("ᴛʜɪꜱ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴅᴏᴇꜱ ɴᴏᴛ ᴇxɪꜱᴛ ʙᴀʙʏ🥀.")
            return
        if int(getinfo["owner"]) == int(user.id) or int(user.id) == OWNER_ID:
            fed_id = is_fed_id
        else:
            update.effective_message.reply_text("ᴏɴʟʏ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴏᴡɴᴇʀꜱ ᴄᴀɴ ᴅᴏ ᴛʜɪꜱ ʙᴀʙʏ🥀!")
            return
    else:
        update.effective_message.reply_text("ᴡʜᴀᴛ ꜱʜᴏᴜʟᴅ ɪ ᴅᴇʟᴇᴛᴇ ʙᴀʙʏ🥀?")
        return

    if is_user_fed_owner(fed_id, user.id) is False:
        update.effective_message.reply_text("ᴏɴʟʏ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴏᴡɴᴇʀꜱ ᴄᴀɴ ᴅᴏ ᴛʜɪꜱ ʙᴀʙʏ🥀!")
        return

    update.effective_message.reply_text(
        "ʏᴏᴜ ꜱᴜʀᴇ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴇʟᴇᴛᴇ ʏᴏᴜʀ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ? ᴛʜɪꜱ ᴄᴀɴɴᴏᴛ ʙᴇ ʀᴇᴠᴇʀᴛᴇᴅ, ʏᴏᴜ ᴡɪʟʟ ʟᴏꜱᴇ ʏᴏᴜʀ ᴇɴᴛɪʀᴇ ʙᴀɴ ʟɪꜱᴛ, ᴀɴᴅ '{}' ᴡɪʟʟ ʙᴇ ᴘᴇʀᴍᴀɴᴇɴᴛʟʏ ʟᴏꜱᴛ ʙᴀʙʏ🥀.".format(
            getinfo["fname"],
        ),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="⚠️ Delete Federation ⚠️",
                        callback_data="rmfed_{}".format(fed_id),
                    ),
                ],
                [InlineKeyboardButton(text="Cancel", callback_data="rmfed_cancel")],
            ],
        ),
    )


def rename_fed(update, context):
    user = update.effective_user
    msg = update.effective_message
    args = msg.text.split(None, 2)

    if len(args) < 3:
        return msg.reply_text("ᴜꜱᴀɢᴇ: /renamefed <fed_id> <newname> ʙᴀʙʏ🥀")

    fed_id, newname = args[1], args[2]
    verify_fed = sql.get_fed_info(fed_id)

    if not verify_fed:
        return msg.reply_text("ᴛʜɪꜱ ꜰᴇᴅ ɴᴏᴛ ᴇxɪꜱᴛ ɪɴ ᴍʏ ᴅᴀᴛᴀʙᴀꜱᴇ ʙᴀʙʏ🥀!")

    if is_user_fed_owner(fed_id, user.id):
        sql.rename_fed(fed_id, user.id, newname)
        msg.reply_text(f"ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ʀᴇɴᴀᴍᴇᴅ ʏᴏᴜʀ ꜰᴇᴅ ɴᴀᴍᴇ ᴛᴏ {newname} ʙᴀʙʏ🥀!")
    else:
        msg.reply_text("ᴏɴʟʏ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴏᴡɴᴇʀ ᴄᴀɴ ᴅᴏ ᴛʜɪꜱ ʙᴀʙʏ🥀!")


def fed_chat(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    chat = update.effective_chat
    user = update.effective_user
    fed_id = sql.get_fed_id(chat.id)

    user_id = update.effective_message.from_user.id
    if not is_user_admin(update.effective_chat, user_id):
        update.effective_message.reply_text(
            "ʏᴏᴜ ᴍᴜꜱᴛ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ ᴛᴏ ᴇxᴇᴄᴜᴛᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ʙᴀʙʏ🥀",
        )
        return

    if not fed_id:
        update.effective_message.reply_text("ᴛʜɪꜱ ɢʀᴏᴜᴘ ɪꜱ ɴᴏᴛ ɪɴ ᴀɴʏ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ʙᴀʙʏ🥀!")
        return

    user = update.effective_user
    chat = update.effective_chat
    info = sql.get_fed_info(fed_id)

    text = "ᴛʜɪꜱ ɢʀᴏᴜᴘ ɪꜱ ᴘᴀʀᴛ ᴏꜰ ᴛʜᴇ ꜰᴏʟʟᴏᴡɪɴɢ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ:"
    text += "\n{} (ID: <code>{}</code>) ʙᴀʙʏ🥀".format(info["fname"], fed_id)

    update.effective_message.reply_text(text, parse_mode=ParseMode.HTML)


def join_fed(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    chat = update.effective_chat
    user = update.effective_user

    if chat.type == "private":
        send_message(
            update.effective_message,
            "ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪꜱ ꜱᴘᴇᴄɪꜰɪᴄ ᴛᴏ ᴛʜᴇ ɢʀᴏᴜᴘ, ɴᴏᴛ ᴛᴏ ᴏᴜʀ ᴘᴍ ʙᴀʙʏ🥀!",
        )
        return

    message = update.effective_message
    administrators = chat.get_administrators()
    fed_id = sql.get_fed_id(chat.id)

    if user.id in DRAGONS:
        pass
    else:
        for admin in administrators:
            status = admin.status
            if status == "creator":
                if str(admin.user.id) == str(user.id):
                    pass
                else:
                    update.effective_message.reply_text(
                        "ᴏɴʟʏ ɢʀᴏᴜᴘ ᴄʀᴇᴀᴛᴏʀꜱ ᴄᴀɴ ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ʙᴀʙʏ🥀!",
                    )
                    return
    if fed_id:
        message.reply_text("ᴏɴʟʏ ɢʀᴏᴜᴘ ᴄʀᴇᴀᴛᴏʀꜱ ᴄᴀɴ ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ʙᴀʙʏ🥀")
        return

    if len(args) >= 1:
        getfed = sql.search_fed_by_id(args[0])
        if getfed is False:
            message.reply_text("ᴘʟᴇᴀꜱᴇ ᴇɴᴛᴇʀ ᴀ ᴠᴀʟɪᴅ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ɪᴅ ʙᴀʙʏ🥀")
            return

        x = sql.chat_join_fed(args[0], chat.title, chat.id)
        if not x:
            message.reply_text(
                f"ꜰᴀɪʟᴇᴅ ᴛᴏ ᴊᴏɪɴ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ! ᴘʟᴇᴀꜱᴇ ᴄᴏɴᴛᴀᴄᴛᴅ @{SUPPORT_CHAT} ꜱʜᴏᴜʟᴅ ᴛʜɪꜱ ᴘʀᴏʙʟᴇᴍ ᴘᴇʀꜱɪꜱᴛ ʙᴀʙʏ🥀!",
            )
            return

        get_fedlog = sql.get_fed_log(args[0])
        if get_fedlog:
            if ast.literal_eval(get_fedlog):
                bot.send_message(
                    get_fedlog,
                    "ᴄʜᴀᴛ *{}* ʜᴀꜱ ᴊᴏɪɴᴇᴅ ᴛʜᴇ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ *{}* ʙᴀʙʏ🥀".format(
                        chat.title,
                        getfed["fname"],
                    ),
                    parse_mode="markdown",
                )

        message.reply_text(
            "ᴛʜɪꜱ ɢʀᴏᴜᴘ ʜᴀꜱ ᴊᴏɪɴᴇᴅ ᴛʜᴇ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ: {} ʙᴀʙʏ🥀!".format(getfed["fname"]),
        )


def leave_fed(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    chat = update.effective_chat
    user = update.effective_user

    if chat.type == "private":
        send_message(
            update.effective_message,
            "ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪꜱ ꜱᴘᴇᴄɪꜰɪᴄ ᴛᴏ ᴛʜᴇ ɢʀᴏᴜᴘ, ɴᴏᴛ ᴛᴏ ᴏᴜʀ ᴘᴍ ʙᴀʙʏ🥀!",
        )
        return

    fed_id = sql.get_fed_id(chat.id)
    fed_info = sql.get_fed_info(fed_id)

    # administrators = chat.get_administrators().status
    getuser = bot.get_chat_member(chat.id, user.id).status
    if getuser in "creator" or user.id in DRAGONS:
        if sql.chat_leave_fed(chat.id) is True:
            get_fedlog = sql.get_fed_log(fed_id)
            if get_fedlog:
                if ast.literal_eval(get_fedlog):
                    bot.send_message(
                        get_fedlog,
                        "ᴄʜᴀᴛ *{}* ʜᴀꜱ ʟᴇꜰᴛ ᴛʜᴇ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ *{}* ʙᴀʙʏ🥀".format(
                            chat.title,
                            fed_info["fname"],
                        ),
                        parse_mode="markdown",
                    )
            send_message(
                update.effective_message,
                "ᴛʜɪꜱ ɢʀᴏᴜᴘ ʜᴀꜱ ʟᴇꜰᴛ ᴛʜᴇ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ {} ʙᴀʙʏ🥀!".format(fed_info["fname"]),
            )
        else:
            update.effective_message.reply_text(
                "ʜᴏᴡ ᴄᴀɴ ʏᴏᴜ ʟᴇᴀᴠᴇ ᴀ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴛʜᴀᴛ ʏᴏᴜ ɴᴇᴠᴇʀ ᴊᴏɪɴᴇᴅ ʙᴀʙʏ🥀?!",
            )
    else:
        update.effective_message.reply_text("ᴏɴʟʏ ɢʀᴏᴜᴘ ᴄʀᴇᴀᴛᴏʀꜱ ᴄᴀɴ ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ʙᴀʙʏ🥀!")


def user_join_fed(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    chat = update.effective_chat
    user = update.effective_user
    msg = update.effective_message

    if chat.type == "private":
        send_message(
            update.effective_message,
            "ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪꜱ ꜱᴘᴇᴄɪꜰɪᴄ ᴛᴏ ᴛʜᴇ ɢʀᴏᴜᴘ, ɴᴏᴛ ᴛᴏ ᴏᴜʀ ᴘᴍ ʙᴀʙʏ🥀!",
        )
        return

    fed_id = sql.get_fed_id(chat.id)

    if is_user_fed_owner(fed_id, user.id) or user.id in DRAGONS:
        user_id = extract_user(msg, args)
        if user_id:
            user = bot.get_chat(user_id)
        elif not msg.reply_to_message and not args:
            user = msg.from_user
        elif not msg.reply_to_message and (
            not args
            or (
                len(args) >= 1
                and not args[0].startswith("@")
                and not args[0].isdigit()
                and not msg.parse_entities([MessageEntity.TEXT_MENTION])
            )
        ):
            msg.reply_text("ɪ ᴄᴀɴɴᴏᴛ ᴇxᴛʀᴀᴄᴛ ᴜꜱᴇʀ ꜰʀᴏᴍ ᴛʜɪꜱ ᴍᴇꜱꜱᴀɢᴇ ʙᴀʙʏ🥀")
            return
        else:
            LOGGER.warning("error")
        getuser = sql.search_user_in_fed(fed_id, user_id)
        fed_id = sql.get_fed_id(chat.id)
        info = sql.get_fed_info(fed_id)
        get_owner = ast.literal_eval(info["fusers"])["owner"]
        get_owner = bot.get_chat(get_owner).id
        if user_id == get_owner:
            update.effective_message.reply_text(
                "ʏᴏᴜ ᴅᴏ ᴋɴᴏᴡ ᴛʜᴀᴛ ᴛʜᴇ ᴜꜱᴇʀ ɪꜱ ᴛʜᴇ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴏᴡɴᴇʀ, ʀɪɢʜᴛ? ʀɪɢʜᴛ? ʙᴀʙʏ🥀",
            )
            return
        if getᴜꜱᴇʀ:
            update.effective_message.reply_text(
                "ɪ ᴄᴀɴɴᴏᴛ ᴘʀᴏᴍᴏᴛᴇ ᴜꜱᴇʀꜱ ᴡʜᴏ ᴀʀᴇ ᴀʟʀᴇᴀᴅʏ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴀᴅᴍɪɴꜱ! ᴄᴀɴ ʀᴇᴍᴏᴠᴇ ᴛʜᴇᴍ ɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ʙᴀʙʏ🥀!",
            )
            return
        if user_id == bot.id:
            update.effective_message.reply_text(
                "ɪ ᴀʟʀᴇᴀᴅʏ ᴀᴍ ᴀ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴀᴅᴍɪɴ ɪɴ ᴀʟʟ ꜰᴇᴅᴇʀᴀᴛɪᴏɴꜱ ʙᴀʙʏ🥀!",
            )
            return
        res = sql.user_join_fed(fed_id, user_id)
        if res:
            update.effective_message.reply_text("ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴘʀᴏᴍᴏᴛᴇᴅ ʙᴀʙʏ🥀!")
        else:
            update.effective_message.reply_text("ꜰᴀɪʟᴇᴅ ᴛᴏ ᴘʀᴏᴍᴏᴛᴇ ʙᴀʙʏ🥀!")
    else:
        update.effective_message.reply_text("ᴏɴʟʏ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴏᴡɴᴇʀꜱ ᴄᴀɴ ᴅᴏ ᴛʜɪꜱ ʙᴀʙʏ🥀!")


def user_demote_fed(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    chat = update.effective_chat
    user = update.effective_user

    if chat.type == "private":
        send_message(
            update.effective_message,
            "ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪꜱ ꜱᴘᴇᴄɪꜰɪᴄ ᴛᴏ ᴛʜᴇ ɢʀᴏᴜᴘ, ɴᴏᴛ ᴛᴏ ᴏᴜʀ ᴘᴍ ʙᴀʙʏ🥀!",
        )
        return

    fed_id = sql.get_fed_id(chat.id)

    if is_user_fed_owner(fed_id, user.id):
        msg = update.effective_message
        user_id = extract_user(msg, args)
        if user_id:
            user = bot.get_chat(user_id)

        elif not msg.reply_to_message and not args:
            user = msg.from_user

        elif not msg.reply_to_message and (
            not args
            or (
                len(args) >= 1
                and not args[0].startswith("@")
                and not args[0].isdigit()
                and not msg.parse_entities([MessageEntity.TEXT_MENTION])
            )
        ):
            msg.reply_text("ɪ ᴄᴀɴɴᴏᴛ ᴇxᴛʀᴀᴄᴛ ᴜꜱᴇʀ ꜰʀᴏᴍ ᴛʜɪꜱ ᴍᴇꜱꜱᴀɢᴇ ʙᴀʙʏ🥀")
            return
        else:
            LOGGER.warning("error")

        if user_id == bot.id:
            update.effective_message.reply_text(
                "ᴛʜᴇ ᴛʜɪɴɢ ʏᴏᴜ ᴀʀᴇ ᴛʀʏɪɴɢ ᴛᴏ ᴅᴇᴍᴏᴛᴇ ᴍᴇ ꜰʀᴏᴍ ᴡɪʟʟ ꜰᴀɪʟ ᴛᴏ ᴡᴏʀᴋ ᴡɪᴛʜᴏᴜᴛ ᴍᴇ! ᴊᴜꜱᴛ ꜱᴀʏɪɴɢ ʙᴀʙʏ🥀.",
            )
            return

        if sql.search_user_in_fed(fed_id, user_id) is False:
            update.effective_message.reply_text(
                "ɪ ᴄᴀɴɴᴏᴛ ᴅᴇᴍᴏᴛᴇ ᴘᴇᴏᴘʟᴇ ᴡʜᴏ ᴀʀᴇ ɴᴏᴛ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴀᴅᴍɪɴꜱ ʙᴀʙʏ🥀!",
            )
            return

        res = sql.user_demote_fed(fed_id, user_id)
        if res is True:
            update.effective_message.reply_text("ᴅᴇᴍᴏᴛᴇᴅ ꜰʀᴏᴍ ᴀ ꜰᴇᴅ ᴀᴅᴍɪɴ ʙᴀʙʏ🥀!")
        else:
            update.effective_message.reply_text("ᴅᴇᴍᴏᴛɪᴏɴ ꜰᴀɪʟᴇᴅ ʙᴀʙʏ🥀!")
    else:
        update.effective_message.reply_text("ᴏɴʟʏ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴏᴡɴᴇʀꜱ ᴄᴀɴ ᴅᴏ ᴛʜɪꜱ ʙᴀʙʏ🥀!")
        return


def fed_info(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    chat = update.effective_chat
    user = update.effective_user
    if args:
        fed_id = args[0]
        info = sql.get_fed_info(fed_id)
    else:
        if chat.type == "private":
            send_message(
                update.effective_message,
                "ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ᴘʀᴏᴠɪᴅᴇ ᴍᴇ ᴀ ꜰᴇᴅɪᴅ ᴛᴏ ᴄʜᴇᴄᴋ ꜰᴇᴅɪɴꜰᴏ ɪɴ ᴍʏ ᴘᴍ ʙᴀʙʏ🥀.",
            )
            return
        fed_id = sql.get_fed_id(chat.id)
        if not fed_id:
            send_message(
                update.effective_message,
                "ᴛʜɪꜱ ɢʀᴏᴜᴘ ɪꜱ ɴᴏᴛ ɪɴ ᴀɴʏ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ʙᴀʙʏ🥀!",
            )
            return
        info = sql.get_fed_info(fed_id)

    if is_user_fed_admin(fed_id, user.id) is False:
        update.effective_message.reply_text("ᴏɴʟʏ ᴀ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴀᴅᴍɪɴ ᴄᴀɴ ᴅᴏ ᴛʜɪꜱ ʙᴀʙʏ🥀!")
        return

    owner = bot.get_chat(info["owner"])
    try:
        owner_name = owner.first_name + " " + owner.last_name
    except:
        owner_name = owner.first_name
    FEDADMIN = sql.all_fed_users(fed_id)
    TotalAdminFed = len(FEDADMIN)

    user = update.effective_user
    chat = update.effective_chat
    info = sql.get_fed_info(fed_id)

    text = "<b>ℹ️ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ:</b>"
    text += "\nꜰᴇᴅɪᴅ: <code>{}</code>".format(fed_id)
    text += "\nɴᴀᴍᴇ: {}".format(info["fname"])
    text += "\nᴄʀᴇᴀᴛᴏʀ: {}".format(mention_html(owner.id, owner_name))
    text += "\nᴀʟʟ ᴀᴅᴍɪɴꜱ: <code>{}</code>".format(TotalAdminFed)
    getfban = sql.get_all_fban_users(fed_id)
    text += "\nᴛᴏᴛᴀʟ ʙᴀɴɴᴇᴅ ᴜꜱᴇʀꜱ: <code>{}</code>".format(len(getfban))
    getfchat = sql.all_fed_chats(fed_id)
    text += "\nɴᴜᴍʙᴇʀ ᴏꜰ ɢʀᴏᴜᴘꜱ ɪɴ ᴛʜɪꜱ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ: <code>{}</code>".format(
        len(getfchat),
    )

    update.effective_message.reply_text(text, parse_mode=ParseMode.HTML)


def fed_admin(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    chat = update.effective_chat
    user = update.effective_user

    if chat.type == "private":
        send_message(
            update.effective_message,
            "ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪꜱ ꜱᴘᴇᴄɪꜰɪᴄ ᴛᴏ ᴛʜᴇ ɢʀᴏᴜᴘ, ɴᴏᴛ ᴛᴏ ᴏᴜʀ ᴘᴍ ʙᴀʙʏ🥀!",
        )
        return

    fed_id = sql.get_fed_id(chat.id)

    if not fed_id:
        update.effective_message.reply_text("ᴛʜɪꜱ ɢʀᴏᴜᴘ ɪꜱ ɴᴏᴛ ɪɴ ᴀɴʏ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ʙᴀʙʏ🥀!")
        return

    if is_user_fed_admin(fed_id, user.id) is False:
        update.effective_message.reply_text("ᴏɴʟʏ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ᴅᴏ ᴛʜɪꜱ ʙᴀʙʏ🥀!")
        return

    user = update.effective_user
    chat = update.effective_chat
    info = sql.get_fed_info(fed_id)

    text = "<b>ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴀᴅᴍɪɴ {}:</b>\n\n".format(info["fname"])
    text += "👑 Owner:\n"
    owner = bot.get_chat(info["owner"])
    try:
        owner_name = owner.first_name + " " + owner.last_name
    except:
        owner_name = owner.first_name
    text += " • {}\n".format(mention_html(owner.id, owner_name))

    members = sql.all_fed_members(fed_id)
    if len(members) == 0:
        text += "\n🔱 ᴛʜᴇʀᴇ ᴀʀᴇ ɴᴏ ᴀᴅᴍɪɴꜱ ɪɴ ᴛʜɪꜱ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ʙᴀʙʏ🥀"
    else:
        text += "\n🔱 ᴀᴅᴍɪɴ:\n"
        for x in members:
            user = bot.get_chat(x)
            text += " • {}\n ".format(mention_html(user.id, user.first_name))

    update.effective_message.reply_text(text, parse_mode=ParseMode.HTML)


def fed_ban(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    chat = update.effective_chat
    user = update.effective_user

    if chat.type == "private":
        send_message(
            update.effective_message,
            "ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪꜱ ꜱᴘᴇᴄɪꜰɪᴄ ᴛᴏ ᴛʜᴇ ɢʀᴏᴜᴘ, ɴᴏᴛ ᴛᴏ ᴏᴜʀ ᴘᴍ ʙᴀʙʏ🥀!",
        )
        return

    fed_id = sql.get_fed_id(chat.id)

    if not fed_id:
        update.effective_message.reply_text(
            "ᴛʜɪꜱ ɢʀᴏᴜᴘ ɪꜱ ɴᴏᴛ ᴀ ᴘᴀʀᴛ ᴏꜰ ᴀɴʏ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ʙᴀʙʏ🥀!",
        )
        return

    info = sql.get_fed_info(fed_id)
    getfednotif = sql.user_feds_report(info["owner"])

    if is_user_fed_admin(fed_id, user.id) is False:
        update.effective_message.reply_text("ᴏɴʟʏ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ᴅᴏ ᴛʜɪꜱ ʙᴀʙʏ🥀!")
        return

    message = update.effective_message

    user_id, reason = extract_unt_fedban(message, args)

    fban, fbanreason, fbantime = sql.get_fban_user(fed_id, user_id)

    if not user_id:
        message.reply_text("ʏᴏᴜ ᴅᴏɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ʙᴇ ʀᴇꜰᴇʀʀɪɴɢ ᴛᴏ ᴀ ᴜꜱᴇʀ ʙᴀʙʏ🥀")
        return

    if user_id == bot.id:
        message.reply_text(
            "ᴡʜᴀᴛ ɪꜱ ꜰᴜɴɴɪᴇʀ ᴛʜᴀɴ ᴋɪᴄᴋɪɴɢ ᴛʜᴇ ɢʀᴏᴜᴘ ᴄʀᴇᴀᴛᴏʀ? ꜱᴇʟꜰ ꜱᴀᴄʀɪꜰɪᴄᴇ ʙᴀʙʏ🥀.",
        )
        return

    if is_user_fed_owner(fed_id, user_id) is True:
        message.reply_text("ᴡʜʏ ᴅɪᴅ ʏᴏᴜ ᴛʀʏ ᴛʜᴇ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ꜰʙᴀɴ ʙᴀʙʏ🥀?")
        return

    if is_user_fed_admin(fed_id, user_id) is True:
        message.reply_text("ʜᴇ ɪꜱ ᴀ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴀᴅᴍɪɴ, ɪ ᴄᴀɴ'ᴛ ꜰʙᴀɴ ʜɪᴍ ʙᴀʙʏ🥀.")
        return

    if user_id == OWNER_ID:
        message.reply_text("ᴅɪꜱᴀꜱᴛᴇʀ ʟᴇᴠᴇʟ ɢᴏᴅ ᴄᴀɴɴᴏᴛ ʙᴇ ꜰᴇᴅ ʙᴀɴɴᴇᴅ ʙᴀʙʏ🥀!")
        return

    if int(user_id) in DRAGONS:
        message.reply_text("ᴅʀᴀɢᴏɴꜱ ᴄᴀɴɴᴏᴛ ʙᴇ ꜰᴇᴅ ʙᴀɴɴᴇᴅ ʙᴀʙʏ🥀!")
        return

    if int(user_id) in TIGERS:
        message.reply_text("ᴛɪɢᴇʀꜱ ᴄᴀɴɴᴏᴛ ʙᴇ ꜰᴇᴅ ʙᴀɴɴᴇᴅ ʙᴀʙʏ🥀!")
        return

    if int(user_id) in WOLVES:
        message.reply_text("ᴡᴏʟᴠᴇꜱ ᴄᴀɴɴᴏᴛ ʙᴇ ꜰᴇᴅ ʙᴀɴɴᴇᴅ ʙᴀʙʏ🥀!")
        return

    if user_id in [777000, 1087968824]:
        message.reply_text("ꜰᴏᴏʟ! ʏᴏᴜ ᴄᴀɴ'ᴛ ᴀᴛᴛᴀᴄᴋ ᴛᴇʟᴇɢʀᴀᴍ'ꜱ ɴᴀᴛɪᴠᴇ ᴛᴇᴄʜ ʙᴀʙʏ🥀!")
        return

    try:
        user_chat = bot.get_chat(user_id)
        isvalid = True
        fban_user_id = user_chat.id
        fban_user_name = user_chat.first_name
        fban_user_lname = user_chat.last_name
        fban_user_uname = user_chat.username
    except BadRequest as excp:
        if not str(user_id).isdigit():
            send_message(update.effective_message, excp.message)
            return
        if len(str(user_id)) != 9:
            send_message(update.effective_message, "ᴛʜᴀᴛ'ꜱ ꜱᴏ ɴᴏᴛ ᴀ ᴜꜱᴇʀ ʙᴀʙʏ🥀!")
            return
        isvalid = False
        fban_user_id = int(user_id)
        fban_user_name = "user({})".format(user_id)
        fban_user_lname = None
        fban_user_uname = None

    if isvalid and user_chat.type != "private":
        send_message(update.effective_message, "ᴛʜᴀᴛ'ꜱ ꜱᴏ ɴᴏᴛ ᴀ ᴜꜱᴇʀ ʙᴀʙʏ🥀!")
        return

    if isvalid:
        user_target = mention_html(fban_user_id, fban_user_name)
    else:
        user_target = fban_user_name

    if fban:
        fed_name = info["fname"]
        # starting = "The reason fban is replaced for {} in the Federation <b>{}</b>.".format(user_target, fed_name)
        # send_message(update.effective_message, starting, parse_mode=ParseMode.HTML)

        # if reason == "":
        #    reason = "No reason given."

        temp = sql.un_fban_user(fed_id, fban_user_id)
        if not temp:
            message.reply_text("ꜰᴀɪʟᴇᴅ ᴛᴏ ᴜᴘᴅᴀᴛᴇ ᴛʜᴇ ʀᴇᴀꜱᴏɴ ꜰᴏʀ ꜰᴇᴅʙᴀɴ ʙᴀʙʏ🥀!")
            return
        x = sql.fban_user(
            fed_id,
            fban_user_id,
            fban_user_name,
            fban_user_lname,
            fban_user_uname,
            reason,
            int(time.time()),
        )
        if not x:
            message.reply_text(
                f"ꜰᴀɪʟᴇᴅ ᴛᴏ ʙᴀɴ ꜰʀᴏᴍ ᴛʜᴇ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ! ɪꜰ ᴛʜɪꜱ ᴘʀᴏʙʟᴇᴍ ᴄᴏɴᴛɪɴᴜᴇꜱ, ᴄᴏɴᴛᴀᴄᴛ @{SUPPORT_CHAT} ʙᴀʙʏ🥀.",
            )
            return

        fed_chats = sql.all_fed_chats(fed_id)
        # Will send to current chat
        bot.send_message(
            chat.id,
            "<b>ꜰᴇᴅʙᴀɴ ʀᴇᴀꜱᴏɴ ᴜᴘᴅᴀᴛᴇᴅ</b>"
            "\n<b>Federation:</b> {}"
            "\n<b>ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴀᴅᴍɪɴ:</b> {}"
            "\n<b>ᴜꜱᴇʀ:</b> {}"
            "\n<b>ᴜꜱᴇʀ ɪᴅ:</b> <code>{}</code>"
            "\n<b>ʀᴇᴀꜱᴏɴ:</b> {}".format(
                fed_name,
                mention_html(user.id, user.first_name),
                user_target,
                fban_user_id,
                reason,
            ),
            parse_mode="HTML",
        )
        # Send message to owner if fednotif is enabled
        if getfednotif:
            bot.send_message(
                info["owner"],
                "<b>ꜰᴇᴅʙᴀɴ ʀᴇᴀꜱᴏɴ ᴜᴘᴅᴀᴛᴇᴅ</b>"
                "\n<b>Federation:</b> {}"
                "\n<b>ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴀᴅᴍɪɴ:</b> {}"
                "\n<b>ᴜꜱᴇʀ:</b> {}"
                "\n<b>ᴜꜱᴇʀ ɪᴅ:</b> <code>{}</code>"
                "\n<b>ʀᴇᴀꜱᴏɴ:</b> {}".format(
                    fed_name,
                    mention_html(user.id, user.first_name),
                    user_target,
                    fban_user_id,
                    reason,
                ),
                parse_mode="HTML",
            )
        # If fedlog is set, then send message, except fedlog is current chat
        get_fedlog = sql.get_fed_log(fed_id)
        if get_fedlog:
            if int(get_fedlog) != int(chat.id):
                bot.send_message(
                    get_fedlog,
                    "<b>ꜰᴇᴅʙᴀɴ ʀᴇᴀꜱᴏɴ ᴜᴘᴅᴀᴛᴇᴅ</b>"
                    "\n<b>Federation:</b> {}"
                    "\n<b>ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴀᴅᴍɪɴ:</b> {}"
                    "\n<b>ᴜꜱᴇʀ:</b> {}"
                    "\n<b>ᴜꜱᴇʀ ɪᴅ:</b> <code>{}</code>"
                    "\n<b>ʀᴇᴀꜱᴏɴ:</b> {}".format(
                        fed_name,
                        mention_html(user.id, user.first_name),
                        user_target,
                        fban_user_id,
                        reason,
                    ),
                    parse_mode="HTML",
                )
        for fedschat in fed_chats:
            try:
                # Do not spam all fed chats
                """
				bot.send_message(chat, "<b>ꜰᴇᴅʙᴀɴ ʀᴇᴀꜱᴏɴ ᴜᴘᴅᴀᴛᴇᴅ</b>" \
							 "\n<b>Federation:</b> {}" \
							 "\n<b>ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴀᴅᴍɪɴ:</b> {}" \
							 "\n<b>ᴜꜱᴇʀ:</b> {}" \
							 "\n<b>ᴜꜱᴇʀ ɪᴅ:</b> <code>{}</code>" \
							 "\n<b>ʀᴇᴀꜱᴏɴ:</b> {}".format(fed_name, mention_html(user.id, user.first_name), user_target, fban_user_id, reason), parse_mode="HTML")
				"""
                bot.kick_chat_member(fedschat, fban_user_id)
            except BadRequest as excp:
                if excp.message in FBAN_ERRORS:
                    try:
                        dispatcher.bot.getChat(fedschat)
                    except Unauthorized:
                        sql.chat_leave_fed(fedschat)
                        LOGGER.info(
                            "ᴄʜᴀᴛ {} ʜᴀꜱ ʟᴇᴀᴠᴇ ꜰᴇᴅ {} ʙᴇᴄᴀᴜꜱᴇ ɪ ᴡᴀꜱ ᴋɪᴄᴋᴇᴅ ʙᴀʙʏ🥀".format(
                                fedschat,
                                info["fname"],
                            ),
                        )
                        continue
                elif excp.message == "User_id_invalid":
                    break
                else:
                    LOGGER.warning(
                        "ᴄᴏᴜʟᴅ ɴᴏᴛ ꜰʙᴀɴ ᴏɴ {} ʙᴇᴄᴀᴜꜱᴇ: {} ʙᴀʙʏ🥀".format(chat, excp.message),
                    )
            except TelegramError:
                pass
        # Also do not spam all fed admins
        """
		send_to_list(bot, FEDADMIN,
				 "<b>ꜰᴇᴅʙᴀɴ ʀᴇᴀꜱᴏɴ ᴜᴘᴅᴀᴛᴇᴅ</b>" \
							 "\n<b>Federation:</b> {}" \
							 "\n<b>ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴀᴅᴍɪɴ:</b> {}" \
							 "\n<b>ᴜꜱᴇʀ:</b> {}" \
							 "\n<b>ᴜꜱᴇʀ ɪᴅ:</b> <code>{}</code>" \
							 "\n<b>ʀᴇᴀꜱᴏɴ:</b> {}".format(fed_name, mention_html(user.id, user.first_name), user_target, fban_user_id, reason),
							html=True)
		"""

        # Fban for fed subscriber
        subscriber = list(sql.get_subscriber(fed_id))
        if len(subscriber) != 0:
            for fedsid in subscriber:
                all_fedschat = sql.all_fed_chats(fedsid)
                for fedschat in all_fedschat:
                    try:
                        bot.kick_chat_member(fedschat, fban_user_id)
                    except BadRequest as excp:
                        if excp.message in FBAN_ERRORS:
                            try:
                                dispatcher.bot.getChat(fedschat)
                            except Unauthorized:
                                targetfed_id = sql.get_fed_id(fedschat)
                                sql.unsubs_fed(fed_id, targetfed_id)
                                LOGGER.info(
                                    "ᴄʜᴀᴛ {} ʜᴀꜱ ᴜɴꜱᴜʙ ꜰᴇᴅ {} ʙᴇᴄᴀᴜꜱᴇ ɪ ᴡᴀꜱ ᴋɪᴄᴋᴇᴅ ʙᴀʙʏ🥀".format(
                                        fedschat,
                                        info["fname"],
                                    ),
                                )
                                continue
                        elif excp.message == "User_id_invalid":
                            break
                        else:
                            LOGGER.warning(
                                "ᴜɴᴀʙʟᴇ ᴛᴏ ꜰʙᴀɴ ᴏɴ {} ʙᴇᴄᴀᴜꜱᴇ: {} ʙᴀʙʏ🥀".format(
                                    fedschat,
                                    excp.message,
                                ),
                            )
                    except TelegramError:
                        pass
        # send_message(update.effective_message, "Fedban Reason has been updated.")
        return

    fed_name = info["fname"]

    # starting = "Starting a federation ban for {} in the Federation <b>{}</b>.".format(
    #    user_target, fed_name)
    # update.effective_message.reply_text(starting, parse_mode=ParseMode.HTML)

    # if reason == "":
    #    reason = "No reason given."

    x = sql.fban_user(
        fed_id,
        fban_user_id,
        fban_user_name,
        fban_user_lname,
        fban_user_uname,
        reason,
        int(time.time()),
    )
    if not x:
        message.reply_text(
            f"ꜰᴀɪʟᴇᴅ ᴛᴏ ʙᴀɴ ꜰʀᴏᴍ ᴛʜᴇ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ! ɪꜰ ᴛʜɪꜱ ᴘʀᴏʙʟᴇᴍ ᴄᴏɴᴛɪɴᴜᴇꜱ, ᴄᴏɴᴛᴀᴄᴛ @{SUPPORT_CHAT} ʙᴀʙʏ🥀.",
        )
        return

    fed_chats = sql.all_fed_chats(fed_id)
    # Will send to current chat
    bot.send_message(
        chat.id,
        "<b>New FedBan</b>"
        "\n<b>Federation:</b> {}"
        "\n<b>ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴀᴅᴍɪɴ:</b> {}"
        "\n<b>ᴜꜱᴇʀ:</b> {}"
        "\n<b>ᴜꜱᴇʀ ɪᴅ:</b> <code>{}</code>"
        "\n<b>ʀᴇᴀꜱᴏɴ:</b> {}".format(
            fed_name,
            mention_html(user.id, user.first_name),
            user_target,
            fban_user_id,
            reason,
        ),
        parse_mode="HTML",
    )
    # Send message to owner if fednotif is enabled
    if getfednotif:
        bot.send_message(
            info["owner"],
            "<b>New FedBan</b>"
            "\n<b>Federation:</b> {}"
            "\n<b>ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴀᴅᴍɪɴ:</b> {}"
            "\n<b>ᴜꜱᴇʀ:</b> {}"
            "\n<b>ᴜꜱᴇʀ ɪᴅ:</b> <code>{}</code>"
            "\n<b>ʀᴇᴀꜱᴏɴ:</b> {}".format(
                fed_name,
                mention_html(user.id, user.first_name),
                user_target,
                fban_user_id,
                reason,
            ),
            parse_mode="HTML",
        )
    # If fedlog is set, then send message, except fedlog is current chat
    get_fedlog = sql.get_fed_log(fed_id)
    if get_fedlog:
        if int(get_fedlog) != int(chat.id):
            bot.send_message(
                get_fedlog,
                "<b>New FedBan</b>"
                "\n<b>Federation:</b> {}"
                "\n<b>ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴀᴅᴍɪɴ:</b> {}"
                "\n<b>ᴜꜱᴇʀ:</b> {}"
                "\n<b>ᴜꜱᴇʀ ɪᴅ:</b> <code>{}</code>"
                "\n<b>ʀᴇᴀꜱᴏɴ:</b> {}".format(
                    fed_name,
                    mention_html(user.id, user.first_name),
                    user_target,
                    fban_user_id,
                    reason,
                ),
                parse_mode="HTML",
            )
    chats_in_fed = 0
    for fedschat in fed_chats:
        chats_in_fed += 1
        try:
            # Do not spamming all fed chats
            """
			bot.send_message(chat, "<b>ꜰᴇᴅʙᴀɴ ʀᴇᴀꜱᴏɴ ᴜᴘᴅᴀᴛᴇᴅ</b>" \
							"\n<b>Federation:</b> {}" \
							"\n<b>ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴀᴅᴍɪɴ:</b> {}" \
							"\n<b>ᴜꜱᴇʀ:</b> {}" \
							"\n<b>ᴜꜱᴇʀ ɪᴅ:</b> <code>{}</code>" \
							"\n<b>ʀᴇᴀꜱᴏɴ:</b> {}".format(fed_name, mention_html(user.id, user.first_name), user_target, fban_user_id, reason), parse_mode="HTML")
			"""
            bot.kick_chat_member(fedschat, fban_user_id)
        except BadRequest as excp:
            if excp.message in FBAN_ERRORS:
                pass
            elif excp.message == "User_id_invalid":
                break
            else:
                LOGGER.warning(
                    "ᴄᴏᴜʟᴅ ɴᴏᴛ ꜰʙᴀɴ ᴏɴ {} ʙᴇᴄᴀᴜꜱᴇ: {} ʙᴀʙʏ🥀".format(chat, excp.message),
                )
        except TelegramError:
            pass

        # Also do not spamming all fed admins
        """
		send_to_list(bot, FEDADMIN,
				 "<b>ꜰᴇᴅʙᴀɴ ʀᴇᴀꜱᴏɴ ᴜᴘᴅᴀᴛᴇᴅ</b>" \
							 "\n<b>Federation:</b> {}" \
							 "\n<b>ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴀᴅᴍɪɴ:</b> {}" \
							 "\n<b>ᴜꜱᴇʀ:</b> {}" \
							 "\n<b>ᴜꜱᴇʀ ɪᴅ:</b> <code>{}</code>" \
							 "\n<b>ʀᴇᴀꜱᴏɴ:</b> {}".format(fed_name, mention_html(user.id, user.first_name), user_target, fban_user_id, reason),
							html=True)
		"""

        # Fban for fed subscriber
        subscriber = list(sql.get_subscriber(fed_id))
        if len(subscriber) != 0:
            for fedsid in subscriber:
                all_fedschat = sql.all_fed_chats(fedsid)
                for fedschat in all_fedschat:
                    try:
                        bot.kick_chat_member(fedschat, fban_user_id)
                    except BadRequest as excp:
                        if excp.message in FBAN_ERRORS:
                            try:
                                dispatcher.bot.getChat(fedschat)
                            except Unauthorized:
                                targetfed_id = sql.get_fed_id(fedschat)
                                sql.unsubs_fed(fed_id, targetfed_id)
                                LOGGER.info(
                                    "ᴄʜᴀᴛ {} ʜᴀꜱ ᴜɴꜱᴜʙ ꜰᴇᴅ {} ʙᴇᴄᴀᴜꜱᴇ ɪ ᴡᴀꜱ ᴋɪᴄᴋᴇᴅ ʙᴀʙʏ🥀".format(
                                        fedschat,
                                        info["fname"],
                                    ),
                                )
                                continue
                        elif excp.message == "User_id_invalid":
                            break
                        else:
                            LOGGER.warning(
                                "ᴜɴᴀʙʟᴇ ᴛᴏ ꜰʙᴀɴ ᴏɴ {} ʙᴇᴄᴀᴜꜱᴇ: {} ʙᴀʙʏ🥀".format(
                                    fedschat,
                                    excp.message,
                                ),
                            )
                    except TelegramError:
                        pass
    # if chats_in_fed == 0:
    #    send_message(update.effective_message, "Fedban affected 0 chats. ")
    # elif chats_in_fed > 0:
    #    send_message(update.effective_message,
    #                 "Fedban affected {} chats. ".format(chats_in_fed))


def unfban(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message

    if chat.type == "private":
        send_message(
            update.effective_message,
            "ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪꜱ ꜱᴘᴇᴄɪꜰɪᴄ ᴛᴏ ᴛʜᴇ ɢʀᴏᴜᴘ, ɴᴏᴛ ᴛᴏ ᴏᴜʀ ᴘᴍ ʙᴀʙʏ🥀!",
        )
        return

    fed_id = sql.get_fed_id(chat.id)

    if not fed_id:
        update.effective_message.reply_text(
            "ᴛʜɪꜱ ɢʀᴏᴜᴘ ɪꜱ ɴᴏᴛ ᴀ ᴘᴀʀᴛ ᴏꜰ ᴀɴʏ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ʙᴀʙʏ🥀!",
        )
        return

    info = sql.get_fed_info(fed_id)
    getfednotif = sql.user_feds_report(info["owner"])

    if is_user_fed_admin(fed_id, user.id) is False:
        update.effective_message.reply_text("ᴏɴʟʏ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ᴅᴏ ᴛʜɪꜱ ʙᴀʙʏ🥀!")
        return

    user_id = extract_user_fban(message, args)
    if not user_id:
        message.reply_text("ʏᴏᴜ ᴅᴏ ɴᴏᴛ ꜱᴇᴇᴍ ᴛᴏ ʙᴇ ʀᴇꜰᴇʀʀɪɴɢ ᴛᴏ ᴀ ᴜꜱᴇʀ ʙᴀʙʏ🥀.")
        return

    try:
        user_chat = bot.get_chat(user_id)
        isvalid = True
        fban_user_id = user_chat.id
        fban_user_name = user_chat.first_name
        fban_user_lname = user_chat.last_name
        fban_user_uname = user_chat.username
    except BadRequest as excp:
        if not str(user_id).isdigit():
            send_message(update.effective_message, excp.message)
            return
        if len(str(user_id)) != 9:
            send_message(update.effective_message, "ᴛʜᴀᴛ'ꜱ ꜱᴏ ɴᴏᴛ ᴀ ᴜꜱᴇʀ ʙᴀʙʏ🥀!")
            return
        isvalid = False
        fban_user_id = int(user_id)
        fban_user_name = "user({})".format(user_id)
        fban_user_lname = None
        fban_user_uname = None

    if isvalid and user_chat.type != "private":
        message.reply_text("ᴛʜᴀᴛ'ꜱ ꜱᴏ ɴᴏᴛ ᴀ ᴜꜱᴇʀ ʙᴀʙʏ🥀!")
        return

    if isvalid:
        user_target = mention_html(fban_user_id, fban_user_name)
    else:
        user_target = fban_user_name

    fban, fbanreason, fbantime = sql.get_fban_user(fed_id, fban_user_id)
    if fban is False:
        message.reply_text("ᴛʜɪꜱ ᴜꜱᴇʀ ɪꜱ ɴᴏᴛ ꜰʙᴀɴɴᴇᴅ ʙᴀʙʏ🥀!")
        return

    banner = update.effective_user

    # message.reply_text("I'll give {} another chance in this federation".format(user_chat.first_name))

    chat_list = sql.all_fed_chats(fed_id)
    # Will send to current chat
    bot.send_message(
        chat.id,
        "<b>ᴜɴ-FedBan</b>"
        "\n<b>Federation:</b> {}"
        "\n<b>ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴀᴅᴍɪɴ:</b> {}"
        "\n<b>ᴜꜱᴇʀ:</b> {}"
        "\n<b>ᴜꜱᴇʀ ɪᴅ:</b> <code>{}</code>".format(
            info["fname"],
            mention_html(user.id, user.first_name),
            user_target,
            fban_user_id,
        ),
        parse_mode="HTML",
    )
    # Send message to owner if fednotif is enabled
    if getfednotif:
        bot.send_message(
            info["owner"],
            "<b>ᴜɴ-FedBan</b>"
            "\n<b>Federation:</b> {}"
            "\n<b>ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴀᴅᴍɪɴ:</b> {}"
            "\n<b>ᴜꜱᴇʀ:</b> {}"
            "\n<b>ᴜꜱᴇʀ ɪᴅ:</b> <code>{}</code>".format(
                info["fname"],
                mention_html(user.id, user.first_name),
                user_target,
                fban_user_id,
            ),
            parse_mode="HTML",
        )
    # If fedlog is set, then send message, except fedlog is current chat
    get_fedlog = sql.get_fed_log(fed_id)
    if get_fedlog:
        if int(get_fedlog) != int(chat.id):
            bot.send_message(
                get_fedlog,
                "<b>ᴜɴ-FedBan</b>"
                "\n<b>Federation:</b> {}"
                "\n<b>ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴀᴅᴍɪɴ:</b> {}"
                "\n<b>ᴜꜱᴇʀ:</b> {}"
                "\n<b>ᴜꜱᴇʀ ɪᴅ:</b> <code>{}</code>".format(
                    info["fname"],
                    mention_html(user.id, user.first_name),
                    user_target,
                    fban_user_id,
                ),
                parse_mode="HTML",
            )
    unfbanned_in_chats = 0
    for fedchats in chat_list:
        unfbanned_in_chats += 1
        try:
            member = bot.get_chat_member(fedchats, user_id)
            if member.status == "kicked":
                bot.unban_chat_member(fedchats, user_id)
            # Do not spamming all fed chats
            """
			bot.send_message(chat, "<b>ᴜɴ-FedBan</b>" \
						 "\n<b>Federation:</b> {}" \
						 "\n<b>ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴀᴅᴍɪɴ:</b> {}" \
						 "\n<b>ᴜꜱᴇʀ:</b> {}" \
						 "\n<b>ᴜꜱᴇʀ ɪᴅ:</b> <code>{}</code>".format(info['fname'], mention_html(user.id, user.first_name), user_target, fban_user_id), parse_mode="HTML")
			"""
        except BadRequest as excp:
            if excp.message in UNFBAN_ERRORS:
                pass
            elif excp.message == "User_id_invalid":
                break
            else:
                LOGGER.warning(
                    "ᴄᴏᴜʟᴅ ɴᴏᴛ ꜰʙᴀɴ ᴏɴ {} ʙᴇᴄᴀᴜꜱᴇ: {} ʙᴀʙʏ🥀".format(chat, excp.message),
                )
        except TelegramError:
            pass

    try:
        x = sql.un_fban_user(fed_id, user_id)
        if not x:
            send_message(
                update.effective_message,
                "UN-ꜰʙᴀɴ ꜰᴀɪʟᴇᴅ, ᴛʜɪꜱ ᴜꜱᴇʀ ᴍᴀʏ ᴀʟʀᴇᴀᴅʏ ʙᴇ ᴜɴ-ꜰᴇᴅʙᴀɴɴᴇᴅ ʙᴀʙʏ🥀!",
            )
            return
    except:
        pass

    # UnFban for fed subscriber
    subscriber = list(sql.get_subscriber(fed_id))
    if len(subscriber) != 0:
        for fedsid in subscriber:
            all_fedschat = sql.all_fed_chats(fedsid)
            for fedschat in all_fedschat:
                try:
                    bot.unban_chat_member(fedchats, user_id)
                except BadRequest as excp:
                    if excp.message in FBAN_ERRORS:
                        try:
                            dispatcher.bot.getChat(fedschat)
                        except Unauthorized:
                            targetfed_id = sql.get_fed_id(fedschat)
                            sql.unsubs_fed(fed_id, targetfed_id)
                            LOGGER.info(
                                "ᴄʜᴀᴛ {} ʜᴀꜱ ᴜɴꜱᴜʙ ꜰᴇᴅ {} ʙᴇᴄᴀᴜꜱᴇ ɪ ᴡᴀꜱ ᴋɪᴄᴋᴇᴅ ʙᴀʙʏ🥀".format(
                                    fedschat,
                                    info["fname"],
                                ),
                            )
                            continue
                    elif excp.message == "User_id_invalid":
                        break
                    else:
                        LOGGER.warning(
                            "ᴜɴᴀʙʟᴇ ᴛᴏ ꜰʙᴀɴ ᴏɴ {} ʙᴇᴄᴀᴜꜱᴇ: {} ʙᴀʙʏ🥀".format(
                                fedschat,
                                excp.message,
                            ),
                        )
                except TelegramError:
                    pass

    if unfbanned_in_chats == 0:
        send_message(
            update.effective_message,
            "ᴛʜɪꜱ ᴘᴇʀꜱᴏɴ ʜᴀꜱ ʙᴇᴇɴ ᴜɴ-ꜰʙᴀɴɴᴇᴅ ɪɴ 0 ᴄʜᴀᴛꜱ ʙᴀʙʏ🥀.",
        )
    if unfbanned_in_chats > 0:
        send_message(
            update.effective_message,
            "ᴛʜɪꜱ ᴘᴇʀꜱᴏɴ ʜᴀꜱ ʙᴇᴇɴ ᴜɴ-ꜰʙᴀɴɴᴇᴅ ɪɴ {} ᴄʜᴀᴛꜱ ʙᴀʙʏ🥀.".format(unfbanned_in_chats),
        )
    # Also do not spamming all fed admins
    """
	FEDADMIN = sql.all_fed_users(fed_id)
	for x in FEDᴀᴅᴍɪɴ:
		getreport = sql.user_feds_report(x)
		if getreport is False:
			FEDADMIN.remove(x)
	send_to_list(bot, FEDADMIN,
			 "<b>ᴜɴ-FedBan</b>" \
			 "\n<b>Federation:</b> {}" \
			 "\n<b>ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴀᴅᴍɪɴ:</b> {}" \
			 "\n<b>ᴜꜱᴇʀ:</b> {}" \
			 "\n<b>ᴜꜱᴇʀ ɪᴅ:</b> <code>{}</code>".format(info['fname'], mention_html(user.id, user.first_name),
												 mention_html(user_chat.id, user_chat.first_name),
															  user_chat.id),
			html=True)
	"""


def set_frules(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    chat = update.effective_chat
    user = update.effective_user

    if chat.type == "private":
        send_message(
            update.effective_message,
            "ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪꜱ ꜱᴘᴇᴄɪꜰɪᴄ ᴛᴏ ᴛʜᴇ ɢʀᴏᴜᴘ, ɴᴏᴛ ᴛᴏ ᴏᴜʀ ᴘᴍ ʙᴀʙʏ🥀!",
        )
        return

    fed_id = sql.get_fed_id(chat.id)

    if not fed_id:
        update.effective_message.reply_text("ᴛʜɪꜱ ɢʀᴏᴜᴘ ɪꜱ ɴᴏᴛ ɪɴ ᴀɴʏ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ʙᴀʙʏ🥀!")
        return

    if is_user_fed_admin(fed_id, user.id) is False:
        update.effective_message.reply_text("ᴏɴʟʏ ꜰᴇᴅ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ᴅᴏ ᴛʜɪꜱ ʙᴀʙʏ🥀!")
        return

    if len(args) >= 1:
        msg = update.effective_message
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
        x = sql.set_frules(fed_id, markdown_rules)
        if not x:
            update.effective_message.reply_text(
                f"ᴡʜᴏᴀ! ᴛʜᴇʀᴇ ᴡᴀꜱ ᴀɴ ᴇʀʀᴏʀ ᴡʜɪʟᴇ ꜱᴇᴛᴛɪɴɢ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ʀᴜʟᴇꜱ! ɪꜰ ʏᴏᴜ ᴡᴏɴᴅᴇʀᴇᴅ ᴡʜʏ ᴘʟᴇᴀꜱᴇ ᴀꜱᴋ ɪᴛ ɪɴ @{SUPPORT_CHAT} ʙᴀʙʏ🥀!",
            )
            return

        rules = sql.get_fed_info(fed_id)["frules"]
        getfed = sql.get_fed_info(fed_id)
        get_fedlog = sql.get_fed_log(fed_id)
        if get_fedlog:
            if ast.literal_eval(get_fedlog):
                bot.send_message(
                    get_fedlog,
                    "*{}* ʜᴀꜱ ᴜᴘᴅᴀᴛᴇᴅ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ʀᴜʟᴇꜱ ꜰᴏʀ ꜰᴇᴅ *{}* ʙᴀʙʏ🥀".format(
                        user.first_name,
                        getfed["fname"],
                    ),
                    parse_mode="markdown",
                )
        update.effective_message.reply_text(f"ʀᴜʟᴇꜱ ʜᴀᴠᴇ ʙᴇᴇɴ ᴄʜᴀɴɢᴇᴅ ᴛᴏ :\n{rules} ʙᴀʙʏ🥀!")
    else:
        update.effective_message.reply_text("ᴘʟᴇᴀꜱᴇ ᴡʀɪᴛᴇ ʀᴜʟᴇꜱ ᴛᴏ ꜱᴇᴛ ᴛʜɪꜱ ᴜᴘ ʙᴀʙʏ🥀!")


def get_frules(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    chat = update.effective_chat

    if chat.type == "private":
        send_message(
            update.effective_message,
            "ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪꜱ ꜱᴘᴇᴄɪꜰɪᴄ ᴛᴏ ᴛʜᴇ ɢʀᴏᴜᴘ, ɴᴏᴛ ᴛᴏ ᴏᴜʀ ᴘᴍ ʙᴀʙʏ🥀!",
        )
        return

    fed_id = sql.get_fed_id(chat.id)
    if not fed_id:
        update.effective_message.reply_text("ᴛʜɪꜱ ɢʀᴏᴜᴘ ɪꜱ ɴᴏᴛ ɪɴ ᴀɴʏ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ʙᴀʙʏ🥀!")
        return

    rules = sql.get_frules(fed_id)
    text = "*ʀᴜʟᴇꜱ ɪɴ ᴛʜɪꜱ ꜰᴇᴅ:*\n"
    text += rules
    update.effective_message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


def fed_broadcast(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    msg = update.effective_message
    user = update.effective_user
    chat = update.effective_chat

    if chat.type == "private":
        send_message(
            update.effective_message,
            "ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪꜱ ꜱᴘᴇᴄɪꜰɪᴄ ᴛᴏ ᴛʜᴇ ɢʀᴏᴜᴘ, ɴᴏᴛ ᴛᴏ ᴏᴜʀ ᴘᴍ ʙᴀʙʏ🥀!",
        )
        return

    if args:
        chat = update.effective_chat
        fed_id = sql.get_fed_id(chat.id)
        fedinfo = sql.get_fed_info(fed_id)
        if is_user_fed_owner(fed_id, user.id) is False:
            update.effective_message.reply_text("ᴏɴʟʏ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴏᴡɴᴇʀꜱ ᴄᴀɴ ᴅᴏ ᴛʜɪꜱ ʙᴀʙʏ🥀!")
            return
        # Parsing md
        raw_text = msg.text
        args = raw_text.split(None, 1)  # use python's maxsplit to separate cmd and args
        txt = args[1]
        offset = len(txt) - len(raw_text)  # set correct offset relative to command
        text_parser = markdown_parser(txt, entities=msg.parse_entities(), offset=offset)
        text = text_parser
        try:
            broadcaster = user.first_name
        except:
            broadcaster = user.first_name + " " + user.last_name
        text += "\n\n- {}".format(mention_markdown(user.id, broadcaster))
        chat_list = sql.all_fed_chats(fed_id)
        failed = 0
        for chat in chat_list:
            title = "*New broadcast fɴᴇᴡ ʙʀᴏᴀᴅᴄᴀꜱᴛ ꜰʀᴏᴍ ꜰᴇᴅrom Fed {} ʙᴀʙʏ🥀*\n".format(fedinfo["fname"])
            try:
                bot.sendMessage(chat, title + text, parse_mode="markdown")
            except TelegramError:
                try:
                    dispatcher.bot.getChat(chat)
                except Unauthorized:
                    failed += 1
                    sql.chat_leave_fed(chat)
                    LOGGER.info(
                        "ᴄʜᴀᴛ {} ʜᴀꜱ ʟᴇꜰᴛ ꜰᴇᴅ {} ʙᴇᴄᴀᴜꜱᴇ ɪ ᴡᴀꜱ ᴘᴜɴᴄʜᴇᴅ ʙᴀʙʏ🥀".format(
                            chat,
                            fedinfo["fname"],
                        ),
                    )
                    continue
                failed += 1
                LOGGER.warning("ᴄᴏᴜʟᴅɴ'ᴛ ꜱᴇɴᴅ ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴛᴏ {} ʙᴀʙʏ🥀".format(str(chat)))

        send_text = "ᴛʜᴇ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ʙʀᴏᴀᴅᴄᴀꜱᴛ ɪꜱ ᴄᴏᴍᴘʟᴇᴛᴇ ʙᴀʙʏ🥀"
        if failed >= 1:
            send_text += "{} ᴛʜᴇ ɢʀᴏᴜᴘ ꜰᴀɪʟᴇᴅ ᴛᴏ ʀᴇᴄᴇɪᴠᴇ ᴛʜᴇ ᴍᴇꜱꜱᴀɢᴇ, ᴘʀᴏʙᴀʙʟʏ ʙᴇᴄᴀᴜꜱᴇ ɪᴛ ʟᴇꜰᴛ ᴛʜᴇ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ʙᴀʙʏ🥀.".format(
                failed,
            )
        update.effective_message.reply_text(send_text)


def fed_ban_list(update: Update, context: CallbackContext):
    bot, args, chat_data = context.bot, context.args, context.chat_data
    chat = update.effective_chat
    user = update.effective_user

    if chat.type == "private":
        send_message(
            update.effective_message,
            "ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪꜱ ꜱᴘᴇᴄɪꜰɪᴄ ᴛᴏ ᴛʜᴇ ɢʀᴏᴜᴘ, ɴᴏᴛ ᴛᴏ ᴏᴜʀ ᴘᴍ ʙᴀʙʏ🥀!",
        )
        return

    fed_id = sql.get_fed_id(chat.id)
    info = sql.get_fed_info(fed_id)

    if not fed_id:
        update.effective_message.reply_text(
            "ᴛʜɪꜱ ɢʀᴏᴜᴘ ɪꜱ ɴᴏᴛ ᴀ ᴘᴀʀᴛ ᴏꜰ ᴀɴʏ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ʙᴀʙʏ🥀!",
        )
        return

    if is_user_fed_owner(fed_id, user.id) is False:
        update.effective_message.reply_text("ᴏɴʟʏ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴏᴡɴᴇʀꜱ ᴄᴀɴ ᴅᴏ ᴛʜɪꜱ ʙᴀʙʏ🥀!")
        return

    user = update.effective_user
    chat = update.effective_chat
    getfban = sql.get_all_fban_users(fed_id)
    if len(getfban) == 0:
        update.effective_message.reply_text(
            "ᴛʜᴇ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ʙᴀɴ ʟɪꜱᴛ ᴏꜰ {} ɪꜱ ᴇᴍᴘᴛʏ ʙᴀʙʏ🥀".format(info["fname"]),
            parse_mode=ParseMode.HTML,
        )
        return

    if args:
        if args[0] == "json":
            jam = time.time()
            new_jam = jam + 1800
            cek = get_chat(chat.id, chat_data)
            if cek.get("status"):
                if jam <= int(cek.get("value")):
                    waktu = time.strftime(
                        "%H:%M:%S %d/%m/%Y",
                        time.localtime(cek.get("value")),
                    )
                    update.effective_message.reply_text(
                        "ʏᴏᴜ ᴄᴀɴ ʙᴀᴄᴋᴜᴘ ʏᴏᴜʀ ᴅᴀᴛᴀ ᴏɴᴄᴇ ᴇᴠᴇʀʏ 30 ᴍɪɴᴜᴛᴇꜱ!\nʏᴏᴜ ᴄᴀɴ ʙᴀᴄᴋ ᴜᴘ ᴅᴀᴛᴀ ᴀɢᴀɪɴ ᴀᴛ `{}` ʙᴀʙʏ🥀".format(
                            waktu,
                        ),
                        parse_mode=ParseMode.MARKDOWN,
                    )
                    return
                if user.id not in DRAGONS:
                    put_chat(chat.id, new_jam, chat_data)
            else:
                if user.id not in DRAGONS:
                    put_chat(chat.id, new_jam, chat_data)
            backups = ""
            for users in getfban:
                getuserinfo = sql.get_all_fban_users_target(fed_id, users)
                json_parser = {
                    "user_id": users,
                    "first_name": getuserinfo["first_name"],
                    "last_name": getuserinfo["last_name"],
                    "user_name": getuserinfo["user_name"],
                    "reason": getuserinfo["reason"],
                }
                backups += json.dumps(json_parser)
                backups += "\n"
            with BytesIO(str.encode(backups)) as output:
                output.name = "saitama_fbanned_users.json"
                update.effective_message.reply_document(
                    document=output,
                    filename="saitama_fbanned_users.json",
                    caption="ᴛᴏᴛᴀʟ {} ᴜꜱᴇʀ ᴀʀᴇ ʙʟᴏᴄᴋᴇᴅ ʙʏ ᴛʜᴇ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ {} ʙᴀʙʏ🥀.".format(
                        len(getfban),
                        info["fname"],
                    ),
                )
            return
        if args[0] == "csv":
            jam = time.time()
            new_jam = jam + 1800
            cek = get_chat(chat.id, chat_data)
            if cek.get("status"):
                if jam <= int(cek.get("value")):
                    waktu = time.strftime(
                        "%H:%M:%S %d/%m/%Y",
                        time.localtime(cek.get("value")),
                    )
                    update.effective_message.reply_text(
                        "ʏᴏᴜ ᴄᴀɴ ʙᴀᴄᴋᴜᴘ ʏᴏᴜʀ ᴅᴀᴛᴀ ᴏɴᴄᴇ ᴇᴠᴇʀʏ 30 ᴍɪɴᴜᴛᴇꜱ!\nʏᴏᴜ ᴄᴀɴ ʙᴀᴄᴋ ᴜᴘ ᴅᴀᴛᴀ ᴀɢᴀɪɴ ᴀᴛ `{}` ʙᴀʙʏ🥀".format(
                            waktu,
                        ),
                        parse_mode=ParseMode.MARKDOWN,
                    )
                    return
                if user.id not in DRAGONS:
                    put_chat(chat.id, new_jam, chat_data)
            else:
                if user.id not in DRAGONS:
                    put_chat(chat.id, new_jam, chat_data)
            backups = "id,firstname,lastname,username,reason\n"
            for users in getfban:
                getuserinfo = sql.get_all_fban_users_target(fed_id, users)
                backups += (
                    "{user_id},{first_name},{last_name},{user_name},{reason}".format(
                        user_id=users,
                        first_name=getuserinfo["first_name"],
                        last_name=getuserinfo["last_name"],
                        user_name=getuserinfo["user_name"],
                        reason=getuserinfo["reason"],
                    )
                )
                backups += "\n"
            with BytesIO(str.encode(backups)) as output:
                output.name = "saitama_fbanned_users.csv"
                update.effective_message.reply_document(
                    document=output,
                    filename="saitama_fbanned_users.csv",
                    caption="ᴛᴏᴛᴀʟ {} ᴜꜱᴇʀ ᴀʀᴇ ʙʟᴏᴄᴋᴇᴅ ʙʏ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ {} ʙᴀʙʏ🥀.".format(
                        len(getfban),
                        info["fname"],
                    ),
                )
            return

    text = "<b>{} ᴜꜱᴇʀꜱ ʜᴀᴠᴇ ʙᴇᴇɴ ʙᴀɴɴᴇᴅ ꜰʀᴏᴍ ᴛʜᴇ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ {}:</b>\n".format(
        len(getfban),
        info["fname"],
    )
    for users in getfban:
        getuserinfo = sql.get_all_fban_users_target(fed_id, users)
        if getuserinfo is False:
            text = "ᴛʜᴇʀᴇ ᴀʀᴇ ɴᴏ ᴜꜱᴇʀꜱ ʙᴀɴɴᴇᴅ ꜰʀᴏᴍ ᴛʜᴇ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ {} ʙᴀʙʏ🥀".format(
                info["fname"],
            )
            break
        user_name = getuserinfo["first_name"]
        if getuserinfo["last_name"]:
            user_name += " " + getuserinfo["last_name"]
        text += " • {} (<code>{}</code>)\n".format(
            mention_html(users, user_name),
            users,
        )

    try:
        update.effective_message.reply_text(text, parse_mode=ParseMode.HTML)
    except:
        jam = time.time()
        new_jam = jam + 1800
        cek = get_chat(chat.id, chat_data)
        if cek.get("status"):
            if jam <= int(cek.get("value")):
                waktu = time.strftime(
                    "%H:%M:%S %d/%m/%Y",
                    time.localtime(cek.get("value")),
                )
                update.effective_message.reply_text(
                    "ʏᴏᴜ ᴄᴀɴ ʙᴀᴄᴋᴜᴘ ʏᴏᴜʀ ᴅᴀᴛᴀ ᴏɴᴄᴇ ᴇᴠᴇʀʏ 30 ᴍɪɴᴜᴛᴇꜱ!\nʏᴏᴜ ᴄᴀɴ ʙᴀᴄᴋ ᴜᴘ ᴅᴀᴛᴀ ᴀɢᴀɪɴ ᴀᴛ `{}` ʙᴀʙʏ🥀".format(
                        waktu,
                    ),
                    parse_mode=ParseMode.MARKDOWN,
                )
                return
            if user.id not in DRAGONS:
                put_chat(chat.id, new_jam, chat_data)
        else:
            if user.id not in DRAGONS:
                put_chat(chat.id, new_jam, chat_data)
        cleanr = re.compile("<.*?>")
        cleantext = re.sub(cleanr, "", text)
        with BytesIO(str.encode(cleantext)) as output:
            output.name = "fbanlist.txt"
            update.effective_message.reply_document(
                document=output,
                filename="fbanlist.txt",
                caption="ᴛʜᴇ ꜰᴏʟʟᴏᴡɪɴɢ ɪꜱ ᴀ ʟɪꜱᴛ ᴏꜰ ᴜꜱᴇʀꜱ ᴡʜᴏ ᴀʀᴇ ᴄᴜʀʀᴇɴᴛʟʏ ꜰʙᴀɴɴᴇᴅ ɪɴ ᴛʜᴇ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ {} ʙᴀʙʏ🥀.".format(
                    info["fname"],
                ),
            )


def fed_notif(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    chat = update.effective_chat
    user = update.effective_user
    msg = update.effective_message
    fed_id = sql.get_fed_id(chat.id)

    if not fed_id:
        update.effective_message.reply_text(
            "ᴛʜɪꜱ ɢʀᴏᴜᴘ ɪꜱ ɴᴏᴛ ᴀ ᴘᴀʀᴛ ᴏꜰ ᴀɴʏ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ʙᴀʙʏ🥀!",
        )
        return

    if args:
        if args[0] in ("yes", "on"):
            sql.set_feds_setting(user.id, True)
            msg.reply_text(
                "ʀᴇᴘᴏʀᴛɪɴɢ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ʙᴀᴄᴋ ᴜᴘ! ᴇᴠᴇʀʏ ᴜꜱᴇʀ ᴡʜᴏ ɪꜱ ꜰʙᴀɴ /unfban ʏᴏᴜ ᴡɪʟʟ ʙᴇ ɴᴏᴛɪꜰɪᴇᴅ ᴠɪᴀ ᴘᴍ ʙᴀʙʏ🥀.",
            )
        elif args[0] in ("no", "off"):
            sql.set_feds_setting(user.id, False)
            msg.reply_text(
                "ʀᴇᴘᴏʀᴛɪɴɢ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ʙᴀᴄᴋ ᴜᴘ! ᴇᴠᴇʀʏ ᴜꜱᴇʀ ᴡʜᴏ ɪꜱ ꜰʙᴀɴ /unfban ʏᴏᴜ ᴡɪʟʟ ʙᴇ ɴᴏᴛɪꜰɪᴇᴅ ᴠɪᴀ ᴘᴍ ʙᴀʙʏ🥀.",
            )
        else:
            msg.reply_text("ᴘʟᴇᴀꜱᴇ ᴇɴᴛᴇʀ `on`/`off`", parse_mode="markdown")
    else:
        getreport = sql.user_feds_report(user.id)
        msg.reply_text(
            "ʏᴏᴜʀ ᴄᴜʀʀᴇɴᴛ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ʀᴇᴘᴏʀᴛ ᴘʀᴇꜰᴇʀᴇɴᴄᴇꜱ: `{}` ʙᴀʙʏ🥀".format(getreport),
            parse_mode="markdown",
        )


def fed_chats(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    chat = update.effective_chat
    user = update.effective_user

    if chat.type == "private":
        send_message(
            update.effective_message,
            "ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪꜱ ꜱᴘᴇᴄɪꜰɪᴄ ᴛᴏ ᴛʜᴇ ɢʀᴏᴜᴘ, ɴᴏᴛ ᴛᴏ ᴏᴜʀ ᴘᴍ ʙᴀʙʏ🥀!",
        )
        return

    fed_id = sql.get_fed_id(chat.id)
    info = sql.get_fed_info(fed_id)

    if not fed_id:
        update.effective_message.reply_text(
            "ᴛʜɪꜱ ɢʀᴏᴜᴘ ɪꜱ ɴᴏᴛ ᴀ ᴘᴀʀᴛ ᴏꜰ ᴀɴʏ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ʙᴀʙʏ🥀!",
        )
        return

    if is_user_fed_admin(fed_id, user.id) is False:
        update.effective_message.reply_text("ᴏɴʟʏ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ᴅᴏ ᴛʜɪꜱ ʙᴀʙʏ🥀!")
        return

    getlist = sql.all_fed_chats(fed_id)
    if len(getlist) == 0:
        update.effective_message.reply_text(
            "ɴᴏ ᴜꜱᴇʀꜱ ᴀʀᴇ ꜰʙᴀɴɴᴇᴅ ꜰʀᴏᴍ ᴛʜᴇ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ {} ʙᴀʙʏ🥀".format(info["fname"]),
            parse_mode=ParseMode.HTML,
        )
        return

    text = "<b>ɴᴇᴡ ᴄʜᴀᴛ ᴊᴏɪɴᴇᴅ ᴛʜᴇ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ {}:</b>\n".format(info["fname"])
    for chats in getlist:
        try:
            chat_name = dispatcher.bot.getChat(chats).title
        except Unauthorized:
            sql.chat_leave_fed(chats)
            LOGGER.info(
                "ᴄʜᴀᴛ {} ʜᴀꜱ ʟᴇᴀᴠᴇ ꜰᴇᴅ {} ʙᴇᴄᴀᴜꜱᴇ ɪ ᴡᴀꜱ ᴋɪᴄᴋᴇᴅ ʙᴀʙʏ🥀".format(
                    chats,
                    info["fname"],
                ),
            )
            continue
        text += " • {} (<code>{}</code>)\n".format(chat_name, chats)

    try:
        update.effective_message.reply_text(text, parse_mode=ParseMode.HTML)
    except:
        cleanr = re.compile("<.*?>")
        cleantext = re.sub(cleanr, "", text)
        with BytesIO(str.encode(cleantext)) as output:
            output.name = "fedchats.txt"
            update.effective_message.reply_document(
                document=output,
                filename="fedchats.txt",
                caption="ʜᴇʀᴇ ɪꜱ ᴀ ʟɪꜱᴛ ᴏꜰ ᴀʟʟ ᴛʜᴇ ᴄʜᴀᴛꜱ ᴛʜᴀᴛ ᴊᴏɪɴᴇᴅ ᴛʜᴇ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ {} ʙᴀʙʏ🥀.".format(
                    info["fname"],
                ),
            )


def fed_import_bans(update: Update, context: CallbackContext):
    bot, chat_data = context.bot, context.chat_data
    chat = update.effective_chat
    user = update.effective_user
    msg = update.effective_message

    if chat.type == "private":
        send_message(
            update.effective_message,
            "ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪꜱ ꜱᴘᴇᴄɪꜰɪᴄ ᴛᴏ ᴛʜᴇ ɢʀᴏᴜᴘ, ɴᴏᴛ ᴛᴏ ᴏᴜʀ ᴘᴍ ʙᴀʙʏ🥀!",
        )
        return

    fed_id = sql.get_fed_id(chat.id)
    info = sql.get_fed_info(fed_id)
    getfed = sql.get_fed_info(fed_id)

    if not fed_id:
        update.effective_message.reply_text(
            "ᴛʜɪꜱ ɢʀᴏᴜᴘ ɪꜱ ɴᴏᴛ ᴀ ᴘᴀʀᴛ ᴏꜰ ᴀɴʏ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ʙᴀʙʏ🥀!",
        )
        return

    if is_user_fed_owner(fed_id, user.id) is False:
        update.effective_message.reply_text("ᴏɴʟʏ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴏᴡɴᴇʀꜱ ᴄᴀɴ ᴅᴏ ᴛʜɪꜱ ʙᴀʙʏ🥀!")
        return

    if msg.reply_to_message and msg.reply_to_message.document:
        jam = time.time()
        new_jam = jam + 1800
        cek = get_chat(chat.id, chat_data)
        if cek.get("status"):
            if jam <= int(cek.get("value")):
                waktu = time.strftime(
                    "%H:%M:%S %d/%m/%Y",
                    time.localtime(cek.get("value")),
                )
                update.effective_message.reply_text(
                    "ʏᴏᴜ ᴄᴀɴ ɢᴇᴛ ʏᴏᴜʀ ᴅᴀᴛᴀ ᴏɴᴄᴇ ᴇᴠᴇʀʏ 30 ᴍɪɴᴜᴛᴇꜱ!\nʏᴏᴜ ᴄᴀɴ ɢᴇᴛ ᴅᴀᴛᴀ ᴀɢᴀɪɴ ᴀᴛ `{}` ʙᴀʙʏ🥀".format(
                        waktu,
                    ),
                    parse_mode=ParseMode.MARKDOWN,
                )
                return
            if user.id not in DRAGONS:
                put_chat(chat.id, new_jam, chat_data)
        else:
            if user.id not in DRAGONS:
                put_chat(chat.id, new_jam, chat_data)
        # if int(int(msg.reply_to_message.document.file_size)/1024) >= 200:
        # 	msg.reply_text("This file is too big!")
        # 	return
        success = 0
        failed = 0
        try:
            file_info = bot.get_file(msg.reply_to_message.document.file_id)
        except BadRequest:
            msg.reply_text(
                "ᴛʀʏ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴀɴᴅ ʀᴇ-ᴜᴘʟᴏᴀᴅɪɴɢ ᴛʜᴇ ꜰɪʟᴇ, ᴛʜɪꜱ ᴏɴᴇ ꜱᴇᴇᴍꜱ ʙʀᴏᴋᴇɴ ʙᴀʙʏ🥀!",
            )
            return
        fileformat = msg.reply_to_message.document.file_name.split(".")[-1]
        if fileformat == "json":
            multi_fed_id = []
            multi_import_userid = []
            multi_import_firstname = []
            multi_import_lastname = []
            multi_import_username = []
            multi_import_reason = []
            with BytesIO() as file:
                file_info.download(out=file)
                file.seek(0)
                reading = file.read().decode("UTF-8")
                splitting = reading.split("\n")
                for x in splitting:
                    if x == "":
                        continue
                    try:
                        data = json.loads(x)
                    except json.decoder.JSONDecodeError as err:
                        failed += 1
                        continue
                    try:
                        import_userid = int(data["user_id"])  # Make sure it int
                        import_firstname = str(data["first_name"])
                        import_lastname = str(data["last_name"])
                        import_username = str(data["user_name"])
                        import_reason = str(data["reason"])
                    except ValueError:
                        failed += 1
                        continue
                    # Checking user
                    if int(import_userid) == bot.id:
                        failed += 1
                        continue
                    if is_user_fed_owner(fed_id, import_userid) is True:
                        failed += 1
                        continue
                    if is_user_fed_admin(fed_id, import_userid) is True:
                        failed += 1
                        continue
                    if str(import_userid) == str(OWNER_ID):
                        failed += 1
                        continue
                    if int(import_userid) in DRAGONS:
                        failed += 1
                        continue
                    if int(import_userid) in TIGERS:
                        failed += 1
                        continue
                    if int(import_userid) in WOLVES:
                        failed += 1
                        continue
                    multi_fed_id.append(fed_id)
                    multi_import_userid.append(str(import_userid))
                    multi_import_firstname.append(import_firstname)
                    multi_import_lastname.append(import_lastname)
                    multi_import_username.append(import_username)
                    multi_import_reason.append(import_reason)
                    success += 1
                sql.multi_fban_user(
                    multi_fed_id,
                    multi_import_userid,
                    multi_import_firstname,
                    multi_import_lastname,
                    multi_import_username,
                    multi_import_reason,
                )
            text = "ʙʟᴏᴄᴋꜱ ᴡᴇʀᴇ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ɪᴍᴘᴏʀᴛᴇᴅ. {} ᴘᴇᴏᴘʟᴇ ᴀʀᴇ ʙʟᴏᴄᴋᴇᴅ ʙᴀʙʏ🥀.".format(
                success,
            )
            if failed >= 1:
                text += " {} Failed to import.".format(failed)
            get_fedlog = sql.get_fed_log(fed_id)
            if get_fedlog:
                if ast.literal_eval(get_fedlog):
                    teks = "ꜰᴇᴅ *{}* ʜᴀꜱ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ɪᴍᴘᴏʀᴛᴇᴅ ᴅᴀᴛᴀ. {} ʙᴀɴɴᴇᴅ ʙᴀʙʏ🥀.".format(
                        getfed["fname"],
                        success,
                    )
                    if failed >= 1:
                        teks += " {} Failed to import ʙᴀʙʏ🥀.".format(failed)
                    bot.send_message(get_fedlog, teks, parse_mode="markdown")
        elif fileformat == "csv":
            multi_fed_id = []
            multi_import_userid = []
            multi_import_firstname = []
            multi_import_lastname = []
            multi_import_username = []
            multi_import_reason = []
            file_info.download(
                "fban_{}.csv".format(msg.reply_to_message.document.file_id),
            )
            with open(
                "fban_{}.csv".format(msg.reply_to_message.document.file_id),
                "r",
                encoding="utf8",
            ) as csvFile:
                reader = csv.reader(csvFile)
                for data in reader:
                    try:
                        import_userid = int(data[0])  # Make sure it int
                        import_firstname = str(data[1])
                        import_lastname = str(data[2])
                        import_username = str(data[3])
                        import_reason = str(data[4])
                    except ValueError:
                        failed += 1
                        continue
                    # Checking user
                    if int(import_userid) == bot.id:
                        failed += 1
                        continue
                    if is_user_fed_owner(fed_id, import_userid) is True:
                        failed += 1
                        continue
                    if is_user_fed_admin(fed_id, import_userid) is True:
                        failed += 1
                        continue
                    if str(import_userid) == str(OWNER_ID):
                        failed += 1
                        continue
                    if int(import_userid) in DRAGONS:
                        failed += 1
                        continue
                    if int(import_userid) in TIGERS:
                        failed += 1
                        continue
                    if int(import_userid) in WOLVES:
                        failed += 1
                        continue
                    multi_fed_id.append(fed_id)
                    multi_import_userid.append(str(import_userid))
                    multi_import_firstname.append(import_firstname)
                    multi_import_lastname.append(import_lastname)
                    multi_import_username.append(import_username)
                    multi_import_reason.append(import_reason)
                    success += 1
                    # t = ThreadWithReturnValue(target=sql.fban_user, args=(fed_id, str(import_userid), import_firstname, import_lastname, import_username, import_reason,))
                    # t.start()
                sql.multi_fban_user(
                    multi_fed_id,
                    multi_import_userid,
                    multi_import_firstname,
                    multi_import_lastname,
                    multi_import_username,
                    multi_import_reason,
                )
            csvFile.close()
            os.remove("fban_{}.csv".format(msg.reply_to_message.document.file_id))
            text = "ꜰɪʟᴇꜱ ᴡᴇʀᴇ ɪᴍᴘᴏʀᴛᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ. {} ᴘᴇᴏᴘʟᴇ ʙᴀɴɴᴇᴅ ʙᴀʙʏ🥀.".format(success)
            if failed >= 1:
                text += " {} Failed to import.".format(failed)
            get_fedlog = sql.get_fed_log(fed_id)
            if get_fedlog:
                if ast.literal_eval(get_fedlog):
                    teks = "Fed *{}* has successfully imported data. {} banned ʙᴀʙʏ🥀.".format(
                        getfed["fname"],
                        success,
                    )
                    if failed >= 1:
                        teks += " {} Failed to import.".format(failed)
                    bot.send_message(get_fedlog, teks, parse_mode="markdown")
        else:
            send_message(update.effective_message, "ᴛʜɪꜱ ꜰɪʟᴇ ɪꜱ ɴᴏᴛ ꜱᴜᴘᴘᴏʀᴛᴇᴅ ʙᴀʙʏ🥀.")
            return
        send_message(update.effective_message, text)


def del_fed_button(update: Update, context: CallbackContext):
    query = update.callback_query
    userid = query.message.chat.id
    fed_id = query.data.split("_")[1]

    if fed_id == "cancel":
        query.message.edit_text("ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴅᴇʟᴇᴛɪᴏɴ ᴄᴀɴᴄᴇʟʟᴇᴅ ʙᴀʙʏ🥀")
        return

    getfed = sql.get_fed_info(fed_id)
    if getfed:
        delete = sql.del_fed(fed_id)
        if delete:
            query.message.edit_text(
                "ʏᴏᴜ ʜᴀᴠᴇ ʀᴇᴍᴏᴠᴇᴅ ʏᴏᴜʀ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ʙᴀʙʏ🥀! ɴᴏᴡ ᴀʟʟ ᴛʜᴇ ɢʀᴏᴜᴘꜱ ᴛʜᴀᴛ ᴀʀᴇ ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴡɪᴛʜ `{}` ᴅᴏ ɴᴏᴛ ʜᴀᴠᴇ ᴀ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ.".format(
                    getfed["fname"],
                ),
                parse_mode="markdown",
            )


def fed_stat_user(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    chat = update.effective_chat
    user = update.effective_user
    msg = update.effective_message

    if args:
        if args[0].isdigit():
            user_id = args[0]
        else:
            user_id = extract_user(msg, args)
    else:
        user_id = extract_user(msg, args)

    if user_id:
        if len(args) == 2 and args[0].isdigit():
            fed_id = args[1]
            user_name, reason, fbantime = sql.get_user_fban(fed_id, str(user_id))
            if fbantime:
                fbantime = time.strftime("%d/%m/%Y", time.localtime(fbantime))
            else:
                fbantime = "Unavaiable"
            if user_name is False:
                send_message(
                    update.effective_message,
                    "Fed {} not found!".format(fed_id),
                    parse_mode="markdown",
                )
                return
            if user_name == "" or user_name is None:
                user_name = "He/she"
            if not ʀᴇᴀꜱᴏɴ:
                send_message(
                    update.effective_message,
                    "{} ɪꜱ ɴᴏᴛ ʙᴀɴɴᴇᴅ ɪɴ ᴛʜɪꜱ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ!".format(user_name),
                )
            else:
                teks = "{} ʙᴀɴɴᴇᴅ ɪɴ ᴛʜɪꜱ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ʙᴇᴄᴀᴜꜱᴇ:\n`{}`\n*ʙᴀɴɴᴇᴅ ᴀᴛ:* `{}` ʙᴀʙʏ🥀".format(
                    user_name,
                    reason,
                    fbantime,
                )
                send_message(update.effective_message, teks, parse_mode="markdown")
            return
        user_name, fbanlist = sql.get_user_fbanlist(str(user_id))
        if user_name == "":
            try:
                user_name = bot.get_chat(user_id).first_name
            except BadRequest:
                user_name = "He/she"
            if user_name == "" or user_name is None:
                user_name = "He/she"
        if len(fbanlist) == 0:
            send_message(
                update.effective_message,
                "{} ɪꜱ ɴᴏᴛ ʙᴀɴɴᴇᴅ ɪɴ ᴀɴʏ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ʙᴀʙʏ🥀!".format(user_name),
            )
            return
        teks = "{} ʜᴀꜱ ʙᴇᴇɴ ʙᴀɴɴᴇᴅ ɪɴ ᴛʜɪꜱ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ʙᴀʙʏ🥀:\n".format(user_name)
        for x in fbanlist:
            teks += "- `{}`: {}\n".format(x[0], x[1][:20])
        teks += "\nɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ꜰɪɴᴅ ᴏᴜᴛ ᴍᴏʀᴇ ᴀʙᴏᴜᴛ ᴛʜᴇ ʀᴇᴀꜱᴏɴꜱ ꜰᴏʀ ꜰᴇᴅʙᴀɴ ꜱᴘᴇᴄɪꜰɪᴄᴀʟʟʏ, ᴜꜱᴇ /fbanstat <FedID> ʙᴀʙʏ🥀"
        send_message(update.effective_message, teks, parse_mode="markdown")

    elif not msg.reply_to_message and not args:
        user_id = msg.from_user.id
        user_name, fbanlist = sql.get_user_fbanlist(user_id)
        if user_name == "":
            user_name = msg.from_user.first_name
        if len(fbanlist) == 0:
            send_message(
                update.effective_message,
                "{} ɪꜱ ɴᴏᴛ ʙᴀɴɴᴇᴅ ɪɴ ᴀɴʏ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ʙᴀʙʏ🥀!".format(user_name),
            )
        else:
            teks = "{} ʜᴀꜱ ʙᴇᴇɴ ʙᴀɴɴᴇᴅ ɪɴ ᴛʜɪꜱ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ʙᴀʙʏ🥀:\n".format(user_name)
            for x in fbanlist:
                teks += "- `{}`: {}\n".format(x[0], x[1][:20])
            teks += "\nɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ꜰɪɴᴅ ᴏᴜᴛ ᴍᴏʀᴇ ᴀʙᴏᴜᴛ ᴛʜᴇ ʀᴇᴀꜱᴏɴꜱ ꜰᴏʀ ꜰᴇᴅʙᴀɴ ꜱᴘᴇᴄɪꜰɪᴄᴀʟʟʏ, ᴜꜱᴇ /fbanstat <FedID> ʙᴀʙʏ🥀"
            send_message(update.effective_message, teks, parse_mode="markdown")

    else:
        fed_id = args[0]
        fedinfo = sql.get_fed_info(fed_id)
        if not fedinfo:
            send_message(update.effective_message, "Fed {} not found ʙᴀʙʏ🥀!".format(fed_id))
            return
        name, reason, fbantime = sql.get_user_fban(fed_id, msg.from_user.id)
        if fbantime:
            fbantime = time.strftime("%d/%m/%Y", time.localtime(fbantime))
        else:
            fbantime = "Unavaiable"
        if not name:
            name = msg.from_user.first_name
        if not ʀᴇᴀꜱᴏɴ:
            send_message(
                update.effective_message,
                "{} ɪꜱ ɴᴏᴛ ʙᴀɴɴᴇᴅ ɪɴ ᴛʜɪꜱ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ʙᴀʙʏ🥀".format(name),
            )
            return
        send_message(
            update.effective_message,
            "{} ʙᴀɴɴᴇᴅ ɪɴ ᴛʜɪꜱ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ʙᴇᴄᴀᴜꜱᴇ:\n`{}`\n*ʙᴀɴɴᴇᴅ ᴀᴛ:* `{}` ʙᴀʙʏ🥀".format(
                name,
                reason,
                fbantime,
            ),
            parse_mode="markdown",
        )


def set_fed_log(update: Update, context: CallbackContext):
    args = context.args
    chat = update.effective_chat
    user = update.effective_user
    msg = update.effective_message

    if chat.type == "private":
        send_message(
            update.effective_message,
            "ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪꜱ ꜱᴘᴇᴄɪꜰɪᴄ ᴛᴏ ᴛʜᴇ ɢʀᴏᴜᴘ, ɴᴏᴛ ᴛᴏ ᴏᴜʀ ᴘᴍ ʙᴀʙʏ🥀!",
        )
        return

    if args:
        fedinfo = sql.get_fed_info(args[0])
        if not fedinfo:
            send_message(update.effective_message, "ᴛʜɪꜱ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴅᴏᴇꜱ ɴᴏᴛ ᴇxɪꜱᴛ ʙᴀʙʏ🥀!")
            return
        isowner = is_user_fed_owner(args[0], user.id)
        if not isowner:
            send_message(
                update.effective_message,
                "ᴏɴʟʏ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴄʀᴇᴀᴛᴏʀ ᴄᴀɴ ꜱᴇᴛ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ʟᴏɢꜱ ʙᴀʙʏ🥀.",
            )
            return
        setlog = sql.set_fed_log(args[0], chat.id)
        if setlog:
            send_message(
                update.effective_message,
                "ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ʟᴏɢ `{}` ʜᴀꜱ ʙᴇᴇɴ ꜱᴇᴛ ᴛᴏ {} ʙᴀʙʏ🥀".format(
                    fedinfo["fname"],
                    chat.title,
                ),
                parse_mode="markdown",
            )
    else:
        send_message(
            update.effective_message,
            "ʏᴏᴜ ʜᴀᴠᴇ ɴᴏᴛ ᴘʀᴏᴠɪᴅᴇᴅ ʏᴏᴜʀ ꜰᴇᴅᴇʀᴀᴛᴇᴅ ɪᴅ ʙᴀʙʏ🥀!",
        )


def unset_fed_log(update: Update, context: CallbackContext):
    args = context.args
    chat = update.effective_chat
    user = update.effective_user
    msg = update.effective_message

    if chat.type == "private":
        send_message(
            update.effective_message,
            "ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪꜱ ꜱᴘᴇᴄɪꜰɪᴄ ᴛᴏ ᴛʜᴇ ɢʀᴏᴜᴘ, ɴᴏᴛ ᴛᴏ ᴏᴜʀ ᴘᴍ ʙᴀʙʏ🥀!",
        )
        return

    if args:
        fedinfo = sql.get_fed_info(args[0])
        if not fedinfo:
            send_message(update.effective_message, "ᴛʜɪꜱ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴅᴏᴇꜱ ɴᴏᴛ ᴇxɪꜱᴛ ʙᴀʙʏ🥀!")
            return
        isowner = is_user_fed_owner(args[0], user.id)
        if not isowner:
            send_message(
                update.effective_message,
                "ᴏɴʟʏ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴄʀᴇᴀᴛᴏʀ ᴄᴀɴ ꜱᴇᴛ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ʟᴏɢꜱ ʙᴀʙʏ🥀.",
            )
            return
        setlog = sql.set_fed_log(args[0], None)
        if setlog:
            send_message(
                update.effective_message,
                "ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ʟᴏɢ `{}` ʜᴀꜱ ʙᴇᴇɴ ʀᴇᴠᴏᴋᴇᴅ ᴏɴ {} ʙᴀʙʏ🥀".format(
                    fedinfo["fname"],
                    chat.title,
                ),
                parse_mode="markdown",
            )
    else:
        send_message(
            update.effective_message,
            "ʏᴏᴜ ʜᴀᴠᴇ ɴᴏᴛ ᴘʀᴏᴠɪᴅᴇᴅ ʏᴏᴜʀ ꜰᴇᴅᴇʀᴀᴛᴇᴅ ɪᴅ ʙᴀʙʏ🥀!",
        )


def subs_feds(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    chat = update.effective_chat
    user = update.effective_user
    msg = update.effective_message

    if chat.type == "private":
        send_message(
            update.effective_message,
            "ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪꜱ ꜱᴘᴇᴄɪꜰɪᴄ ᴛᴏ ᴛʜᴇ ɢʀᴏᴜᴘ, ɴᴏᴛ ᴛᴏ ᴏᴜʀ ᴘᴍ ʙᴀʙʏ🥀!",
        )
        return

    fed_id = sql.get_fed_id(chat.id)
    fedinfo = sql.get_fed_info(fed_id)

    if not fed_id:
        send_message(update.effective_message, "ᴛʜɪꜱ ɢʀᴏᴜᴘ ɪꜱ ɴᴏᴛ ɪɴ ᴀɴʏ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ʙᴀʙʏ🥀!")
        return

    if is_user_fed_owner(fed_id, user.id) is False:
        send_message(update.effective_message, "ᴏɴʟʏ ꜰᴇᴅ ᴏᴡɴᴇʀ ᴄᴀɴ ᴅᴏ ᴛʜɪꜱ ʙᴀʙʏ🥀!")
        return

    if args:
        getfed = sql.search_fed_by_id(args[0])
        if getfed is False:
            send_message(
                update.effective_message,
                "ᴘʟᴇᴀꜱᴇ ᴇɴᴛᴇʀ ᴀ ᴠᴀʟɪᴅ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ɪᴅ ʙᴀʙʏ🥀.",
            )
            return
        subfed = sql.subs_fed(args[0], fed_id)
        if subfed:
            send_message(
                update.effective_message,
                "ꜰᴇᴅᴇʀᴀᴛɪᴏɴ `{}` ʜᴀꜱ ꜱᴜʙꜱᴄʀɪʙᴇ ᴛʜᴇ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ `{}` ʙᴀʙʏ🥀. ᴇᴠᴇʀʏ ᴛɪᴍᴇ ᴛʜᴇʀᴇ ɪꜱ ᴀ ꜰᴇᴅʙᴀɴ ꜰʀᴏᴍ ᴛʜᴀᴛ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ, ᴛʜɪꜱ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴡɪʟʟ ᴀʟꜱᴏ ʙᴀɴɴᴇᴅ ᴛʜᴀᴛ ᴜꜱᴇʀ.".format(
                    fedinfo["fname"],
                    getfed["fname"],
                ),
                parse_mode="markdown",
            )
            get_fedlog = sql.get_fed_log(args[0])
            if get_fedlog:
                if int(get_fedlog) != int(chat.id):
                    bot.send_message(
                        get_fedlog,
                        "ꜰᴇᴅᴇʀᴀᴛɪᴏɴ `{}` ʜᴀꜱ ꜱᴜʙꜱᴄʀɪʙᴇ ᴛʜᴇ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ `{}`".format(
                            fedinfo["fname"],
                            getfed["fname"],
                        ),
                        parse_mode="markdown",
                    )
        else:
            send_message(
                update.effective_message,
                "ꜰᴇᴅᴇʀᴀᴛɪᴏɴ `{}` ᴀʟʀᴇᴀᴅʏ ꜱᴜʙꜱᴄʀɪʙᴇ ᴛʜᴇ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ `{}` ʙᴀʙʏ🥀.".format(
                    fedinfo["fname"],
                    getfed["fname"],
                ),
                parse_mode="markdown",
            )
    else:
        send_message(
            update.effective_message,
            "ʏᴏᴜ ʜᴀᴠᴇ ɴᴏᴛ ᴘʀᴏᴠɪᴅᴇᴅ ʏᴏᴜʀ ꜰᴇᴅᴇʀᴀᴛᴇᴅ ɪᴅ ʙᴀʙʏ🥀!",
        )


def unsubs_feds(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    chat = update.effective_chat
    user = update.effective_user
    msg = update.effective_message

    if chat.type == "private":
        send_message(
            update.effective_message,
            "ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪꜱ ꜱᴘᴇᴄɪꜰɪᴄ ᴛᴏ ᴛʜᴇ ɢʀᴏᴜᴘ, ɴᴏᴛ ᴛᴏ ᴏᴜʀ ᴘᴍ ʙᴀʙʏ🥀!",
        )
        return

    fed_id = sql.get_fed_id(chat.id)
    fedinfo = sql.get_fed_info(fed_id)

    if not fed_id:
        send_message(update.effective_message, "ᴛʜɪꜱ ɢʀᴏᴜᴘ ɪꜱ ɴᴏᴛ ɪɴ ᴀɴʏ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ʙᴀʙʏ🥀!")
        return

    if is_user_fed_owner(fed_id, user.id) is False:
        send_message(update.effective_message, "ᴏɴʟʏ ꜰᴇᴅ ᴏᴡɴᴇʀ ᴄᴀɴ ᴅᴏ ᴛʜɪꜱ ʙᴀʙʏ🥀!")
        return

    if args:
        getfed = sql.search_fed_by_id(args[0])
        if getfed is False:
            send_message(
                update.effective_message,
                "ᴘʟᴇᴀꜱᴇ ᴇɴᴛᴇʀ ᴀ ᴠᴀʟɪᴅ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ɪᴅ ʙᴀʙʏ🥀.",
            )
            return
        subfed = sql.unsubs_fed(args[0], fed_id)
        if subfed:
            send_message(
                update.effective_message,
                "ꜰᴇᴅᴇʀᴀᴛɪᴏɴ `{}` ɴᴏᴡ ᴜɴꜱᴜʙꜱᴄʀɪʙᴇ ꜰᴇᴅ `{}` ʙᴀʙʏ🥀.".format(
                    fedinfo["fname"],
                    getfed["fname"],
                ),
                parse_mode="markdown",
            )
            get_fedlog = sql.get_fed_log(args[0])
            if get_fedlog:
                if int(get_fedlog) != int(chat.id):
                    bot.send_message(
                        get_fedlog,
                        "ꜰᴇᴅᴇʀᴀᴛɪᴏɴ `{}` ʜᴀꜱ ᴜɴꜱᴜʙꜱᴄʀɪʙᴇ ꜰᴇᴅ `{}` ʙᴀʙʏ🥀.".format(
                            fedinfo["fname"],
                            getfed["fname"],
                        ),
                        parse_mode="markdown",
                    )
        else:
            send_message(
                update.effective_message,
                "ꜰᴇᴅᴇʀᴀᴛɪᴏɴ `{}` ɪꜱ ɴᴏᴛ ꜱᴜʙꜱᴄʀɪʙɪɴɢ `{}` ʙᴀʙʏ🥀.".format(
                    fedinfo["fname"],
                    getfed["fname"],
                ),
                parse_mode="markdown",
            )
    else:
        send_message(
            update.effective_message,
            "ʏᴏᴜ ʜᴀᴠᴇ ɴᴏᴛ ᴘʀᴏᴠɪᴅᴇᴅ ʏᴏᴜʀ ꜰᴇᴅᴇʀᴀᴛᴇᴅ ɪᴅ ʙᴀʙʏ🥀!",
        )


def get_myfedsubs(update: Update, context: CallbackContext):
    args = context.args
    chat = update.effective_chat
    user = update.effective_user
    msg = update.effective_message

    if chat.type == "private":
        send_message(
            update.effective_message,
            "ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪꜱ ꜱᴘᴇᴄɪꜰɪᴄ ᴛᴏ ᴛʜᴇ ɢʀᴏᴜᴘ, ɴᴏᴛ ᴛᴏ ᴏᴜʀ ᴘᴍ ʙᴀʙʏ🥀!",
        )
        return

    fed_id = sql.get_fed_id(chat.id)
    fedinfo = sql.get_fed_info(fed_id)

    if not fed_id:
        send_message(update.effective_message, "ᴛʜɪꜱ ɢʀᴏᴜᴘ ɪꜱ ɴᴏᴛ ɪɴ ᴀɴʏ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ʙᴀʙʏ🥀!")
        return

    if is_user_fed_owner(fed_id, user.id) is False:
        send_message(update.effective_message, "ᴏɴʟʏ ꜰᴇᴅ ᴏᴡɴᴇʀ ᴄᴀɴ ᴅᴏ ᴛʜɪꜱ ʙᴀʙʏ🥀!")
        return

    try:
        getmy = sql.get_mysubs(fed_id)
    except:
        getmy = []

    if len(getmy) == 0:
        send_message(
            update.effective_message,
            "ꜰᴇᴅᴇʀᴀᴛɪᴏɴ `{}` ɪꜱ ɴᴏᴛ ꜱᴜʙꜱᴄʀɪʙɪɴɢ ᴀɴʏ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ʙᴀʙʏ🥀.".format(
                fedinfo["fname"],
            ),
            parse_mode="markdown",
        )
        return
    listfed = "ꜰᴇᴅᴇʀᴀᴛɪᴏɴ `{}` ɪꜱ ꜱᴜʙꜱᴄʀɪʙɪɴɢ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ʙᴀʙʏ🥀:\n".format(
        fedinfo["fname"],
    )
    for x in getmy:
        listfed += "- `{}`\n".format(x)
    listfed += (
        "\nᴛᴏ ɢᴇᴛ ꜰᴇᴅ ɪɴꜰᴏ `/fedinfo <fedid>`. ᴛᴏ ᴜɴꜱᴜʙꜱᴄʀɪʙᴇ `/unsubfed <fedid>` ʙᴀʙʏ🥀."
    )
    send_message(update.effective_message, listfed, parse_mode="markdown")


def get_myfeds_list(update: Update, context: CallbackContext):
    chat = update.effective_chat
    user = update.effective_user
    msg = update.effective_message

    fedowner = sql.get_user_owner_fed_full(user.id)
    if fedowner:
        text = "*ʏᴏᴜ ᴀʀᴇ ᴏᴡɴᴇʀ ᴏꜰ ꜰᴇᴅꜱ ʙᴀʙʏ🥀:\n*"
        for f in fedowner:
            text += "- `{}`: *{}*\n".format(f["fed_id"], f["fed"]["fname"])
    else:
        text = "*ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ʜᴀᴠᴇ ᴀɴʏ ꜰᴇᴅꜱ ʙᴀʙʏ🥀!*"
    send_message(update.effective_message, text, parse_mode="markdown")


def is_user_fed_admin(fed_id, user_id):
    fed_admins = sql.all_fed_users(fed_id)
    if fed_admins is False:
        return False
    return bool(int(user_id) in fed_admins or int(user_id) == OWNER_ID)


def is_user_fed_owner(fed_id, user_id):
    getsql = sql.get_fed_info(fed_id)
    if getsql is False:
        return False
    getfedowner = ast.literal_eval(getsql["fusers"])
    if getfedowner is None or getfedowner is False:
        return False
    getfedowner = getfedowner["owner"]
    return bool(str(user_id) == getfedowner or int(user_id) == OWNER_ID)


# There's no handler for this yet, but updating for v12 in case its used
def welcome_fed(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    chat = update.effective_chat
    user = update.effective_user
    fed_id = sql.get_fed_id(chat.id)
    fban, fbanreason, fbantime = sql.get_fban_user(fed_id, user.id)
    if fban:
        update.effective_message.reply_text(
            "ᴛʜɪꜱ ᴜꜱᴇʀ ɪꜱ ʙᴀɴɴᴇᴅ ɪɴ ᴄᴜʀʀᴇɴᴛ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ! ɪ ᴡɪʟʟ ʀᴇᴍᴏᴠᴇ ʜɪᴍ ʙᴀʙʏ🥀.",
        )
        bot.kick_chat_member(chat.id, user.id)
        return True
    return False


def __stats__():
    all_fbanned = sql.get_all_fban_users_global()
    all_feds = sql.get_all_feds_users_global()
    return "× {} ʙᴀɴɴᴇᴅ ᴜꜱᴇʀꜱ ᴀᴄʀᴏꜱꜱ {} ꜰᴇᴅᴇʀᴀᴛɪᴏɴꜱ ʙᴀʙʏ🥀".format(
        len(all_fbanned),
        len(all_feds),
    )


def __user_info__(user_id, chat_id):
    fed_id = sql.get_fed_id(chat_id)
    if fed_id:
        fban, fbanreason, fbantime = sql.get_fban_user(fed_id, user_id)
        info = sql.get_fed_info(fed_id)
        infoname = info["fname"]

        if int(info["owner"]) == user_id:
            text = "ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴏᴡɴᴇʀ ᴏꜰ: <b>{}</b> ʙᴀʙʏ🥀.".format(infoname)
        elif is_user_fed_admin(fed_id, user_id):
            text = "ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴀᴅᴍɪɴ ᴏꜰ: <b>{}</b> ʙᴀʙʏ🥀.".format(infoname)

        elif fban:
            text = "ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ʙᴀɴɴᴇᴅ: <b>Yes</b>"
            text += "\n<b>ʀᴇᴀꜱᴏɴ:</b> {} ʙᴀʙʏ🥀".format(fbanreason)
        else:
            text = "ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ʙᴀɴɴᴇᴅ: <b>No</b>"
    else:
        text = ""
    return text


# Temporary data
def put_chat(chat_id, value, chat_data):
    # print(chat_data)
    if value is False:
        status = False
    else:
        status = True
    chat_data[chat_id] = {"federation": {"status": status, "value": value}}


def get_chat(chat_id, chat_data):
    # print(chat_data)
    try:
        value = chat_data[chat_id]["federation"]
        return value
    except KeyError:
        return {"status": False, "value": False}


def fed_owner_help(update: Update, context: CallbackContext):
    update.effective_message.reply_text(
        """*👑 Fed Owner Only:*
 » `/newfed <fed_name>`*:* ᴄʀᴇᴀᴛᴇꜱ ᴀ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ, ᴏɴᴇ ᴀʟʟᴏᴡᴇᴅ ᴘᴇʀ ᴜꜱᴇʀ
 » `/renamefed <fed_id> <new_fed_name>`*:* ʀᴇɴᴀᴍᴇꜱ ᴛʜᴇ ꜰᴇᴅ ɪᴅ ᴛᴏ ᴀ ɴᴇᴡ ɴᴀᴍᴇ
 » `/delfed <fed_id>`*:* ᴅᴇʟᴇᴛᴇ ᴀ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ, ᴀɴᴅ ᴀɴʏ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ ʀᴇʟᴀᴛᴇᴅ ᴛᴏ ɪᴛ. ᴡɪʟʟ ɴᴏᴛ ᴄᴀɴᴄᴇʟ ʙʟᴏᴄᴋᴇᴅ ᴜꜱᴇʀꜱ
 » `/fpromote <user>`*:* ᴀꜱꜱɪɢɴꜱ ᴛʜᴇ ᴜꜱᴇʀ ᴀꜱ ᴀ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴀᴅᴍɪɴ. ᴇɴᴀʙʟᴇꜱ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅꜱ ꜰᴏʀ ᴛʜᴇ ᴜꜱᴇʀ ᴜɴᴅᴇʀ `ꜰᴇᴅ ᴀᴅᴍɪɴꜱ`
 » `/fdemote <user>`*:* ᴅʀᴏᴘꜱ ᴛʜᴇ ᴜꜱᴇʀ ꜰʀᴏᴍ ᴛʜᴇ ᴀᴅᴍɪɴ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴛᴏ ᴀ ɴᴏʀᴍᴀʟ ᴜꜱᴇʀ
 » `/subfed <fed_id>`*:* ꜱᴜʙꜱᴄʀɪʙᴇꜱ ᴛᴏ ᴀ ɢɪᴠᴇɴ ꜰᴇᴅ ɪᴅ, ʙᴀɴꜱ ꜰʀᴏᴍ ᴛʜᴀᴛ ꜱᴜʙꜱᴄʀɪʙᴇᴅ ꜰᴇᴅ ᴡɪʟʟ ᴀʟꜱᴏ ʜᴀᴘᴘᴇɴ ɪɴ ʏᴏᴜʀ ꜰᴇᴅ
 » `/unsubfed <fed_id>`*:* ᴜɴꜱᴜʙꜱᴄʀɪʙᴇꜱ ᴛᴏ ᴀ ɢɪᴠᴇɴ ꜰᴇᴅ ɪᴅ
 » `/setfedlog <fed_id>`*:* ꜱᴇᴛꜱ ᴛʜᴇ ɢʀᴏᴜᴘ ᴀꜱ ᴀ ꜰᴇᴅ ʟᴏɢ ʀᴇᴘᴏʀᴛ ʙᴀꜱᴇ ꜰᴏʀ ᴛʜᴇ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ
 » `/unsetfedlog <fed_id>`*:* ʀᴇᴍᴏᴠᴇᴅ ᴛʜᴇ ɢʀᴏᴜᴘ ᴀꜱ ᴀ ꜰᴇᴅ ʟᴏɢ ʀᴇᴘᴏʀᴛ ʙᴀꜱᴇ ꜰᴏʀ ᴛʜᴇ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ
 » `/fbroadcast <message>`*:* ʙʀᴏᴀᴅᴄᴀꜱᴛꜱ ᴀ ᴍᴇꜱꜱᴀɢᴇꜱ ᴛᴏ ᴀʟʟ ɢʀᴏᴜᴘꜱ ᴛʜᴀᴛ ʜᴀᴠᴇ ᴊᴏɪɴᴇᴅ ʏᴏᴜʀ ꜰᴇᴅ
 » `/fedsubs`*:* ꜱʜᴏᴡꜱ ᴛʜᴇ ꜰᴇᴅꜱ ʏᴏᴜʀ ɢʀᴏᴜᴘ ɪꜱ ꜱᴜʙꜱᴄʀɪʙᴇᴅ ᴛᴏ `(ʙʀᴏᴋᴇɴ ʀɴ)`""",
        parse_mode=ParseMode.MARKDOWN,
    )


def fed_admin_help(update: Update, context: CallbackContext):
    update.effective_message.reply_text(
        """*🔱 Fed Admins:*
 » `/fban <user> <reason>`*:* ꜰᴇᴅ ʙᴀɴꜱ ᴀ ᴜꜱᴇʀ
 » `/unfban <user> <reason>`*:* ʀᴇᴍᴏᴠᴇꜱ ᴀ ᴜꜱᴇʀ ꜰʀᴏᴍ ᴀ ꜰᴇᴅ ʙᴀɴ
 » `/fedinfo <fed_id>`*:* ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴛʜᴇ ꜱᴘᴇᴄɪꜰɪᴇᴅ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ
 » `/joinfed <fed_id>`*:* ᴊᴏɪɴ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴄʜᴀᴛ ᴛᴏ ᴛʜᴇ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ. ᴏɴʟʏ ᴄʜᴀᴛ ᴏᴡɴᴇʀꜱ can do this. Every chat can only be in one Federation
 » `/leavefed <fed_id>`*:* ʟᴇᴀᴠᴇ ᴛʜᴇ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ɢɪᴠᴇɴ. ᴏɴʟʏ ᴄʜᴀᴛ ᴏᴡɴᴇʀꜱ ᴄᴀɴ ᴅᴏ ᴛʜɪꜱ
 » `/setfrules <rules>`*:* ᴀʀʀᴀɴɢᴇ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ʀᴜʟᴇꜱ
 » `/fedadmins`*:* ꜱʜᴏᴡ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴀᴅᴍɪɴ
 » `/fbanlist`*:* ᴅɪꜱᴘʟᴀʏꜱ ᴀʟʟ ᴜꜱᴇʀꜱ ᴡʜᴏ ᴀʀᴇ ᴠɪᴄᴛɪᴍɪᴢᴇᴅ ᴀᴛ ᴛʜᴇ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴀᴛ ᴛʜɪꜱ ᴛɪᴍᴇ
 » `/fedchats`*:* ɢᴇᴛ ᴀʟʟ ᴛʜᴇ ᴄʜᴀᴛꜱ ᴛʜᴀᴛ ᴀʀᴇ ᴄᴏɴɴᴇᴄᴛᴇᴅ ɪɴ ᴛʜᴇ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ
 » `/chatfed `*:* ꜱᴇᴇ ᴛʜᴇ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ɪɴ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴄʜᴀᴛ\n""",
        parse_mode=ParseMode.MARKDOWN,
    )


def fed_user_help(update: Update, context: CallbackContext):
    update.effective_message.reply_text(
        """*🎩 Any ᴜꜱᴇʀ:*

» /fbanstat*:* ꜱʜᴏᴡꜱ ɪꜰ ʏᴏᴜ/ᴏʀ ᴛʜᴇ ᴜꜱᴇʀ ʏᴏᴜ ᴀʀᴇ ʀᴇᴘʟʏɪɴɢ ᴛᴏ ᴏʀ ᴛʜᴇɪʀ ᴜꜱᴇʀɴᴀᴍᴇ ɪꜱ ꜰʙᴀɴɴᴇᴅ ꜱᴏᴍᴇᴡʜᴇʀᴇ ᴏʀ ɴᴏᴛ
» /fednotif <on/off>*:* ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ꜱᴇᴛᴛɪɴɢꜱ ɴᴏᴛ ɪɴ ᴘᴍ ᴡʜᴇɴ ᴛʜᴇʀᴇ ᴀʀᴇ ᴜꜱᴇʀꜱ ᴡʜᴏ ᴀʀᴇ ꜰʙᴀɴᴇᴅ/ᴜɴꜰʙᴀɴᴇᴅ
» /frules*:* ꜱᴇᴇ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ʀᴇɢᴜʟᴀᴛɪᴏɴꜱ\n""",
        parse_mode=ParseMode.MARKDOWN,
    )


__mod_name__ = "FEDRATIONS"


NEW_FED_HANDLER = CommandHandler("newfed", new_fed, run_async=True)
DEL_FED_HANDLER = CommandHandler("delfed", del_fed, run_async=True)
RENAME_FED = CommandHandler("renamefed", rename_fed, run_async=True)
JOIN_FED_HANDLER = CommandHandler("joinfed", join_fed, run_async=True)
LEAVE_FED_HANDLER = CommandHandler("leavefed", leave_fed, run_async=True)
PROMOTE_FED_HANDLER = CommandHandler("fpromote", user_join_fed, run_async=True)
DEMOTE_FED_HANDLER = CommandHandler("fdemote", user_demote_fed, run_async=True)
INFO_FED_HANDLER = CommandHandler("fedinfo", fed_info, run_async=True)
BAN_FED_HANDLER = DisableAbleCommandHandler("fban", fed_ban, run_async=True)
UN_BAN_FED_HANDLER = CommandHandler("unfban", unfban, run_async=True)
FED_BROADCAST_HANDLER = CommandHandler("fbroadcast", fed_broadcast, run_async=True)
FED_SET_RULES_HANDLER = CommandHandler("setfrules", set_frules, run_async=True)
FED_GET_RULES_HANDLER = CommandHandler("frules", get_frules, run_async=True)
FED_CHAT_HANDLER = CommandHandler("chatfed", fed_chat, run_async=True)
FED_ADMIN_HANDLER = CommandHandler("fedadmins", fed_admin, run_async=True)
FED_USERBAN_HANDLER = CommandHandler("fbanlist", fed_ban_list, run_async=True)
FED_NOTIF_HANDLER = CommandHandler("fednotif", fed_notif, run_async=True)
FED_CHATLIST_HANDLER = CommandHandler("fedchats", fed_chats, run_async=True)
FED_IMPORTBAN_HANDLER = CommandHandler("importfbans", fed_import_bans, run_async=True)
FEDSTAT_USER = DisableAbleCommandHandler(
    ["fedstat", "fbanstat"], fed_stat_user, run_async=True
)
SET_FED_LOG = CommandHandler("setfedlog", set_fed_log, run_async=True)
UNSET_FED_LOG = CommandHandler("unsetfedlog", unset_fed_log, run_async=True)
SUBS_FED = CommandHandler("subfed", subs_feds, run_async=True)
UNSUBS_FED = CommandHandler("unsubfed", unsubs_feds, run_async=True)
MY_SUB_FED = CommandHandler("fedsubs", get_myfedsubs, run_async=True)
MY_FEDS_LIST = CommandHandler("myfeds", get_myfeds_list, run_async=True)
DELETEBTN_FED_HANDLER = CallbackQueryHandler(
    del_fed_button, pattern=r"rmfed_", run_async=True
)
FED_OWNER_HELP_HANDLER = CommandHandler("fedownerhelp", fed_owner_help, run_async=True)
FED_ADMIN_HELP_HANDLER = CommandHandler("fedadminhelp", fed_admin_help, run_async=True)
FED_USER_HELP_HANDLER = CommandHandler("feduserhelp", fed_user_help, run_async=True)

dispatcher.add_handler(NEW_FED_HANDLER)
dispatcher.add_handler(DEL_FED_HANDLER)
dispatcher.add_handler(RENAME_FED)
dispatcher.add_handler(JOIN_FED_HANDLER)
dispatcher.add_handler(LEAVE_FED_HANDLER)
dispatcher.add_handler(PROMOTE_FED_HANDLER)
dispatcher.add_handler(DEMOTE_FED_HANDLER)
dispatcher.add_handler(INFO_FED_HANDLER)
dispatcher.add_handler(BAN_FED_HANDLER)
dispatcher.add_handler(UN_BAN_FED_HANDLER)
dispatcher.add_handler(FED_BROADCAST_HANDLER)
dispatcher.add_handler(FED_SET_RULES_HANDLER)
dispatcher.add_handler(FED_GET_RULES_HANDLER)
dispatcher.add_handler(FED_CHAT_HANDLER)
dispatcher.add_handler(FED_ADMIN_HANDLER)
dispatcher.add_handler(FED_USERBAN_HANDLER)
dispatcher.add_handler(FED_NOTIF_HANDLER)
dispatcher.add_handler(FED_CHATLIST_HANDLER)
# dispatcher.add_handler(FED_IMPORTBAN_HANDLER)
dispatcher.add_handler(FEDSTAT_USER)
dispatcher.add_handler(SET_FED_LOG)
dispatcher.add_handler(UNSET_FED_LOG)
dispatcher.add_handler(SUBS_FED)
dispatcher.add_handler(UNSUBS_FED)
dispatcher.add_handler(MY_SUB_FED)
dispatcher.add_handler(MY_FEDS_LIST)
dispatcher.add_handler(DELETEBTN_FED_HANDLER)
dispatcher.add_handler(FED_OWNER_HELP_HANDLER)
dispatcher.add_handler(FED_ADMIN_HELP_HANDLER)
dispatcher.add_handler(FED_USER_HELP_HANDLER)
