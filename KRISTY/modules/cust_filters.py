import re
import random
from html import escape
import telegram
from telegram import ParseMode, InlineKeyboardMarkup, Message, InlineKeyboardButton
from telegram.error import BadRequest
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    DispatcherHandlerStop,
    CallbackQueryHandler,
    run_async,
    Filters,
)
from telegram.utils.helpers import mention_html, escape_markdown
from KRISTY import dispatcher, LOGGER, DRAGONS
from KRISTY.modules.disable import DisableAbleCommandHandler
from KRISTY.modules.helper_funcs.handlers import MessageHandlerChecker
from KRISTY.modules.helper_funcs.chat_status import user_admin
from KRISTY.modules.helper_funcs.extraction import extract_text
from KRISTY.modules.helper_funcs.filters import CustomFilters
from KRISTY.modules.helper_funcs.misc import build_keyboard_parser
from KRISTY.modules.helper_funcs.msg_types import get_filter_type
from KRISTY.modules.helper_funcs.string_handling import (
    split_quotes,
    button_markdown_parser,
    escape_invalid_curly_brackets,
    markdown_to_html,
)
from KRISTY.modules.sql import cust_filters_sql as sql
from KRISTY.modules.connection import connected
from KRISTY.modules.helper_funcs.alternate import send_message, typing_action

HANDLER_GROUP = 10

ENUM_FUNC_MAP = {
    sql.Types.TEXT.value: dispatcher.bot.send_message,
    sql.Types.BUTTON_TEXT.value: dispatcher.bot.send_message,
    sql.Types.STICKER.value: dispatcher.bot.send_sticker,
    sql.Types.DOCUMENT.value: dispatcher.bot.send_document,
    sql.Types.PHOTO.value: dispatcher.bot.send_photo,
    sql.Types.AUDIO.value: dispatcher.bot.send_audio,
    sql.Types.VOICE.value: dispatcher.bot.send_voice,
    sql.Types.VIDEO.value: dispatcher.bot.send_video,
    # sql.Types.VIDEO_NOTE.value: dispatcher.bot.send_video_note
}


@typing_action
def list_handlers(update, context):
    chat = update.effective_chat
    user = update.effective_user

    conn = connected(context.bot, update, chat, user.id, need_admin=False)
    if not conn is False:
        chat_id = conn
        chat_name = dispatcher.bot.getChat(conn).title
        filter_list = "*ꜰɪʟᴛᴇʀ ɪɴ {}:*\n"
    else:
        chat_id = update.effective_chat.id
        if chat.type == "private":
            chat_name = "Local filters"
            filter_list = "*ʟᴏᴄᴀʟ ꜰɪʟᴛᴇʀꜱ:*\n"
        else:
            chat_name = chat.title
            filter_list = "*ꜰɪʟᴛᴇʀ ɪɴ {}*:\n"

    all_handlers = sql.get_chat_triggers(chat_id)

    if not all_handlers:
        send_message(
            update.effective_message, "ɴᴏ ꜰɪʟᴛᴇʀꜱ ꜱᴀᴠᴇᴅ ɪɴ {} ʙᴀʙʏ🥀!".format(chat_name)
        )
        return

    for keyword in all_handlers:
        entry = " • `{}`\n".format(escape_markdown(keyword))
        if len(entry) + len(filter_list) > telegram.MAX_MESSAGE_LENGTH:
            send_message(
                update.effective_message,
                filter_list.format(chat_name),
                parse_mode=telegram.ParseMode.MARKDOWN,
            )
            filter_list = entry
        else:
            filter_list += entry

    send_message(
        update.effective_message,
        filter_list.format(chat_name),
        parse_mode=telegram.ParseMode.MARKDOWN,
    )


