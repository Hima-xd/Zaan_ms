import KRISTY.modules.sql.locks_sql as sql
import html
import ast

from telegram import Message, Chat, ParseMode, MessageEntity
from telegram import TelegramError, ChatPermissions
from telegram.error import BadRequest
from telegram.ext import CommandHandler, MessageHandler, Filters
from telegram.ext.dispatcher import run_async
from telegram.utils.helpers import mention_html
from alphabet_detector import AlphabetDetector
from KRISTY import dispatcher, DRAGONS, LOGGER
from KRISTY.modules.disable import DisableAbleCommandHandler
from KRISTY.modules.helper_funcs.chat_status import (
    can_delete,
    is_user_admin,
    user_not_admin,
    is_bot_admin,
    user_admin,
)
from KRISTY.modules.sql.approve_sql import is_approved
from KRISTY.modules.log_channel import loggable
from KRISTY.modules.connection import connected
from KRISTY.modules.helper_funcs.alternate import send_message, typing_action

ad = AlphabetDetector()

LOCK_TYPES = {
    "audio": Filters.audio,
    "voice": Filters.voice,
    "document": Filters.document,
    "video": Filters.video,
    "contact": Filters.contact,
    "photo": Filters.photo,
    "url": Filters.entity(MessageEntity.URL)
    | Filters.caption_entity(MessageEntity.URL),
    "bots": Filters.status_update.new_chat_members,
    "forward": Filters.forwarded,
    "game": Filters.game,
    "location": Filters.location,
    "egame": Filters.dice,
    "rtl": "rtl",
    "button": "button",
    "inline": "inline",
}

LOCK_CHAT_RESTRICTION = {
    "all": {
        "can_send_messages": False,
        "can_send_media_messages": False,
        "can_send_polls": False,
        "can_send_other_messages": False,
        "can_add_web_page_previews": False,
        "can_change_info": False,
        "can_invite_users": False,
        "can_pin_messages": False,
    },
    "messages": {"can_send_messages": False},
    "media": {"can_send_media_messages": False},
    "sticker": {"can_send_other_messages": False},
    "gif": {"can_send_other_messages": False},
    "poll": {"can_send_polls": False},
    "other": {"can_send_other_messages": False},
    "previews": {"can_add_web_page_previews": False},
    "info": {"can_change_info": False},
    "invite": {"can_invite_users": False},
    "pin": {"can_pin_messages": False},
}

UNLOCK_CHAT_RESTRICTION = {
    "all": {
        "can_send_messages": True,
        "can_send_media_messages": True,
        "can_send_polls": True,
        "can_send_other_messages": True,
        "can_add_web_page_previews": True,
        "can_invite_users": True,
    },
    "messages": {"can_send_messages": True},
    "media": {"can_send_media_messages": True},
    "sticker": {"can_send_other_messages": True},
    "gif": {"can_send_other_messages": True},
    "poll": {"can_send_polls": True},
    "other": {"can_send_other_messages": True},
    "previews": {"can_add_web_page_previews": True},
    "info": {"can_change_info": True},
    "invite": {"can_invite_users": True},
    "pin": {"can_pin_messages": True},
}

PERM_GROUP = 1
REST_GROUP = 2


# NOT ASYNC
def restr_members(
    bot, chat_id, members, messages=False, media=False, other=False, previews=False
):
    for mem in members:
        try:
            bot.restrict_chat_member(
                chat_id,
                mem.user,
                can_send_messages=messages,
                can_send_media_messages=media,
                can_send_other_messages=other,
                can_add_web_page_previews=previews,
            )
        except TelegramError:
            pass


# NOT ASYNC
def unrestr_members(
    bot, chat_id, members, messages=True, media=True, other=True, previews=True
):
    for mem in members:
        try:
            bot.restrict_chat_member(
                chat_id,
                mem.user,
                can_send_messages=messages,
                can_send_media_messages=media,
                can_send_other_messages=other,
                can_add_web_page_previews=previews,
            )
        except TelegramError:
            pass


