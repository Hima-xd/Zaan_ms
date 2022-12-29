import time
import re

from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton, Update, Bot
from telegram.error import BadRequest, Unauthorized
from telegram.ext import CommandHandler, CallbackQueryHandler

import KRISTY.modules.sql.connection_sql as sql
from KRISTY import dispatcher, DRAGONS, DEV_USERS
from KRISTY.modules.helper_funcs import chat_status
from KRISTY.modules.helper_funcs.alternate import send_message, typing_action

user_admin = chat_status.user_admin


@user_admin
@typing_action
def allow_connections(update, context) -> str:

    chat = update.effective_chat
    args = context.args

    if chat.type != chat.PRIVATE:
        if len(args) >= 1:
            var = args[0]
            if var == "no":
                sql.set_allow_connect_to_chat(chat.id, False)
                send_message(
                    update.effective_message,
                    "ᴄᴏɴɴᴇᴄᴛɪᴏɴ ʜᴀꜱ ʙᴇᴇɴ ᴅɪꜱᴀʙʟᴇᴅ ꜰᴏʀ ᴛʜɪꜱ ᴄʜᴀᴛ ʙᴀʙʏ🥀",
                )
            elif var == "yes":
                sql.set_allow_connect_to_chat(chat.id, True)
                send_message(
                    update.effective_message,
                    "ᴄᴏɴɴᴇᴄᴛɪᴏɴ ʜᴀꜱ ʙᴇᴇɴ ᴇɴᴀʙʟᴇᴅ ꜰᴏʀ ᴛʜɪꜱ ᴄʜᴀᴛ ʙᴀʙʏ🥀",
                )
            else:
                send_message(
                    update.effective_message,
                    "ᴘʟᴇᴀꜱᴇ ᴇɴᴛᴇʀ `yes` or `no` ʙᴀʙʏ🥀!",
                    parse_mode=ParseMode.MARKDOWN,
                )
        else:
            get_settings = sql.allow_connect_to_chat(chat.id)
            if get_settings:
                send_message(
                    update.effective_message,
                    "ᴄᴏɴɴᴇᴄᴛɪᴏɴꜱ ᴛᴏ ᴛʜɪꜱ ɢʀᴏᴜᴘ ᴀʀᴇ *ᴀʟʟᴏᴡᴇᴅ* ꜰᴏʀ ᴍᴇᴍʙᴇʀꜱ ʙᴀʙʏ🥀!",
                    parse_mode=ParseMode.MARKDOWN,
                )
            else:
                send_message(
                    update.effective_message,
                    "ᴄᴏɴɴᴇᴄᴛɪᴏɴ ᴛᴏ ᴛʜɪꜱ ɢʀᴏᴜᴘ ᴀʀᴇ *ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ* ꜰᴏʀ ᴍᴇᴍʙᴇʀꜱ ʙᴀʙʏ🥀!",
                    parse_mode=ParseMode.MARKDOWN,
                )
    else:
        send_message(
            update.effective_message,
            "ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪꜱ ꜰᴏʀ ɢʀᴏᴜᴘ ᴏɴʟʏ. ɴᴏᴛ ɪɴ ᴘᴍ ʙᴀʙʏ🥀!",
        )


@typing_action
def connection_chat(update, context):

    chat = update.effective_chat
    user = update.effective_user

    conn = connected(context.bot, update, chat, user.id, need_admin=True)

    if conn:
        chat = dispatcher.bot.getChat(conn)
        chat_name = dispatcher.bot.getChat(conn).title
    else:
        if update.effective_message.chat.type != "private":
            return
        chat = update.effective_chat
        chat_name = update.effective_message.chat.title

    if conn:
        message = "ʏᴏᴜ ᴀʀᴇ ᴄᴜʀʀᴇɴᴛʟʏ ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴛᴏ {} ʙᴀʙʏ🥀.\n".format(chat_name)
    else:
        message = "ʏᴏᴜ ᴀʀᴇ ᴄᴜʀʀᴇɴᴛʟʏ ɴᴏᴛ ᴄᴏɴɴᴇᴄᴛᴇᴅ ɪɴ ᴀɴʏ ɢʀᴏᴜᴘ ʙᴀʙʏ🥀.\n"
    send_message(update.effective_message, message, parse_mode="markdown")