# NOT ASYNC BECAUSE DISPATCHER HANDLER RAISED
@user_admin
@typing_action
def filters(update, context):
    chat = update.effective_chat
    user = update.effective_user
    msg = update.effective_message
    args = msg.text.split(
        None, 1
    )  # use python's maxsplit to separate Cmd, keyword, and reply_text

    conn = connected(context.bot, update, chat, user.id)
    if not conn is False:
        chat_id = conn
        chat_name = dispatcher.bot.getChat(conn).title
    else:
        chat_id = update.effective_chat.id
        if chat.type == "private":
            chat_name = "local filters"
        else:
            chat_name = chat.title

    if not msg.reply_to_message and len(args) < 2:
        send_message(
            update.effective_message,
            "ᴘʟᴇᴀꜱᴇ ᴘʀᴏᴠɪᴅᴇ ᴋᴇʏʙᴏᴀʀᴅ ᴋᴇʏᴡᴏʀᴅ ꜰᴏʀ ᴛʜɪꜱ ꜰɪʟᴛᴇʀ ᴛᴏ ʀᴇᴘʟʏ ᴡɪᴛʜ ʙᴀʙʏ🥀!",
        )
        return

    if msg.reply_to_message:
        if len(args) < 2:
            send_message(
                update.effective_message,
                "ᴘʟᴇᴀꜱᴇ ᴘʀᴏᴠɪᴅᴇ ᴋᴇʏᴡᴏʀᴅ ꜰᴏʀ ᴛʜɪꜱ ꜰɪʟᴛᴇʀ ᴛᴏ ʀᴇᴘʟʏ ᴡɪᴛʜ ʙᴀʙʏ🥀!",
            )
            return
        else:
            keyword = args[1]
    else:
        extracted = split_quotes(args[1])
        if len(extracted) < 1:
            return
        # set trigger -> lower, so as to avoid adding duplicate filters with different cases
        keyword = extracted[0].lower()

    # Add the filter
    # Note: perhaps handlers can be removed somehow using sql.get_chat_filters
    for handler in dispatcher.handlers.get(HANDLER_GROUP, []):
        if handler.filters == (keyword, chat_id):
            dispatcher.remove_handler(handler, HANDLER_GROUP)

    text, file_type, file_id = get_filter_type(msg)
    if not msg.reply_to_message and len(extracted) >= 2:
        offset = len(extracted[1]) - len(
            msg.text
        )  # set correct offset relative to command + notename
        text, buttons = button_markdown_parser(
            extracted[1], entities=msg.parse_entities(), offset=offset
        )
        text = text.strip()
        if not text:
            send_message(
                update.effective_message,
                "ᴛʜᴇʀᴇ ɪꜱ ɴᴏ ɴᴏᴛᴇ ᴍᴇꜱꜱᴀɢᴇ - ʏᴏᴜ ᴄᴀɴ'ᴛ ᴊᴜꜱᴛ ʜᴀᴠᴇ ʙᴜᴛᴛᴏɴꜱ, ʏᴏᴜ ɴᴇᴇᴅ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ɢᴏ ᴡɪᴛʜ ɪᴛ ʙᴀʙʏ🥀!",
            )
            return

    elif msg.reply_to_message and len(args) >= 2:
        if msg.reply_to_message.text:
            text_to_parsing = msg.reply_to_message.text
        elif msg.reply_to_message.caption:
            text_to_parsing = msg.reply_to_message.caption
        else:
            text_to_parsing = ""
        offset = len(
            text_to_parsing
        )  # set correct offset relative to command + notename
        text, buttons = button_markdown_parser(
            text_to_parsing, entities=msg.parse_entities(), offset=offset
        )
        text = text.strip()

    elif not text and not file_type:
        send_message(
            update.effective_message,
            "ᴘʟᴇᴀꜱᴇ ᴘʀᴏᴠɪᴅᴇ ᴋᴇʏᴡᴏʀᴅ ꜰᴏʀ ᴛʜɪꜱ ꜰɪʟᴛᴇʀ ʀᴇᴘʟʏ ᴡɪᴛʜ ʙᴀʙʏ🥀!",
        )
        return

    elif msg.reply_to_message:
        if msg.reply_to_message.text:
            text_to_parsing = msg.reply_to_message.text
        elif msg.reply_to_message.caption:
            text_to_parsing = msg.reply_to_message.caption
        else:
            text_to_parsing = ""
        offset = len(
            text_to_parsing
        )  # set correct offset relative to command + notename
        text, buttons = button_markdown_parser(
            text_to_parsing, entities=msg.parse_entities(), offset=offset
        )
        text = text.strip()
        if (msg.reply_to_message.text or msg.reply_to_message.caption) and not text:
            send_message(
                update.effective_message,
                "ᴛʜᴇʀᴇ ɪꜱ ɴᴏ ɴᴏᴛᴇ ᴍᴇꜱꜱᴀɢᴇ - ʏᴏᴜ ᴄᴀɴ'ᴛ ᴊᴜꜱᴛ ʜᴀᴠᴇ ʙᴜᴛᴛᴏɴꜱ, ʏᴏᴜ ɴᴇᴇᴅ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ɢᴏ ᴡɪᴛʜ ɪᴛ ʙᴀʙʏ🥀!",
            )
            return

    else:
        send_message(update.effective_message, "ɪɴᴠᴀʟɪᴅ ꜰɪʟᴛᴇʀ ʙᴀʙʏ🥀!")
        return

    add = addnew_filter(update, chat_id, keyword, text, file_type, file_id, buttons)
    # This is an old method
    # sql.add_filter(chat_id, keyword, content, is_sticker, is_document, is_image, is_audio, is_voice, is_video, buttons)

    if add is True:
        send_message(
            update.effective_message,
            "ꜱᴀᴠᴇᴅ ꜰɪʟᴛᴇʀ '{}' ɪɴ *{}* ʙᴀʙʏ🥀!".format(keyword, chat_name),
            parse_mode=telegram.ParseMode.MARKDOWN,
        )
    raise DispatcherHandlerStop