def locktypes(update, context):
    update.effective_message.reply_text(
        "\n » ".join(
            ["ʟᴏᴄᴋꜱ ᴀᴠᴀɪʟᴀʙʟᴇ: "]
            + sorted(list(LOCK_TYPES) + list(LOCK_CHAT_RESTRICTION))
        )
    )


@user_admin
@loggable
@typing_action
def lock(update, context) -> str:
    args = context.args
    chat = update.effective_chat
    user = update.effective_user

    if (
        can_delete(chat, context.bot.id)
        or update.effective_message.chat.type == "private"
    ):
        if len(args) >= 1:
            ltype = args[0].lower()
            if ltype in LOCK_TYPES:
                # Connection check
                conn = connected(context.bot, update, chat, user.id, need_admin=True)
                if conn:
                    chat = dispatcher.bot.getChat(conn)
                    chat_id = conn
                    chat_name = chat.title
                    text = "ʟᴏᴄᴋᴇᴅ {} ꜰᴏʀ ɴᴏɴ-ᴀᴅᴍɪɴꜱ ɪɴ {} ʙᴀʙʏ🥀!".format(ltype, chat_name)
                else:
                    if update.effective_message.chat.type == "private":
                        send_message(
                            update.effective_message,
                            "ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪꜱ ᴍᴇᴀɴᴛ ᴛᴏ ᴜꜱᴇ ɪɴ ɢʀᴏᴜᴘ ɴᴏᴛ ɪɴ ᴘᴍ ʙᴀʙʏ🥀",
                        )
                        return ""
                    chat = update.effective_chat
                    chat_id = update.effective_chat.id
                    chat_name = update.effective_message.chat.title
                    text = "ʟᴏᴄᴋᴇᴅ {} ꜰᴏʀ ɴᴏɴ-ᴀᴅᴍɪɴꜱ!".format(ltype)
                sql.update_lock(chat.id, ltype, locked=True)
                send_message(update.effective_message, text, parse_mode="markdown")

                return (
                    "<b>{}:</b>"
                    "\n#ʟᴏᴄᴋ"
                    "\n<b>ᴀᴅᴍɪɴ:</b> {}"
                    "\nʟᴏᴄᴋᴇᴅ <code>{}</code>.".format(
                        html.escape(chat.title),
                        mention_html(user.id, user.first_name),
                        ltype,
                    )
                )

            if ltype in LOCK_CHAT_RESTRICTION:
                # Connection check
                conn = connected(context.bot, update, chat, user.id, need_admin=True)
                if conn:
                    chat = dispatcher.bot.getChat(conn)
                    chat_id = conn
                    chat_name = chat.title
                    text = "ʟᴏᴄᴋᴇᴅ {} ꜰᴏʀ ᴀʟʟ ɴᴏɴ-ᴀᴅᴍɪɴꜱ ɪɴ {} ʙᴀʙʏ🥀!".format(
                        ltype, chat_name
                    )
                else:
                    if update.effective_message.chat.type == "private":
                        send_message(
                            update.effective_message,
                            "ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪꜱ ᴍᴇᴀɴᴛ ᴛᴏ ᴜꜱᴇ ɪɴ ɢʀᴏᴜᴘ ɴᴏᴛ ɪɴ ᴘᴍ ʙᴀʙʏ🥀",
                        )
                        return ""
                    chat = update.effective_chat
                    chat_id = update.effective_chat.id
                    chat_name = update.effective_message.chat.title
                    text = "ʟᴏᴄᴋᴇᴅ {} ꜰᴏʀ ᴀʟʟ ɴᴏɴ-ᴀᴅᴍɪɴꜱ ʙᴀʙʏ🥀!".format(ltype)

                current_permission = context.bot.getChat(chat_id).permissions
                context.bot.set_chat_permissions(
                    chat_id=chat_id,
                    permissions=get_permission_list(
                        ast.literal_eval(str(current_permission)),
                        LOCK_CHAT_RESTRICTION[ltype.lower()],
                    ),
                )

                send_message(update.effective_message, text, parse_mode="markdown")
                return (
                    "<b>{}:</b>"
                    "\n#ᴘᴇʀᴍɪꜱꜱɪᴏɴ_ʟᴏᴄᴋ"
                    "\n<b>ᴀᴅᴍɪɴ:</b> {}"
                    "\nʟᴏᴄᴋᴇᴅ <code>{}</code>.".format(
                        html.escape(chat.title),
                        mention_html(user.id, user.first_name),
                        ltype,
                    )
                )
            send_message(
                update.effective_message,
                "ᴡʜᴀᴛ ᴀʀᴇ ʏᴏᴜ ᴛʀʏɪɴɢ ᴛᴏ ʟᴏᴄᴋ...? ᴛʀʏ /locktypes ꜰᴏʀ ᴛʜᴇ ʟɪꜱᴛ ᴏꜰ ʟᴏᴄᴋᴀʙʟᴇꜱ ʙᴀʙʏ🥀",
            )
        else:
            send_message(update.effective_message, "ᴡʜᴀᴛ ᴀʀᴇ ʏᴏᴜ ᴛʀʏɪɴɢ ᴛᴏ ʟᴏᴄᴋ ʙᴀʙʏ🥀...?")

    else:
        send_message(
            update.effective_message,
            "ɪ ᴀᴍ ɴᴏᴛ ᴀᴅᴍɪɴ ᴏʀ ʜᴀᴠᴇɴ'ᴛ ɢᴏᴛ ᴇɴᴏᴜɢʜ ʀɪɢʜᴛꜱ ʙᴀʙʏ🥀.",
        )

    return ""