@typing_action
def connect_chat(update, context):

    chat = update.effective_chat
    user = update.effective_user
    args = context.args

    if update.effective_chat.type == "private":
        if args and len(args) >= 1:
            try:
                connect_chat = int(args[0])
                getstatusadmin = context.bot.get_chat_member(
                    connect_chat,
                    update.effective_message.from_user.id,
                )
            except ValueError:
                try:
                    connect_chat = str(args[0])
                    get_chat = context.bot.getChat(connect_chat)
                    connect_chat = get_chat.id
                    getstatusadmin = context.bot.get_chat_member(
                        connect_chat,
                        update.effective_message.from_user.id,
                    )
                except BadRequest:
                    send_message(update.effective_message, "ɪɴᴠᴀʟɪᴅ ᴄʜᴀᴛ ɪᴅ ʙᴀʙʏ🥀!")
                    return
            except BadRequest:
                send_message(update.effective_message, "ɪɴᴠᴀʟɪᴅ ᴄʜᴀᴛ ɪᴅ ʙᴀʙʏ🥀!")
                return

            isadmin = getstatusadmin.status in ("administrator", "creator")
            ismember = getstatusadmin.status in ("member")
            isallow = sql.allow_connect_to_chat(connect_chat)

            if (isadmin) or (isallow and ismember) or (user.id in DRAGONS):
                connection_status = sql.connect(
                    update.effective_message.from_user.id,
                    connect_chat,
                )
                if connection_status:
                    conn_chat = dispatcher.bot.getChat(
                        connected(context.bot, update, chat, user.id, need_admin=False),
                    )
                    chat_name = conn_chat.title
                    send_message(
                        update.effective_message,
                        "ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴛᴏ *{}*. \nᴜꜱᴇ /helpconnect ᴛᴏ ᴄʜᴇᴄᴋ ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅꜱ ʙᴀʙʏ🥀.".format(
                            chat_name,
                        ),
                        parse_mode=ParseMode.MARKDOWN,
                    )
                    sql.add_history_conn(user.id, str(conn_chat.id), chat_name)
                else:
                    send_message(update.effective_message, "Connection failed!")
            else:
                send_message(
                    update.effective_message,
                    "ᴄᴏɴɴᴇᴄᴛɪᴏɴ ᴛᴏ ᴛʜɪꜱ ᴄʜᴀᴛ ɪꜱ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ʙᴀʙʏ🥀!",
                )
        else:
            gethistory = sql.get_history_conn(user.id)
            if gethistory:
                buttons = [
                    InlineKeyboardButton(
                        text="❎ Close button",
                        callback_data="connect_close",
                    ),
                    InlineKeyboardButton(
                        text="🧹 Clear history",
                        callback_data="connect_clear",
                    ),
                ]
            else:
                buttons = []
            conn = connected(context.bot, update, chat, user.id, need_admin=False)
            if conn:
                connectedchat = dispatcher.bot.getChat(conn)
                text = "ʏᴏᴜ ᴀʀᴇ ᴄᴜʀʀᴇɴᴛʟʏ ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴛᴏ *{}* (`{}`) ʙᴀʙʏ🥀".format(
                    connectedchat.title,
                    conn,
                )
                buttons.append(
                    InlineKeyboardButton(
                        text="🔌 Disconnect",
                        callback_data="connect_disconnect",
                    ),
                )
            else:
                text = "ᴡʀɪᴛᴇ ᴛʜᴇ ᴄʜᴀᴛ ɪᴅ ᴏʀ ᴛᴀɢ ᴛᴏ ᴄᴏɴɴᴇᴄᴛ ʙᴀʙʏ🥀!"
            if gethistory:
                text += "\n\n*ᴄᴏɴɴᴇᴄᴛɪᴏɴ ʜɪꜱᴛᴏʀʏ:*\n"
                text += "╒═══「 *ɪɴꜰᴏ* 」\n"
                text += "│  ꜱᴏʀᴛᴇᴅ: `ɴᴇᴡᴇꜱᴛ`\n"
                text += "│\n"
                buttons = [buttons]
                for x in sorted(gethistory.keys(), reverse=True):
                    htime = time.strftime("%d/%m/%Y", time.localtime(x))
                    text += "╞═「 *{}* 」\n│   `{}`\n│   `{}`\n".format(
                        gethistory[x]["chat_name"],
                        gethistory[x]["chat_id"],
                        htime,
                    )
                    text += "│\n"
                    buttons.append(
                        [
                            InlineKeyboardButton(
                                text=gethistory[x]["chat_name"],
                                callback_data="connect({})".format(
                                    gethistory[x]["chat_id"],
                                ),
                            ),
                        ],
                    )
                text += "╘══「 ᴛᴏᴛᴀʟ {} ᴄʜᴀᴛꜱ 」".format(
                    str(len(gethistory)) + " (max)"
                    if len(gethistory) == 5
                    else str(len(gethistory)),
                )
                conn_hist = InlineKeyboardMarkup(buttons)
            elif buttons:
                conn_hist = InlineKeyboardMarkup([buttons])
            else:
                conn_hist = None
            send_message(
                update.effective_message,
                text,
                parse_mode="markdown",
                reply_markup=conn_hist,
            )

    else:
        getstatusadmin = context.bot.get_chat_member(
            chat.id,
            update.effective_message.from_user.id,
        )
        isadmin = getstatusadmin.status in ("administrator", "creator")
        ismember = getstatusadmin.status in ("member")
        isallow = sql.allow_connect_to_chat(chat.id)
        if (isadmin) or (isallow and ismember) or (user.id in DRAGONS):
            connection_status = sql.connect(
                update.effective_message.from_user.id,
                chat.id,
            )
            if connection_status:
                chat_name = dispatcher.bot.getChat(chat.id).title
                send_message(
                    update.effective_message,
                    "ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴛᴏ *{}* ʙᴀʙʏ🥀.".format(chat_name),
                    parse_mode=ParseMode.MARKDOWN,
                )
                try:
                    sql.add_history_conn(user.id, str(chat.id), chat_name)
                    context.bot.send_message(
                        update.effective_message.from_user.id,
                        "ʏᴏᴜ ᴀʀᴇ ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴛᴏ *{}*. \nᴜꜱᴇ `/helpconnect` ᴛᴏ ᴄʜᴇᴄᴋ ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅꜱ ʙᴀʙʏ🥀.".format(
                            chat_name,
                        ),
                        parse_mode="markdown",
                    )
                except BadRequest:
                    pass
                except Unauthorized:
                    pass
            else:
                send_message(update.effective_message, "ᴄᴏɴɴᴇᴄᴛɪᴏɴ ꜰᴀɪʟᴇᴅ ʙᴀʙʏ🥀!")
        else:
            send_message(
                update.effective_message,
                "ᴄᴏɴɴᴇᴄᴛɪᴏɴ ᴛᴏ ᴛʜɪꜱ ᴄʜᴀᴛ ɪꜱ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ʙᴀʙʏ🥀!",
            )