# NOT ASYNC BECAUSE DISPATCHER HANDLER RAISED
@user_admin
@typing_action
def stop_filter(update, context):
    chat = update.effective_chat
    user = update.effective_user
    args = update.effective_message.text.split(None, 1)

    conn = connected(context.bot, update, chat, user.id)
    if not conn is False:
        chat_id = conn
        chat_name = dispatcher.bot.getChat(conn).title
    else:
        chat_id = update.effective_chat.id
        if chat.type == "private":
            chat_name = "Local filters"
        else:
            chat_name = chat.title

    if len(args) < 2:
        send_message(update.effective_message, "ᴡʜᴀᴛ ꜱʜᴏᴜʟᴅ ɪ ꜱᴛᴏᴘ? ʙᴀʙʏ🥀")
        return

    chat_filters = sql.get_chat_triggers(chat_id)

    if not chat_filters:
        send_message(update.effective_message, "ɴᴏ ꜰɪʟᴛᴇʀꜱ ᴀᴄᴛɪᴠᴇ ʜᴇʀᴇ ʙᴀʙʏ🥀!")
        return

    for keyword in chat_filters:
        if keyword == args[1]:
            sql.remove_filter(chat_id, args[1])
            send_message(
                update.effective_message,
                "ᴏᴋᴀʏ, ɪ'ʟʟ ꜱᴛᴏᴘ ʀᴇᴘʟʏɪɴɢ ᴛᴏ ᴛʜᴀᴛ ꜰɪʟᴛᴇʀ ɪɴ *{}* ʙᴀʙʏ🥀.".format(chat_name),
                parse_mode=telegram.ParseMode.MARKDOWN,
            )
            raise DispatcherHandlerStop

    send_message(
        update.effective_message,
        "ᴛʜᴀᴛ'ꜱ ɴᴏᴛ ᴀ ꜰɪʟᴛᴇʀ - ᴄʟɪᴄᴋ: /filters ᴛᴏ ɢᴇᴛ ᴄᴜʀʀᴇɴᴛʟʏ ᴀᴄᴛɪᴠᴇ ꜰɪʟᴛᴇʀꜱ ʙᴀʙʏ🥀.",
    )