@user_admin
@loggable
@typing_action
def unlock(update, context) -> str:
    args = context.args
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message
    if is_user_admin(chat, message.from_user.id):
        if len(args) >= 1:
            ltype = args[0].lower()
            if ltype in LOCK_TYPES:
                # Connection check
                conn = connected(context.bot, update, chat, user.id, need_admin=True)
                if conn:
                    chat = dispatcher.bot.getChat(conn)
                    chat_id = conn
                    chat_name = chat.title
                    text = "ᴜɴʟᴏᴄᴋᴇᴅ {} ꜰᴏʀ ᴇᴠᴇʀʏᴏɴᴇ ɪɴ {} ʙᴀʙʏ🥀!".format(ltype, chat_name)
                else:
                    if update.effective_message.chat.type == "private":
                        send_message(
                            update.effective_message,
                            "ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪꜱ ᴍᴇᴀɴᴛ ᴛᴏ ᴜꜱᴇ ɪɴ ɢʀᴏᴜᴘ ɴᴏᴛ ɪɴ ᴘᴍ ʙᴀʙʏ🥀",
                        )
                        return ""
                    chat = update.effective_chat
                    chat_id = update.effective_chat.id
                    chat_name = update.effective_message.chat.title
                    text = "ᴜɴʟᴏᴄᴋᴇᴅ {} ꜰᴏʀ ᴇᴠᴇʀʏᴏɴᴇ ʙᴀʙʏ🥀!".format(ltype)
                sql.update_lock(chat.id, ltype, locked=False)
                send_message(update.effective_message, text, parse_mode="markdown")
                return (
                    "<b>{}:</b>"
                    "\n#UNLOCK"
                    "\n<b>ᴀᴅᴍɪɴ:</b> {}"
                    "\nᴜɴʟᴏᴄᴋᴇᴅ <code>{}</code>.".format(
                        html.escape(chat.title),
                        mention_html(user.id, user.first_name),
                        ltype,
                    )
                )

            if ltype in UNLOCK_CHAT_RESTRICTION:
                # Connection check
                conn = connected(context.bot, update, chat, user.id, need_admin=True)
                if conn:
                    chat = dispatcher.bot.getChat(conn)
                    chat_id = conn
                    chat_name = chat.title
                    text = "ᴜɴʟᴏᴄᴋᴇᴅ {} ꜰᴏʀ ᴇᴠᴇʀʏᴏɴᴇ ɪɴ {} ʙᴀʙʏ🥀!".format(ltype, chat_name)
                else:
                    if update.effective_message.chat.type == "private":
                        send_message(
                            update.effective_message,
                            "ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪꜱ ᴍᴇᴀɴᴛ ᴛᴏ ᴜꜱᴇ ɪɴ ɢʀᴏᴜᴘ ɴᴏᴛ ɪɴ ᴘᴍ ʙᴀʙʏ🥀",
                        )
                        return ""
                    chat = update.effective_chat
                    chat_id = update.effective_chat.id
                    chat_name = update.effective_message.chat.title
                    text = "ᴜɴʟᴏᴄᴋᴇᴅ {} ꜰᴏʀ ᴇᴠᴇʀʏᴏɴᴇ ʙᴀʙʏ🥀!".format(ltype)

                current_permission = context.bot.getChat(chat_id).permissions
                context.bot.set_chat_permissions(
                    chat_id=chat_id,
                    permissions=get_permission_list(
                        ast.literal_eval(str(current_permission)),
                        UNLOCK_CHAT_RESTRICTION[ltype.lower()],
                    ),
                )

                send_message(update.effective_message, text, parse_mode="markdown")

                return (
                    "<b>{}:</b>"
                    "\n#ᴜɴʟᴏᴄᴋ"
                    "\n<b>ᴀᴅᴍɪɴ:</b> {}"
                    "\nᴜɴʟᴏᴄᴋᴇᴅ <code>{}</code>.".format(
                        html.escape(chat.title),
                        mention_html(user.id, user.first_name),
                        ltype,
                    )
                )
            send_message(
                update.effective_message,
                "ᴡʜᴀᴛ ᴀʀᴇ ʏᴏᴜ ᴛʀʏɪɴɢ ᴛᴏ ᴜɴʟᴏᴄᴋ...? ᴛʀʏ /locktypes ꜰᴏʀ ᴛʜᴇ ʟɪꜱᴛ ᴏꜰ ʟᴏᴄᴋᴀʙʟᴇꜱ ʙᴀʙʏ🥀.",
            )

        else:
            send_message(update.effective_message, "ᴡʜᴀᴛ ᴀʀᴇ ʏᴏᴜ ᴛʀʏɪɴɢ ᴛᴏ ᴜɴʟᴏᴄᴋ ʙᴀʙʏ🥀...?")

    return ""