def disconnect_chat(update, context):

    if update.effective_chat.type == "private":
        disconnection_status = sql.disconnect(update.effective_message.from_user.id)
        if disconnection_status:
            sql.disconnected_chat = send_message(
                update.effective_message,
                "ᴅɪꜱᴄᴏɴɴᴇᴄᴛᴇᴅ ꜰʀᴏᴍ ᴄʜᴀᴛ ʙᴀʙʏ🥀!",
            )
        else:
            send_message(update.effective_message, "ʏᴏᴜ'ʀᴇ ɴᴏᴛ ᴄᴏɴɴᴇᴄᴛᴇᴅ ʙᴀʙʏ🥀!")
    else:
        send_message(update.effective_message, "ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪꜱ ᴏɴʟʏ ᴀᴠᴀɪʟᴀʙʟᴇ ɪɴ ᴘᴍ ʙᴀʙʏ🥀.")


def connected(bot: Bot, update: Update, chat, user_id, need_admin=True):
    user = update.effective_user

    if chat.type == chat.PRIVATE and sql.get_connected_chat(user_id):

        conn_id = sql.get_connected_chat(user_id).chat_id
        getstatusadmin = bot.get_chat_member(
            conn_id,
            update.effective_message.from_user.id,
        )
        isadmin = getstatusadmin.status in ("administrator", "creator")
        ismember = getstatusadmin.status in ("member")
        isallow = sql.allow_connect_to_chat(conn_id)

        if (
            (isadmin)
            or (isallow and ismember)
            or (user.id in DRAGONS)
            or (user.id in DEV_USERS)
        ):
            if need_admin is True:
                if (
                    getstatusadmin.status in ("administrator", "creator")
                    or user_id in DRAGONS
                    or user.id in DEV_USERS
                ):
                    return conn_id
                send_message(
                    update.effective_message,
                    "ʏᴏᴜ ᴍᴜꜱᴛ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ ɪɴ ᴛʜᴇ ᴄᴏɴɴᴇᴄᴛᴇᴅ ɢʀᴏᴜᴘ ʙᴀʙʏ🥀!",
                )
            else:
                return conn_id
        else:
            send_message(
                update.effective_message,
                "ᴛʜᴇ ɢʀᴏᴜᴘ ᴄʜᴀɴɢᴇᴅ ᴛʜᴇ ᴄᴏɴɴᴇᴄᴛɪᴏɴ ʀɪɢʜᴛꜱ ᴏʀ ʏᴏᴜ ᴀʀᴇ ɴᴏ ʟᴏɴɢᴇʀ ᴀɴ ᴀᴅᴍɪɴ.\nɪ'ᴠᴇ ᴅɪꜱᴄᴏɴɴᴇᴄᴛᴇᴅ ʏᴏᴜ ʙᴀʙʏ🥀.",
            )
            disconnect_chat(update, bot)
    else:
        return False