def reply_filter(update, context):
    chat = update.effective_chat  # type: Optional[Chat]
    message = update.effective_message  # type: Optional[Message]

    if not update.effective_user or update.effective_user.id == 777000:
        return
    to_match = extract_text(message)
    if not to_match:
        return

    chat_filters = sql.get_chat_triggers(chat.id)
    for keyword in chat_filters:
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, to_match, flags=re.IGNORECASE):
            if MessageHandlerChecker.check_user(update.effective_user.id):
                return
            filt = sql.get_filter(chat.id, keyword)
            if filt.reply == "there is should be a new reply":
                buttons = sql.get_buttons(chat.id, filt.keyword)
                keyb = build_keyboard_parser(context.bot, chat.id, buttons)
                keyboard = InlineKeyboardMarkup(keyb)

                VALID_WELCOME_FORMATTERS = [
                    "first",
                    "last",
                    "fullname",
                    "username",
                    "id",
                    "chatname",
                    "mention",
                ]
                if filt.reply_text:
                    if "%%%" in filt.reply_text:
                        split = filt.reply_text.split("%%%")
                        if all(split):
                            text = random.choice(split)
                        else:
                            text = filt.reply_text
                    else:
                        text = filt.reply_text
                    if text.startswith("~!") and text.endswith("!~"):
                        sticker_id = text.replace("~!", "").replace("!~", "")
                        try:
                            context.bot.send_sticker(
                                chat.id,
                                sticker_id,
                                reply_to_message_id=message.message_id,
                            )
                            return
                        except BadRequest as excp:
                            if (
                                excp.message
                                == "Wrong remote file identifier specified: wrong padding in the string"
                            ):
                                context.bot.send_message(
                                    chat.id,
                                    "ᴍᴇꜱꜱᴀɢᴇ ᴄᴏᴜʟᴅɴ'ᴛ ʙᴇ ꜱᴇɴᴛ, ɪꜱ ᴛʜᴇ ꜱᴛɪᴄᴋᴇʀ ɪᴅ ᴠᴀʟɪᴅ? ʙᴀʙʏ🥀",
                                )
                                return
                            else:
                                LOGGER.exception("Error in filters: " + excp.message)
                                return
                    valid_format = escape_invalid_curly_brackets(
                        text, VALID_WELCOME_FORMATTERS
                    )
                    if valid_format:
                        filtext = valid_format.format(
                            first=escape(message.from_user.first_name),
                            last=escape(
                                message.from_user.last_name
                                or message.from_user.first_name
                            ),
                            fullname=" ".join(
                                [
                                    escape(message.from_user.first_name),
                                    escape(message.from_user.last_name),
                                ]
                                if message.from_user.last_name
                                else [escape(message.from_user.first_name)]
                            ),
                            username="@" + escape(message.from_user.username)
                            if message.from_user.username
                            else mention_html(
                                message.from_user.id, message.from_user.first_name
                            ),
                            mention=mention_html(
                                message.from_user.id, message.from_user.first_name
                            ),
                            chatname=escape(message.chat.title)
                            if message.chat.type != "private"
                            else escape(message.from_user.first_name),
                            id=message.from_user.id,
                        )
                    else:
                        filtext = ""
                else:
                    filtext = ""

                if filt.file_type in (sql.Types.BUTTON_TEXT, sql.Types.TEXT):
                    try:
                        context.bot.send_message(
                            chat.id,
                            markdown_to_html(filtext),
                            reply_to_message_id=message.message_id,
                            parse_mode=ParseMode.HTML,
                            disable_web_page_preview=True,
                            reply_markup=keyboard,
                        )
                    except BadRequest as excp:
                        error_catch = get_exception(excp, filt, chat)
                        if error_catch == "noreply":
                            try:
                                context.bot.send_message(
                                    chat.id,
                                    markdown_to_html(filtext),
                                    parse_mode=ParseMode.HTML,
                                    disable_web_page_preview=True,
                                    reply_markup=keyboard,
                                )
                            except BadRequest as excp:
                                LOGGER.exception("Error in filters: " + excp.message)
                                send_message(
                                    update.effective_message,
                                    get_exception(excp, filt, chat),
                                )
                        else:
                            try:
                                send_message(
                                    update.effective_message,
                                    get_exception(excp, filt, chat),
                                )
                            except BadRequest as excp:
                                LOGGER.exception(
                                    "Failed to send message: " + excp.message
                                )
                                pass
                else:
                    if ENUM_FUNC_MAP[filt.file_type] == dispatcher.bot.send_sticker:
                        ENUM_FUNC_MAP[filt.file_type](
                            chat.id,
                            filt.file_id,
                            reply_to_message_id=message.message_id,
                            reply_markup=keyboard,
                        )
                    else:
                        ENUM_FUNC_MAP[filt.file_type](
                            chat.id,
                            filt.file_id,
                            caption=markdown_to_html(filtext),
                            reply_to_message_id=message.message_id,
                            parse_mode=ParseMode.HTML,
                            reply_markup=keyboard,
                        )
                break
            else:
                if filt.is_sticker:
                    message.reply_sticker(filt.reply)
                elif filt.is_document:
                    message.reply_document(filt.reply)
                elif filt.is_image:
                    message.reply_photo(filt.reply)
                elif filt.is_audio:
                    message.reply_audio(filt.reply)
                elif filt.is_voice:
                    message.reply_voice(filt.reply)
                elif filt.is_video:
                    message.reply_video(filt.reply)
                elif filt.has_markdown:
                    buttons = sql.get_buttons(chat.id, filt.keyword)
                    keyb = build_keyboard_parser(context.bot, chat.id, buttons)
                    keyboard = InlineKeyboardMarkup(keyb)

                    try:
                        send_message(
                            update.effective_message,
                            filt.reply,
                            parse_mode=ParseMode.MARKDOWN,
                            disable_web_page_preview=True,
                            reply_markup=keyboard,
                        )
                    except BadRequest as excp:
                        if excp.message == "Unsupported url protocol":
                            try:
                                send_message(
                                    update.effective_message,
                                    "ʏᴏᴜ ꜱᴇᴇᴍ ᴛᴏ ʙᴇ ᴛʀʏɪɴɢ ᴛᴏ ᴜꜱᴇ ᴀɴ ᴜɴꜱᴜᴘᴘᴏʀᴛᴇᴅ ᴜʀʟ ᴘʀᴏᴛᴏᴄᴏʟ. "
                                    "ᴛᴇʟᴇɢʀᴀᴍ ᴅᴏᴇꜱɴ'ᴛ ꜱᴜᴘᴘᴏʀᴛ ʙᴜᴛᴛᴏɴꜱ ꜰᴏʀ ꜱᴏᴍᴇ ᴘʀᴏᴛᴏᴄᴏʟꜱ, ꜱᴜᴄʜ ᴀꜱ ᴛɢ://. ᴘʟᴇᴀꜱᴇ ᴛʀʏ "
                                    "ᴀɢᴀɪɴ ʙᴀʙʏ🥀...",
                                )
                            except BadRequest as excp:
                                LOGGER.exception("Error in filters: " + excp.message)
                                pass
                        elif excp.message == "Reply message not found":
                            try:
                                context.bot.send_message(
                                    chat.id,
                                    filt.reply,
                                    parse_mode=ParseMode.MARKDOWN,
                                    disable_web_page_preview=True,
                                    reply_markup=keyboard,
                                )
                            except BadRequest as excp:
                                LOGGER.exception("Error in filters: " + excp.message)
                                pass
                        else:
                            try:
                                send_message(
                                    update.effective_message,
                                    "ᴛʜɪꜱ ᴍᴇꜱꜱᴀɢᴇ ᴄᴏᴜʟᴅɴ'ᴛ ʙᴇ ꜱᴇɴᴛ ᴀꜱ ɪᴛ'ꜱ ɪɴᴄᴏʀʀᴇᴄᴛʟʏ ꜰᴏʀᴍᴀᴛᴛᴇᴅ ʙᴀʙʏ🥀.",
                                )
                            except BadRequest as excp:
                                LOGGER.exception("Error in filters: " + excp.message)
                                pass
                            LOGGER.warning(
                                "Message %s could not be parsed", str(filt.reply)
                            )
                            LOGGER.exception(
                                "Could not parse filter %s in chat %s",
                                str(filt.keyword),
                                str(chat.id),
                            )

                else:
                    # LEGACY - all new filters will have has_markdown set to True.
                    try:
                        send_message(update.effective_message, filt.reply)
                    except BadRequest as excp:
                        LOGGER.exception("Error in filters: " + excp.message)
                        pass
                break