@user_not_admin
def del_lockables(update, context):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user
    message = update.effective_message  # type: Optional[Message]
    if is_approved(chat.id, user.id):
        return
    for lockable, filter in LOCK_TYPES.items():
        if lockable == "rtl":
            if sql.is_locked(chat.id, lockable) and can_delete(chat, context.bot.id):
                if message.caption:
                    check = ad.detect_alphabet("{}".format(message.caption))
                    if "ARABIC" in check:
                        try:
                            message.delete()
                        except BadRequest as excp:
                            if excp.message != "Message to delete not found":
                                LOGGER.exception("ERROR in lockables")
                        break
                if message.text:
                    check = ad.detect_alphabet("{}".format(message.text))
                    if "ARABIC" in check:
                        try:
                            message.delete()
                        except BadRequest as excp:
                            if excp.message != "Message to delete not found":
                                LOGGER.exception("ERROR in lockables")
                        break
            continue
        if lockable == "button":
            if (
                sql.is_locked(chat.id, lockable)
                and can_delete(chat, context.bot.id)
                and message.reply_markup
                and message.reply_markup.inline_keyboard
            ):
                try:
                    message.delete()
                except BadRequest as excp:
                    if excp.message != "Message to delete not found":
                        LOGGER.exception("ERROR in lockables")
                break
            continue
        if lockable == "inline":
            if (
                sql.is_locked(chat.id, lockable)
                and can_delete(chat, context.bot.id)
                and message
                and message.via_bot
            ):
                try:
                    message.delete()
                except BadRequest as excp:
                    if excp.message != "Message to delete not found":
                        LOGGER.exception("ERROR in lockables")
                break
            continue
        if (
            filter(update)
            and sql.is_locked(chat.id, lockable)
            and can_delete(chat, context.bot.id)
        ):
            if lockable == "bots":
                new_members = update.effective_message.new_chat_members
                for new_mem in new_members:
                    if new_mem.is_bot:
                        if not is_bot_admin(chat, context.bot.id):
                            send_message(
                                update.effective_message,
                                "ɪ ꜱᴇᴇ ᴀ ʙᴏᴛ ᴀɴᴅ ɪ'ᴠᴇ ʙᴇᴇɴ ᴛᴏʟᴅ ᴛᴏ ꜱᴛᴏᴘ ᴛʜᴇᴍ ꜰʀᴏᴍ ᴊᴏɪɴɪɴɢ ʙᴀʙʏ🥀..."  
                                "ʙᴜᴛ ɪ'ᴍ ɴᴏᴛ ᴀᴅᴍɪɴ!",
                            )
                            return

                        chat.ban_member(new_mem.id)
                        send_message(
                            update.effective_message,
                            "ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴀʀᴇ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴀᴅᴅ ʙᴏᴛꜱ ɪɴ ᴛʜɪꜱ ᴄʜᴀᴛ! ɢᴇᴛ ᴏᴜᴛᴛᴀ ʜᴇʀᴇ ʙᴀʙʏ🥀.",
                        )
                        break
            else:
                try:
                    message.delete()
                except BadRequest as excp:
                    if excp.message != "Message to delete not found":
                        LOGGER.exception("ERROR in lockables")

                break