CONN_HELP = """
 Actions are available with connected groups:
 » View and edit Notes.
 » View and edit Filters.
 » Get invite link of chat.
 » Set and control AntiFlood settings.
 » Set and control Blacklist settings.
 » Set Locks and Unlocks in chat.
 » Enable and Disable commands in chat.
 » Export and Imports of chat backup.
 » More in future!"""


def help_connect_chat(update, context):

    args = context.args

    if update.effective_message.chat.type != "private":
        send_message(update.effective_message, "ᴘᴍ ᴍᴇ ᴡɪᴛʜ ᴛʜᴀᴛ ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ɢᴇᴛ ʜᴇʟᴘ ʙᴀʙʏ🥀.")
        return
    send_message(update.effective_message, CONN_HELP, parse_mode="markdown")


def connect_button(update, context):

    query = update.callback_query
    chat = update.effective_chat
    user = update.effective_user

    connect_match = re.match(r"connect\((.+?)\)", query.data)
    disconnect_match = query.data == "connect_disconnect"
    clear_match = query.data == "connect_clear"
    connect_close = query.data == "connect_close"

    if connect_match:
        target_chat = connect_match.group(1)
        getstatusadmin = context.bot.get_chat_member(target_chat, query.from_user.id)
        isadmin = getstatusadmin.status in ("administrator", "creator")
        ismember = getstatusadmin.status in ("member")
        isallow = sql.allow_connect_to_chat(target_chat)

        if (isadmin) or (isallow and ismember) or (user.id in DRAGONS):
            connection_status = sql.connect(query.from_user.id, target_chat)

            if connection_status:
                conn_chat = dispatcher.bot.getChat(
                    connected(context.bot, update, chat, user.id, need_admin=False),
                )
                chat_name = conn_chat.title
                query.message.edit_text(
                    "ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴛᴏ *{}*. \nᴜꜱᴇ `/helpconnect` ᴛᴏ ᴄʜᴇᴄᴋ ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅꜱ ʙᴀʙʏ🥀.".format(
                        chat_name,
                    ),
                    parse_mode=ParseMode.MARKDOWN,
                )
                sql.add_history_conn(user.id, str(conn_chat.id), chat_name)
            else:
                query.message.edit_text("Connection failed!")
        else:
            context.bot.answer_callback_query(
                query.id,
                "ᴄᴏɴɴᴇᴄᴛɪᴏɴ ᴛᴏ ᴛʜɪꜱ ᴄʜᴀᴛ ɪꜱ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ʙᴀʙʏ🥀!",
                show_alert=True,
            )
    elif disconnect_match:
        disconnection_status = sql.disconnect(query.from_user.id)
        if disconnection_status:
            sql.disconnected_chat = query.message.edit_text("ᴅɪꜱᴄᴏɴɴᴇᴄᴛᴇᴅ ꜰʀᴏᴍ ᴄʜᴀᴛ ʙᴀʙʏ🥀!")
        else:
            context.bot.answer_callback_query(
                query.id,
                "ʏᴏᴜ'ʀᴇ ɴᴏᴛ ᴄᴏɴɴᴇᴄᴛᴇᴅ ʙᴀʙʏ🥀!",
                show_alert=True,
            )
    elif clear_match:
        sql.clear_history_conn(query.from_user.id)
        query.message.edit_text("ʜɪꜱᴛᴏʀʏ ᴄᴏɴɴᴇᴄᴛᴇᴅ ʜᴀꜱ ʙᴇᴇɴ ᴄʟᴇᴀʀᴇᴅ ʙᴀʙʏ🥀!")
    elif connect_close:
        query.message.edit_text("ᴄʟᴏꜱᴇᴅ.\nᴛᴏ ᴏᴘᴇɴ ᴀɢᴀɪɴ, ᴛʏᴘᴇ /connect ʙᴀʙʏ🥀")
    else:
        connect_chat(update, context)


__mod_name__ = "CONNECTION"