def rmall_filters(update, context):
    chat = update.effective_chat
    user = update.effective_user
    member = chat.get_member(user.id)
    if member.status != "creator" and user.id not in DRAGONS:
        update.effective_message.reply_text(
            "ᴏɴʟʏ ᴛʜᴇ ᴄʜᴀᴛ ᴏᴡɴᴇʀ ᴄᴀɴ ᴄʟᴇᴀʀ ᴀʟʟ ɴᴏᴛᴇꜱ ᴀᴛ ᴏɴᴄᴇ ʙᴀʙʏ🥀."
        )
    else:
        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Stop all filters", callback_data="filters_rmall"
                    )
                ],
                [InlineKeyboardButton(text="Cancel", callback_data="filters_cancel")],
            ]
        )
        update.effective_message.reply_text(
            f"ᴀʀᴇ ʏᴏᴜ ꜱᴜʀᴇ ʏᴏᴜ ᴡᴏᴜʟᴅ ʟɪᴋᴇ ᴛᴏ ꜱᴛᴏᴘ ᴀʟʟ ꜰɪʟᴛᴇʀꜱ ɪɴ {chat.title}? ᴛʜɪꜱ ᴀᴄᴛɪᴏɴ ᴄᴀɴɴᴏᴛ ʙᴇ ᴜɴᴅᴏɴᴇ ʙᴀʙʏ🥀.",
            reply_markup=buttons,
            parse_mode=ParseMode.MARKDOWN,
        )