def build_lock_message(chat_id):
    locks = sql.get_locks(chat_id)
    res = ""
    locklist = []
    permslist = []
    if locks:
        res += "*" + "These are the current locks in this Chat:" + "*"
        locklist.append("sticker = `{}`".format(locks.sticker))
        locklist.append("audio = `{}`".format(locks.audio))
        locklist.append("voice = `{}`".format(locks.voice))
        locklist.append("document = `{}`".format(locks.document))
        locklist.append("video = `{}`".format(locks.video))
        locklist.append("contact = `{}`".format(locks.contact))
        locklist.append("photo = `{}`".format(locks.photo))
        locklist.append("gif = `{}`".format(locks.gif))
        locklist.append("url = `{}`".format(locks.url))
        locklist.append("bots = `{}`".format(locks.bots))
        locklist.append("forward = `{}`".format(locks.forward))
        locklist.append("game = `{}`".format(locks.game))
        locklist.append("location = `{}`".format(locks.location))
        locklist.append("rtl = `{}`".format(locks.rtl))
        locklist.append("button = `{}`".format(locks.button))
        locklist.append("egame = `{}`".format(locks.egame))
        locklist.append("inline = `{}`".format(locks.inline))
    permissions = dispatcher.bot.get_chat(chat_id).permissions
    permslist.append("messages = `{}`".format(permissions.can_send_messages))
    permslist.append("media = `{}`".format(permissions.can_send_media_messages))
    permslist.append("poll = `{}`".format(permissions.can_send_polls))
    permslist.append("other = `{}`".format(permissions.can_send_other_messages))
    permslist.append("previews = `{}`".format(permissions.can_add_web_page_previews))
    permslist.append("info = `{}`".format(permissions.can_change_info))
    permslist.append("invite = `{}`".format(permissions.can_invite_users))
    permslist.append("pin = `{}`".format(permissions.can_pin_messages))

    if locklist:
        # Ordering lock list
        locklist.sort()
        # Building lock list string
        for x in locklist:
            res += "\n × {}".format(x)
    res += "\n\n*" + "ᴛʜᴇꜱᴇ ᴀʀᴇ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴄʜᴀᴛ ᴘᴇʀᴍɪꜱꜱɪᴏɴꜱ ʙᴀʙʏ🥀:" + "*"
    for x in permslist:
        res += "\n × {}".format(x)
    return res