__help__ = """
ꜱᴏᴍᴇᴛɪᴍᴇꜱ, ʏᴏᴜ ᴊᴜꜱᴛ ᴡᴀɴᴛ ᴛᴏ ᴀᴅᴅ ꜱᴏᴍᴇ ɴᴏᴛᴇꜱ ᴀɴᴅ ꜰɪʟᴛᴇʀꜱ ᴛᴏ ᴀ ɢʀᴏᴜᴘ ᴄʜᴀᴛ, ʙᴜᴛ ʏᴏᴜ ᴅᴏɴ'ᴛ ᴡᴀɴᴛ ᴇᴠᴇʀʏᴏɴᴇ ᴛᴏ ꜱᴇᴇ; ᴛʜɪꜱ ɪꜱ ᴡʜᴇʀᴇ ᴄᴏɴɴᴇᴄᴛɪᴏɴꜱ ᴄᴏᴍᴇ ɪɴ...
ᴛʜɪꜱ ᴀʟʟᴏᴡꜱ ʏᴏᴜ ᴛᴏ ᴄᴏɴɴᴇᴄᴛ ᴛᴏ ᴀ ᴄʜᴀᴛ'ꜱ ᴅᴀᴛᴀʙᴀꜱᴇ, ᴀɴᴅ ᴀᴅᴅ ᴛʜɪɴɢꜱ ᴛᴏ ɪᴛ ᴡɪᴛʜᴏᴜᴛ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅꜱ ᴀᴘᴘᴇᴀʀɪɴɢ ɪɴ ᴄʜᴀᴛ! ꜰᴏʀ ᴏʙᴠɪᴏᴜꜱ ʀᴇᴀꜱᴏɴꜱ, ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ ᴛᴏ ᴀᴅᴅ ᴛʜɪɴɢꜱ; ʙᴜᴛ ᴀɴʏ ᴍᴇᴍʙᴇʀ ɪɴ ᴛʜᴇ ɢʀᴏᴜᴘ ᴄᴀɴ ᴠɪᴇᴡ ʏᴏᴜʀ ᴅᴀᴛᴀ.

» `/connect`: ᴄᴏɴɴᴇᴄᴛꜱ ᴛᴏ ᴄʜᴀᴛ (ᴄᴀɴ ʙᴇ ᴅᴏɴᴇ ɪɴ ᴀ ɢʀᴏᴜᴘ ʙʏ `/connect` ᴏʀ `/connect` <chat id> ɪɴ ᴘᴍ)
» `/connection`: ʟɪꜱᴛ ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴄʜᴀᴛꜱ
» `/disconnect`: ᴅɪꜱᴄᴏɴɴᴇᴄᴛ ꜰʀᴏᴍ ᴀ ᴄʜᴀᴛ
» `/helpconnect`: ʟɪꜱᴛ ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅꜱ ᴛʜᴀᴛ ᴄᴀɴ ʙᴇ ᴜꜱᴇᴅ ʀᴇᴍᴏᴛᴇʟʏ

*ᴀᴅᴍɪɴ ᴏɴʟʏ:*

» `/allowconnect` <yes/no>: ᴀʟʟᴏᴡ ᴀ ᴜꜱᴇʀ ᴛᴏ ᴄᴏɴɴᴇᴄᴛ ᴛᴏ ᴀ ᴄʜᴀᴛ
"""

CONNECT_CHAT_HANDLER = CommandHandler(
    "connect", connect_chat, pass_args=True, run_async=True
)
CONNECTION_CHAT_HANDLER = CommandHandler("connection", connection_chat, run_async=True)
DISCONNECT_CHAT_HANDLER = CommandHandler("disconnect", disconnect_chat, run_async=True)
ALLOW_CONNECTIONS_HANDLER = CommandHandler(
    "allowconnect",
    allow_connections,
    pass_args=True,
    run_async=True,
)
HELP_CONNECT_CHAT_HANDLER = CommandHandler(
    "helpconnect", help_connect_chat, run_async=True
)
CONNECT_BTN_HANDLER = CallbackQueryHandler(
    connect_button, pattern=r"connect", run_async=True
)

dispatcher.add_handler(CONNECT_CHAT_HANDLER)
dispatcher.add_handler(CONNECTION_CHAT_HANDLER)
dispatcher.add_handler(DISCONNECT_CHAT_HANDLER)
dispatcher.add_handler(ALLOW_CONNECTIONS_HANDLER)
dispatcher.add_handler(HELP_CONNECT_CHAT_HANDLER)
dispatcher.add_handler(CONNECT_BTN_HANDLER)