def rmall_callback(update, context):
    query = update.callback_query
    chat = update.effective_chat
    msg = update.effective_message
    member = chat.get_member(query.from_user.id)
    if query.data == "filters_rmall":
        if member.status == "creator" or query.from_user.id in DRAGONS:
            allfilters = sql.get_chat_triggers(chat.id)
            if not allfilters:
                msg.edit_text("ɴᴏ ꜰɪʟᴛᴇʀꜱ ɪɴ ᴛʜɪꜱ ᴄʜᴀᴛ, ɴᴏᴛʜɪɴɢ ᴛᴏ ꜱᴛᴏᴘ ʙᴀʙʏ🥀!")
                return

            count = 0
            filterlist = []
            for x in allfilters:
                count += 1
                filterlist.append(x)

            for i in filterlist:
                sql.remove_filter(chat.id, i)

            msg.edit_text(f"ᴄʟᴇᴀɴᴇᴅ {count} ꜰɪʟᴛᴇʀꜱ ɪɴ {chat.title} ʙᴀʙʏ🥀")

        if member.status == "administrator":
            query.answer("ᴏɴʟʏ ᴏᴡɴᴇʀ ᴏꜰ ᴛʜᴇ ᴄʜᴀᴛ ᴄᴀɴ ᴅᴏ ᴛʜɪꜱ ʙᴀʙʏ🥀.")

        if member.status == "member":
            query.answer("ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʙᴇ ᴀᴅᴍɪɴ ᴛᴏ ᴅᴏ ᴛʜɪꜱ ʙᴀʙʏ🥀.")
    elif query.data == "filters_cancel":
        if member.status == "creator" or query.from_user.id in DRAGONS:
            msg.edit_text("ᴄʟᴇᴀʀɪɴɢ ᴏꜰ ᴀʟʟ ꜰɪʟᴛᴇʀꜱ ʜᴀꜱ ʙᴇᴇɴ ᴄᴀɴᴄᴇʟʟᴇᴅ ʙᴀʙʏ🥀.")
            return
        if member.status == "administrator":
            query.answer("ᴏɴʟʏ ᴏᴡɴᴇʀ ᴏꜰ ᴛʜᴇ ᴄʜᴀᴛ ᴄᴀɴ ᴅᴏ ᴛʜɪꜱ ʙᴀʙʏ🥀.")
        if member.status == "member":
            query.answer("ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʙᴇ ᴀᴅᴍɪɴ ᴛᴏ ᴅᴏ ᴛʜɪꜱ ʙᴀʙʏ🥀.")