@user_admin
@typing_action
def list_locks(update, context):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user

    # Connection check
    conn = connected(context.bot, update, chat, user.id, need_admin=True)
    if conn:
        chat = dispatcher.bot.getChat(conn)
        chat_name = chat.title
    else:
        if update.effective_message.chat.type == "private":
            send_message(
                update.effective_message,
                "ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪꜱ ᴍᴇᴀɴᴛ ᴛᴏ ᴜꜱᴇ ɪɴ ɢʀᴏᴜᴘ ɴᴏᴛ ɪɴ ᴘᴍ ʙᴀʙʏ🥀",
            )
            return ""
        chat = update.effective_chat
        chat_name = update.effective_message.chat.title

    res = build_lock_message(chat.id)
    if conn:
        res = res.replace("Locks in", "*{}*".format(chat_name))

    send_message(update.effective_message, res, parse_mode=ParseMode.MARKDOWN)


def get_permission_list(current, new):
    permissions = {
        "can_send_messages": None,
        "can_send_media_messages": None,
        "can_send_polls": None,
        "can_send_other_messages": None,
        "can_add_web_page_previews": None,
        "can_change_info": None,
        "can_invite_users": None,
        "can_pin_messages": None,
    }
    permissions.update(current)
    permissions.update(new)
    return ChatPermissions(**permissions)


def __import_data__(chat_id, data):
    # set chat locks
    locks = data.get("locks", {})
    for itemlock in locks:
        if itemlock in LOCK_TYPES:
            sql.update_lock(chat_id, itemlock, locked=True)
        elif itemlock in LOCK_CHAT_RESTRICTION:
            sql.update_restriction(chat_id, itemlock, locked=True)


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)


def __chat_settings__(chat_id, user_id):
    return build_lock_message(chat_id)