# NOT ASYNC NOT A HANDLER
def get_exception(excp, filt, chat):
    if excp.message == "Unsupported url protocol":
        return "You seem to be trying to use the URL protocol which is not supported. Telegram does not support key for multiple protocols, such as tg: //. Please try again!"
    elif excp.message == "Reply message not found":
        return "noreply"
    else:
        LOGGER.warning("Message %s could not be parsed", str(filt.reply))
        LOGGER.exception(
            "Could not parse filter %s in chat %s", str(filt.keyword), str(chat.id)
        )
        return "This data could not be sent because it is incorrectly formatted."


# NOT ASYNC NOT A HANDLER
def addnew_filter(update, chat_id, keyword, text, file_type, file_id, buttons):
    msg = update.effective_message
    totalfilt = sql.get_chat_triggers(chat_id)
    if len(totalfilt) >= 150:  # Idk why i made this like function....
        msg.reply_text("ᴛʜɪꜱ ɢʀᴏᴜᴘ ʜᴀꜱ ʀᴇᴀᴄʜᴇᴅ ɪᴛꜱ ᴍᴀx ꜰɪʟᴛᴇʀꜱ ʟɪᴍɪᴛ ᴏꜰ 150 ʙᴀʙʏ🥀.")
        return False
    else:
        sql.new_add_filter(chat_id, keyword, text, file_type, file_id, buttons)
        return True


def __stats__():
    return "× {} filters, across {} chats.".format(sql.num_filters(), sql.num_chats())


def __import_data__(chat_id, data):
    # set chat filters
    filters = data.get("filters", {})
    for trigger in filters:
        sql.add_to_blacklist(chat_id, trigger)


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)


def __chat_settings__(chat_id, user_id):
    cust_filters = sql.get_chat_triggers(chat_id)
    return "There are `{}` custom filters here.".format(len(cust_filters))


__help__ = """

» `/filters`*:* ʟɪꜱᴛ ᴀʟʟ ᴀᴄᴛɪᴠᴇ ꜰɪʟᴛᴇʀꜱ ꜱᴀᴠᴇᴅ ɪɴ ᴛʜᴇ ᴄʜᴀᴛ.

*ᴀᴅᴍɪɴ ᴏɴʟʏ:*
» `/filter` <ᴋᴇʏᴡᴏʀᴅ> <ʀᴇᴘʟʏ ᴍᴇꜱꜱᴀɢᴇ>*:* ᴀᴅᴅ ᴀ ꜰɪʟᴛᴇʀ ᴛᴏ ᴛʜɪꜱ ᴄʜᴀᴛ. ᴛʜᴇ ʙᴏᴛ ᴡɪʟʟ ɴᴏᴡ ʀᴇᴘʟʏ ᴛʜᴀᴛ ᴍᴇꜱꜱᴀɢᴇ ᴡʜᴇɴᴇᴠᴇʀ 'ᴋᴇʏᴡᴏʀᴅ'\
ɪꜱ ᴍᴇɴᴛɪᴏɴᴇᴅ. ɪꜰ ʏᴏᴜ ʀᴇᴘʟʏ ᴛᴏ ᴀ ꜱᴛɪᴄᴋᴇʀ ᴡɪᴛʜ ᴀ ᴋᴇʏᴡᴏʀᴅ, ᴛʜᴇ ʙᴏᴛ ᴡɪʟʟ ʀᴇᴘʟʏ ᴡɪᴛʜ ᴛʜᴀᴛ ꜱᴛɪᴄᴋᴇʀ. ɴᴏᴛᴇ: ᴀʟʟ ꜰɪʟᴛᴇʀ \
ᴋᴇʏᴡᴏʀᴅꜱ ᴀʀᴇ ɪɴ ʟᴏᴡᴇʀᴄᴀꜱᴇ. ɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ʏᴏᴜʀ ᴋᴇʏᴡᴏʀᴅ ᴛᴏ ʙᴇ ᴀ ꜱᴇɴᴛᴇɴᴄᴇ, ᴜꜱᴇ Qᴜᴏᴛᴇꜱ. ᴇɢ: /filter "ʜᴇʏ ᴛʜᴇʀᴇ" ʜᴏᴡ ʏᴏᴜ \
ᴅᴏɪɴ? 

ꜱᴇᴘᴀʀᴀᴛᴇ ᴅɪꜰꜰ ʀᴇᴘʟɪᴇꜱ ʙʏ `%%%` ᴛᴏ ɢᴇᴛ ʀᴀɴᴅᴏᴍ ʀᴇᴘʟɪᴇꜱ 
*ᴇxᴀᴍᴘʟᴇ:*  `/filter "ꜰɪʟᴛᴇʀɴᴀᴍᴇ" 
ʀᴇᴘʟʏ 1
 %%% 
 ʀᴇᴘʟʏ 2 
 %%% 
 ʀᴇᴘʟʏ 3`


» `/stop` <ꜰɪʟᴛᴇʀ ᴋᴇʏᴡᴏʀᴅ>*:* ꜱᴛᴏᴘ ᴛʜᴀᴛ ꜰɪʟᴛᴇʀ.

*ᴄʜᴀᴛ ᴄʀᴇᴀᴛᴏʀ ᴏɴʟʏ:*
» `/removeallfilters`*:* ʀᴇᴍᴏᴠᴇ ᴀʟʟ ᴄʜᴀᴛ ꜰɪʟᴛᴇʀꜱ ᴀᴛ ᴏɴᴄᴇ.

*ɴᴏᴛᴇ*: ꜰɪʟᴛᴇʀꜱ ᴀʟꜱᴏ ꜱᴜᴘᴘᴏʀᴛ ᴍᴀʀᴋᴅᴏᴡɴ ꜰᴏʀᴍᴀᴛᴛᴇʀꜱ ʟɪᴋᴇ: {first}, {last} ᴇᴛᴄ.. ᴀɴᴅ ʙᴜᴛᴛᴏɴꜱ.
ᴄʜᴇᴄᴋ /markdownhelp ᴛᴏ ᴋɴᴏᴡ ᴍᴏʀᴇ!

"""

__mod_name__ = "FILTERS"

FILTER_HANDLER = CommandHandler("filter", filters)
STOP_HANDLER = CommandHandler("stop", stop_filter)
RMALLFILTER_HANDLER = CommandHandler(
    "removeallfilters", rmall_filters, filters=Filters.chat_type.groups, run_async=True
)
RMALLFILTER_CALLBACK = CallbackQueryHandler(
    rmall_callback, pattern=r"filters_.*", run_async=True
)
LIST_HANDLER = DisableAbleCommandHandler(
    "filters", list_handlers, admin_ok=True, run_async=True
)
CUST_FILTER_HANDLER = MessageHandler(
    CustomFilters.has_text & ~Filters.update.edited_message,
    reply_filter,
    run_async=True,
)

dispatcher.add_handler(FILTER_HANDLER)
dispatcher.add_handler(STOP_HANDLER)
dispatcher.add_handler(LIST_HANDLER)
dispatcher.add_handler(CUST_FILTER_HANDLER, HANDLER_GROUP)
dispatcher.add_handler(RMALLFILTER_HANDLER)
dispatcher.add_handler(RMALLFILTER_CALLBACK)

__handlers__ = [
    FILTER_HANDLER,
    STOP_HANDLER,
    LIST_HANDLER,
    (CUST_FILTER_HANDLER, HANDLER_GROUP, RMALLFILTER_HANDLER),
]