__help__ = """

ᴅᴏ ꜱᴛɪᴄᴋᴇʀꜱ ᴀɴɴᴏʏ ʏᴏᴜ? ᴏʀ ᴡᴀɴᴛ ᴛᴏ ᴀᴠᴏɪᴅ ᴘᴇᴏᴘʟᴇ ꜱʜᴀʀɪɴɢ ʟɪɴᴋꜱ? ᴏʀ ᴘɪᴄᴛᴜʀᴇꜱ? \
ʏᴏᴜ'ʀᴇ ɪɴ ᴛʜᴇ ʀɪɢʜᴛ ᴘʟᴀᴄᴇ!
ᴛʜᴇ ʟᴏᴄᴋꜱ ᴍᴏᴅᴜʟᴇ ᴀʟʟᴏᴡꜱ ʏᴏᴜ ᴛᴏ ʟᴏᴄᴋ ᴀᴡᴀʏ ꜱᴏᴍᴇ ᴄᴏᴍᴍᴏɴ ɪᴛᴇᴍꜱ ɪɴ ᴛʜᴇ \
ᴛᴇʟᴇɢʀᴀᴍ ᴡᴏʀʟᴅ; ᴛʜᴇ ʙᴏᴛ ᴡɪʟʟ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴅᴇʟᴇᴛᴇ ᴛʜᴇᴍ!

» `/locktypes`*:* ʟɪꜱᴛꜱ ᴀʟʟ ᴘᴏꜱꜱɪʙʟᴇ ʟᴏᴄᴋᴛʏᴘᴇꜱ

*ᴀᴅᴍɪɴꜱ ᴏɴʟʏ:*
» `/lock` <ᴛʏᴘᴇ>*:* ʟᴏᴄᴋ ɪᴛᴇᴍꜱ ᴏꜰ ᴀ ᴄᴇʀᴛᴀɪɴ ᴛʏᴘᴇ (ɴᴏᴛ ᴀᴠᴀɪʟᴀʙʟᴇ ɪɴ ᴘʀɪᴠᴀᴛᴇ)
» `/unlock` <ᴛʏᴘᴇ>*:* ᴜɴʟᴏᴄᴋ ɪᴛᴇᴍꜱ ᴏꜰ ᴀ ᴄᴇʀᴛᴀɪɴ ᴛʏᴘᴇ (ɴᴏᴛ ᴀᴠᴀɪʟᴀʙʟᴇ ɪɴ ᴘʀɪᴠᴀᴛᴇ)
» `/locks`*:* ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ʟɪꜱᴛ ᴏꜰ ʟᴏᴄᴋꜱ ɪɴ ᴛʜɪꜱ ᴄʜᴀᴛ.

ʟᴏᴄᴋꜱ ᴄᴀɴ ʙᴇ ᴜꜱᴇᴅ ᴛᴏ ʀᴇꜱᴛʀɪᴄᴛ ᴀ ɢʀᴏᴜᴘ'ꜱ ᴜꜱᴇʀꜱ.
ᴇɢ:
ʟᴏᴄᴋɪɴɢ ᴜʀʟꜱ ᴡɪʟʟ ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ ᴀʟʟ ᴍᴇꜱꜱᴀɢᴇꜱ ᴡɪᴛʜ ᴜʀʟꜱ, ʟᴏᴄᴋɪɴɢ ꜱᴛɪᴄᴋᴇʀꜱ ᴡɪʟʟ ʀᴇꜱᴛʀɪᴄᴛ ᴀʟʟ \
ɴᴏɴ-ᴀᴅᴍɪɴ ᴜꜱᴇʀꜱ ꜰʀᴏᴍ ꜱᴇɴᴅɪɴɢ ꜱᴛɪᴄᴋᴇʀꜱ, ᴇᴛᴄ.
ʟᴏᴄᴋɪɴɢ ʙᴏᴛꜱ ᴡɪʟʟ ꜱᴛᴏᴘ ɴᴏɴ-ᴀᴅᴍɪɴꜱ ꜰʀᴏᴍ ᴀᴅᴅɪɴɢ ʙᴏᴛꜱ ᴛᴏ ᴛʜᴇ ᴄʜᴀᴛ.


*ɴᴏᴛᴇ:*
» ᴜɴʟᴏᴄᴋɪɴɢ ᴘᴇʀᴍɪꜱꜱɪᴏɴ *ɪɴꜰᴏ* ᴡɪʟʟ ᴀʟʟᴏᴡ ᴍᴇᴍʙᴇʀꜱ (ɴᴏɴ-ᴀᴅᴍɪɴꜱ) ᴛᴏ ᴄʜᴀɴɢᴇ ᴛʜᴇ ɢʀᴏᴜᴘ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ, ꜱᴜᴄʜ ᴀꜱ ᴛʜᴇ ᴅᴇꜱᴄʀɪᴘᴛɪᴏɴ ᴏʀ ᴛʜᴇ ɢʀᴏᴜᴘ ɴᴀᴍᴇ
» ᴜɴʟᴏᴄᴋɪɴɢ ᴘᴇʀᴍɪꜱꜱɪᴏɴ *ᴘɪɴ* ᴡɪʟʟ ᴀʟʟᴏᴡ ᴍᴇᴍʙᴇʀꜱ (ɴᴏɴ-ᴀᴅᴍɪɴꜱ) ᴛᴏ ᴘɪɴɴᴇᴅ ᴀ ᴍᴇꜱꜱᴀɢᴇ ɪɴ ᴀ ɢʀᴏᴜᴘ

"""

__mod_name__ = "LOCKS"

LOCKTYPES_HANDLER = DisableAbleCommandHandler("locktypes", locktypes, run_async=True)
LOCK_HANDLER = CommandHandler(
    "lock", lock, pass_args=True, run_async=True
)  # , filters=Filters.chat_type.groups)
UNLOCK_HANDLER = CommandHandler(
    "unlock", unlock, pass_args=True, run_async=True
)  # , filters=Filters.chat_type.groups)
LOCKED_HANDLER = CommandHandler(
    "locks", list_locks, run_async=True
)  # , filters=Filters.chat_type.groups)

dispatcher.add_handler(LOCK_HANDLER)
dispatcher.add_handler(UNLOCK_HANDLER)
dispatcher.add_handler(LOCKTYPES_HANDLER)
dispatcher.add_handler(LOCKED_HANDLER)

dispatcher.add_handler(
    MessageHandler(
        Filters.all & Filters.chat_type.groups, del_lockables, run_async=True
    ),
    PERM_GROUP,
)
