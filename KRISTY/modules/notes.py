import re, ast
from io import BytesIO
import random
from typing import Optional

import KRISTY.modules.sql.notes_sql as sql
from KRISTY import LOGGER, JOIN_LOGGER, SUPPORT_CHAT, dispatcher, DRAGONS
from KRISTY.modules.disable import DisableAbleCommandHandler
from KRISTY.modules.helper_funcs.handlers import MessageHandlerChecker
from KRISTY.modules.helper_funcs.chat_status import user_admin, connection_status
from KRISTY.modules.helper_funcs.misc import build_keyboard, revert_buttons
from KRISTY.modules.helper_funcs.msg_types import get_note_type
from KRISTY.modules.helper_funcs.string_handling import (
    escape_invalid_curly_brackets,
)
from telegram import (
    MAX_MESSAGE_LENGTH,
    InlineKeyboardMarkup,
    Message,
    ParseMode,
    Update,
    InlineKeyboardButton,
)
from telegram.error import BadRequest
from telegram.utils.helpers import escape_markdown, mention_markdown
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    CallbackQueryHandler,
    Filters,
    MessageHandler,
)

FILE_MATCHER = re.compile(r"^###file_id(!photo)?###:(.*?)(?:\s|$)")
STICKER_MATCHER = re.compile(r"^###sticker(!photo)?###:")
BUTTON_MATCHER = re.compile(r"^###button(!photo)?###:(.*?)(?:\s|$)")
MYFILE_MATCHER = re.compile(r"^###file(!photo)?###:")
MYPHOTO_MATCHER = re.compile(r"^###photo(!photo)?###:")
MYAUDIO_MATCHER = re.compile(r"^###audio(!photo)?###:")
MYVOICE_MATCHER = re.compile(r"^###voice(!photo)?###:")
MYVIDEO_MATCHER = re.compile(r"^###video(!photo)?###:")
MYVIDEONOTE_MATCHER = re.compile(r"^###video_note(!photo)?###:")

ENUM_FUNC_MAP = {
    sql.Types.TEXT.value: dispatcher.bot.send_message,
    sql.Types.BUTTON_TEXT.value: dispatcher.bot.send_message,
    sql.Types.STICKER.value: dispatcher.bot.send_sticker,
    sql.Types.DOCUMENT.value: dispatcher.bot.send_document,
    sql.Types.PHOTO.value: dispatcher.bot.send_photo,
    sql.Types.AUDIO.value: dispatcher.bot.send_audio,
    sql.Types.VOICE.value: dispatcher.bot.send_voice,
    sql.Types.VIDEO.value: dispatcher.bot.send_video,
}


# Do not async
def get(update, context, notename, show_none=True, no_format=False):
    bot = context.bot
    chat_id = update.effective_message.chat.id
    note_chat_id = update.effective_chat.id
    note = sql.get_note(note_chat_id, notename)
    message = update.effective_message  # type: Optional[Message]

    if note:
        if MessageHandlerChecker.check_user(update.effective_user.id):
            return
        # If we're replying to a message, reply to that message (unless it's an error)
        if message.reply_to_message:
            reply_id = message.reply_to_message.message_id
        else:
            reply_id = message.message_id
        if note.is_reply:
            if JOIN_LOGGER:
                try:
                    bot.forward_message(
                        chat_id=chat_id,
                        from_chat_id=JOIN_LOGGER,
                        message_id=note.value,
                    )
                except BadRequest as excp:
                    if excp.message == "Message to forward not found":
                        message.reply_text(
                            "ᴛʜɪꜱ ᴍᴇꜱꜱᴀɢᴇ ꜱᴇᴇᴍꜱ ᴛᴏ ʜᴀᴠᴇ ʙᴇᴇɴ ʟᴏꜱᴛ - ɪ'ʟʟ ʀᴇᴍᴏᴠᴇ ɪᴛ"
                            "ꜰʀᴏᴍ ʏᴏᴜʀ ɴᴏᴛᴇꜱ ʟɪꜱᴛ ʙᴀʙʏ🥀.",
                        )
                        sql.rm_note(note_chat_id, notename)
                    else:
                        raise
            else:
                try:
                    bot.forward_message(
                        chat_id=chat_id,
                        from_chat_id=chat_id,
                        message_id=note.value,
                    )
                except BadRequest as excp:
                    if excp.message == "Message to forward not found":
                        message.reply_text(
                            "ʟᴏᴏᴋꜱ ʟɪᴋᴇ ᴛʜᴇ ᴏʀɪɢɪɴᴀʟ ꜱᴇɴᴅᴇʀ ᴏꜰ ᴛʜɪꜱ ɴᴏᴛᴇ ʜᴀꜱ ᴅᴇʟᴇᴛᴇᴅ ʙᴀʙʏ🥀"
                            "ᴛʜᴇɪʀ ᴍᴇꜱꜱᴀɢᴇ - ꜱᴏʀʀʏ! ɢᴇᴛ ʏᴏᴜʀ ʙᴏᴛ ᴀᴅᴍɪɴ ᴛᴏ ꜱᴛᴀʀᴛ ᴜꜱɪɴɢ ᴀ "
                            "ᴍᴇꜱꜱᴀɢᴇ ᴅᴜᴍᴘ ᴛᴏ ᴀᴠᴏɪᴅ ᴛʜɪꜱ ʙᴀʙʏ🥀. ɪ'ʟʟ ʀᴇᴍᴏᴠᴇ ᴛʜɪꜱ ɴᴏᴛᴇ ꜰʀᴏᴍ "
                            "ʏᴏᴜʀ ꜱᴀᴠᴇᴅ ɴᴏᴛᴇꜱ ʙᴀʙʏ🥀.",
                        )
                        sql.rm_note(note_chat_id, notename)
                    else:
                        raise
        else:
            VALID_NOTE_FORMATTERS = [
                "first",
                "last",
                "fullname",
                "username",
                "id",
                "chatname",
                "mention",
            ]
            valid_format = escape_invalid_curly_brackets(
                note.value,
                VALID_NOTE_FORMATTERS,
            )
            if valid_format:
                if not no_format:
                    if "%%%" in valid_format:
                        split = valid_format.split("%%%")
                        if all(split):
                            text = random.choice(split)
                        else:
                            text = valid_format
                    else:
                        text = valid_format
                else:
                    text = valid_format
                text = text.format(
                    first=escape_markdown(message.from_user.first_name),
                    last=escape_markdown(
                        message.from_user.last_name or message.from_user.first_name,
                    ),
                    fullname=escape_markdown(
                        " ".join(
                            [message.from_user.first_name, message.from_user.last_name]
                            if message.from_user.last_name
                            else [message.from_user.first_name],
                        ),
                    ),
                    username="@" + message.from_user.username
                    if message.from_user.username
                    else mention_markdown(
                        message.from_user.id,
                        message.from_user.first_name,
                    ),
                    mention=mention_markdown(
                        message.from_user.id,
                        message.from_user.first_name,
                    ),
                    chatname=escape_markdown(
                        message.chat.title
                        if message.chat.type != "private"
                        else message.from_user.first_name,
                    ),
                    id=message.from_user.id,
                )
            else:
                text = ""

            keyb = []
            parseMode = ParseMode.MARKDOWN
            buttons = sql.get_buttons(note_chat_id, notename)
            if no_format:
                parseMode = None
                text += revert_buttons(buttons)
            else:
                keyb = build_keyboard(buttons)

            keyboard = InlineKeyboardMarkup(keyb)

            try:
                if note.msgtype in (sql.Types.BUTTON_TEXT, sql.Types.TEXT):
                    bot.send_message(
                        chat_id,
                        text,
                        reply_to_message_id=reply_id,
                        parse_mode=parseMode,
                        disable_web_page_preview=True,
                        reply_markup=keyboard,
                    )
                else:
                    ENUM_FUNC_MAP[note.msgtype](
                        chat_id,
                        note.file,
                        caption=text,
                        reply_to_message_id=reply_id,
                        parse_mode=parseMode,
                        reply_markup=keyboard,
                    )

            except BadRequest as excp:
                if excp.message == "Entity_mention_user_invalid":
                    message.reply_text(
                        "ʟᴏᴏᴋꜱ ʟɪᴋᴇ ʏᴏᴜ ᴛʀɪᴇᴅ ᴛᴏ ᴍᴇɴᴛɪᴏɴ ꜱᴏᴍᴇᴏɴᴇ ɪ'ᴠᴇ ɴᴇᴠᴇʀ ꜱᴇᴇɴ ʙᴇꜰᴏʀᴇ ʙᴀʙʏ🥀. ɪꜰ ʏᴏᴜ ʀᴇᴀʟʟʏ "
                        "ᴡᴀɴᴛ ᴛᴏ ᴍᴇɴᴛɪᴏɴ ᴛʜᴇᴍ, ꜰᴏʀᴡᴀʀᴅ ᴏɴᴇ ᴏꜰ ᴛʜᴇɪʀ ᴍᴇꜱꜱᴀɢᴇꜱ ᴛᴏ ᴍᴇ, ᴀɴᴅ ɪ'ʟʟ ʙᴇ ᴀʙʟᴇ "
                        "ᴛᴏ ᴛᴀɢ ᴛʜᴇᴍ ʙᴀʙʏ🥀!",
                    )
                elif FILE_MATCHER.match(note.value):
                    message.reply_text(
                        "ᴛʜɪꜱ ɴᴏᴛᴇ ᴡᴀꜱ ᴀɴ ɪɴᴄᴏʀʀᴇᴄᴛʟʏ ɪᴍᴘᴏʀᴛᴇᴅ ꜰɪʟᴇ ꜰʀᴏᴍ ᴀɴᴏᴛʜᴇʀ ʙᴏᴛ - ɪ ᴄᴀɴ'ᴛ ᴜꜱᴇ "
                        "ɪᴛ ʙᴀʙʏ🥀. ɪꜰ ʏᴏᴜ ʀᴇᴀʟʟʏ ɴᴇᴇᴅ ɪᴛ, ʏᴏᴜ'ʟʟ ʜᴀᴠᴇ ᴛᴏ ꜱᴀᴠᴇ ɪᴛ ᴀɢᴀɪɴ. ɪɴ "
                        "ᴛʜᴇ ᴍᴇᴀɴᴛɪᴍᴇ, ɪ'ʟʟ ʀᴇᴍᴏᴠᴇ ɪᴛ ꜰʀᴏᴍ ʏᴏᴜʀ ɴᴏᴛᴇꜱ ʟɪꜱᴛ ʙᴀʙʏ🥀.",
                    )
                    sql.rm_note(note_chat_id, notename)
                else:
                    message.reply_text(
                        "ᴛʜɪꜱ ɴᴏᴛᴇ ᴄᴏᴜʟᴅ ɴᴏᴛ ʙᴇ ꜱᴇɴᴛ, ᴀꜱ ɪᴛ ɪꜱ ɪɴᴄᴏʀʀᴇᴄᴛʟʏ ꜰᴏʀᴍᴀᴛᴛᴇᴅ ʙᴀʙʏ🥀. ᴀꜱᴋ ɪɴ "
                        f"@{SUPPORT_CHAT} ɪꜰ ʏᴏᴜ ᴄᴀɴ'ᴛ ꜰɪɢᴜʀᴇ ᴏᴜᴛ ᴡʜʏ ʙᴀʙʏ🥀!",
                    )
                    LOGGER.exception(
                        "could not parse message #%s in chat %s",
                        notename,
                        str(note_chat_id),
                    )
                    LOGGER.warning("message was: %s", str(note.value))
        return
    if show_none:
        message.reply_text("ᴛʜɪꜱ ɴᴏᴛᴇ ᴅᴏᴇꜱɴ'ᴛ ᴇxɪꜱᴛ ʙᴀʙʏ🥀")


@connection_status
def cmd_get(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    if len(args) >= 2 and args[1].lower() == "noformat":
        get(update, context, args[0].lower(), show_none=True, no_format=True)
    elif len(args) >= 1:
        get(update, context, args[0].lower(), show_none=True)
    else:
        update.effective_message.reply_text("ɢᴇᴛ ʀᴇᴋᴛ")


@connection_status
def hash_get(update: Update, context: CallbackContext):
    message = update.effective_message.text
    fst_word = message.split()[0]
    no_hash = fst_word[1:].lower()
    get(update, context, no_hash, show_none=False)


@connection_status
def slash_get(update: Update, context: CallbackContext):
    message, chat_id = update.effective_message.text, update.effective_chat.id
    no_slash = message[1:]
    note_list = sql.get_all_chat_notes(chat_id)

    try:
        noteid = note_list[int(no_slash) - 1]
        note_name = str(noteid).strip(">").split()[1]
        get(update, context, note_name, show_none=False)
    except IndexError:
        update.effective_message.reply_text("ᴡʀᴏɴɢ ɴᴏᴛᴇ ɪᴅ ʙᴀʙʏ🥀")


@user_admin
@connection_status
def save(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    msg = update.effective_message  # type: Optional[Message]

    note_name, text, data_type, content, buttons = get_note_type(msg)
    note_name = note_name.lower()
    if data_type is None:
        msg.reply_text(" ʙᴀʙʏ🥀, ᴛʜᴇʀᴇ'ꜱ ɴᴏ ɴᴏᴛᴇ")
        return

    sql.add_note_to_db(
        chat_id,
        note_name,
        text,
        data_type,
        buttons=buttons,
        file=content,
    )

    msg.reply_text(
        f"ʏᴇꜱ! ᴀᴅᴅᴇᴅ `{note_name}`.\nɢᴇᴛ ɪᴛ ᴡɪᴛʜ /get `{note_name}`, ᴏʀ `#{note_name}` ʙᴀʙʏ🥀",
        parse_mode=ParseMode.MARKDOWN,
    )

    if msg.reply_to_message and msg.reply_to_message.from_user.is_bot:
        if text:
            msg.reply_text(
                "ꜱᴇᴇᴍꜱ ʟɪᴋᴇ ʏᴏᴜ'ʀᴇ ᴛʀʏɪɴɢ ᴛᴏ ꜱᴀᴠᴇ ᴀ ᴍᴇꜱꜱᴀɢᴇ ꜰʀᴏᴍ ᴀ ʙᴏᴛ ʙᴀʙʏ🥀. ᴜɴꜰᴏʀᴛᴜɴᴀᴛᴇʟʏ, "
                "ʙᴏᴛꜱ ᴄᴀɴ'ᴛ ꜰᴏʀᴡᴀʀᴅ ʙᴏᴛ ᴍᴇꜱꜱᴀɢᴇꜱ, ꜱᴏ ɪ ᴄᴀɴ'ᴛ ꜱᴀᴠᴇ ᴛʜᴇ ᴇxᴀᴄᴛ ᴍᴇꜱꜱᴀɢᴇ ʙᴀʙʏ🥀. "
                "\nɪ'ʟʟ ꜱᴀᴠᴇ ᴀʟʟ ᴛʜᴇ ᴛᴇxᴛ ɪ ᴄᴀɴ, ʙᴜᴛ ɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴍᴏʀᴇ, ʏᴏᴜ'ʟʟ ʜᴀᴠᴇ ᴛᴏ "
                "ꜰᴏʀᴡᴀʀᴅ ᴛʜᴇ ᴍᴇꜱꜱᴀɢᴇ ʏᴏᴜʀꜱᴇʟꜰ, ᴀɴᴅ ᴛʜᴇɴ ꜱᴀᴠᴇ ɪᴛ ʙᴀʙʏ🥀.",
            )
        else:
            msg.reply_text(
                "ʙᴏᴛꜱ ᴀʀᴇ ᴋɪɴᴅᴀ ʜᴀɴᴅɪᴄᴀᴘᴘᴇᴅ ʙʏ ᴛᴇʟᴇɢʀᴀᴍ, ᴍᴀᴋɪɴɢ ɪᴛ ʜᴀʀᴅ ꜰᴏʀ ʙᴏᴛꜱ ᴛᴏ "
                "ɪɴᴛᴇʀᴀᴄᴛ ᴡɪᴛʜ ᴏᴛʜᴇʀ ʙᴏᴛꜱ, ꜱᴏ ɪ ᴄᴀɴ'ᴛ ꜱᴀᴠᴇ ᴛʜɪꜱ ᴍᴇꜱꜱᴀɢᴇ "
                "ʟɪᴋᴇ ɪ ᴜꜱᴜᴀʟʟʏ ᴡᴏᴜʟᴅ - ᴅᴏ ʏᴏᴜ ᴍɪɴᴅ ꜰᴏʀᴡᴀʀᴅɪɴɢ ɪᴛ ᴀɴᴅ "
                "ᴛʜᴇɴ ꜱᴀᴠɪɴɢ ᴛʜᴀᴛ ɴᴇᴡ ᴍᴇꜱꜱᴀɢᴇ? ᴛʜᴀɴᴋꜱ ʙᴀʙʏ🥀!",
            )
        return


@user_admin
@connection_status
def clear(update: Update, context: CallbackContext):
    args = context.args
    chat_id = update.effective_chat.id
    if len(args) >= 1:
        notename = args[0].lower()

        if sql.rm_note(chat_id, notename):
            update.effective_message.reply_text("ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ʀᴇᴍᴏᴠᴇᴅ ɴᴏᴛᴇ ʙᴀʙʏ🥀.")
        else:
            update.effective_message.reply_text("ᴛʜᴀᴛ'ꜱ ɴᴏᴛ ᴀ ɴᴏᴛᴇ ɪɴ ᴍʏ ᴅᴀᴛᴀʙᴀꜱᴇ ʙᴀʙʏ🥀!")


def clearall(update: Update, context: CallbackContext):
    chat = update.effective_chat
    user = update.effective_user
    member = chat.get_member(user.id)
    if member.status != "creator" and user.id not in DRAGONS:
        update.effective_message.reply_text(
            "ᴏɴʟʏ ᴛʜᴇ ᴄʜᴀᴛ ᴏᴡɴᴇʀ ᴄᴀɴ ᴄʟᴇᴀʀ ᴀʟʟ ɴᴏᴛᴇꜱ ᴀᴛ ᴏɴᴄᴇ ʙᴀʙʏ🥀.",
        )
    else:
        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Delete all notes",
                        callback_data="notes_rmall",
                    ),
                ],
                [InlineKeyboardButton(text="Cancel", callback_data="notes_cancel")],
            ],
        )
        update.effective_message.reply_text(
            f"ᴀʀᴇ ʏᴏᴜ ꜱᴜʀᴇ ʏᴏᴜ ᴡᴏᴜʟᴅ ʟɪᴋᴇ ᴛᴏ ᴄʟᴇᴀʀ ᴀʟʟ ɴᴏᴛᴇꜱ ɪɴ {chat.title}? ᴛʜɪꜱ ᴀᴄᴛɪᴏɴ ᴄᴀɴɴᴏᴛ ʙᴇ ᴜɴᴅᴏɴᴇ ʙᴀʙʏ🥀.",
            reply_markup=buttons,
            parse_mode=ParseMode.MARKDOWN,
        )


def clearall_btn(update: Update, context: CallbackContext):
    query = update.callback_query
    chat = update.effective_chat
    message = update.effective_message
    member = chat.get_member(query.from_user.id)
    if query.data == "notes_rmall":
        if member.status == "creator" or query.from_user.id in DRAGONS:
            note_list = sql.get_all_chat_notes(chat.id)
            try:
                for notename in note_list:
                    note = notename.name.lower()
                    sql.rm_note(chat.id, note)
                message.edit_text("ᴅᴇʟᴇᴛᴇᴅ ᴀʟʟ ɴᴏᴛᴇꜱ ʙᴀʙʏ🥀.")
            except BadRequest:
                return

        if member.status == "administrator":
            query.answer("ᴏɴʟʏ ᴏᴡɴᴇʀ ᴏꜰ ᴛʜᴇ ᴄʜᴀᴛ ᴄᴀɴ ᴅᴏ ᴛʜɪꜱ ʙᴀʙʏ🥀.")

        if member.status == "member":
            query.answer("ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʙᴇ ᴀᴅᴍɪɴ ᴛᴏ ᴅᴏ ᴛʜɪꜱ ʙᴀʙʏ🥀.")
    elif query.data == "notes_cancel":
        if member.status == "creator" or query.from_user.id in DRAGONS:
            message.edit_text("ᴄʟᴇᴀʀɪɴɢ ᴏꜰ ᴀʟʟ ɴᴏᴛᴇꜱ ʜᴀꜱ ʙᴇᴇɴ ᴄᴀɴᴄᴇʟʟᴇᴅ ʙᴀʙʏ🥀.")
            return
        if member.status == "administrator":
            query.answer("ᴏɴʟʏ ᴏᴡɴᴇʀ ᴏꜰ ᴛʜᴇ ᴄʜᴀᴛ ᴄᴀɴ ᴅᴏ ᴛʜɪꜱ ʙᴀʙʏ🥀.")
        if member.status == "member":
            query.answer("ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʙᴇ ᴀᴅᴍɪɴ ᴛᴏ ᴅᴏ ᴛʜɪꜱ ʙᴀʙʏ🥀.")


@connection_status
def list_notes(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    note_list = sql.get_all_chat_notes(chat_id)
    notes = len(note_list) + 1
    msg = "ɢᴇᴛ ɴᴏᴛᴇ ʙʏ `/notenumber` ᴏʀ `#notename` ʙᴀʙʏ🥀 \n\n  *ɪᴅ*    *ɴᴏᴛᴇ* \n"
    for note_id, note in zip(range(1, notes), note_list):
        if note_id < 10:
            note_name = f"`{note_id:2}.`  `#{(note.name.lower())}`\n"
        else:
            note_name = f"`{note_id}.`  `#{(note.name.lower())}`\n"
        if len(msg) + len(note_name) > MAX_MESSAGE_LENGTH:
            update.effective_message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            msg = ""
        msg += note_name

    if not note_list:
        try:
            update.effective_message.reply_text("ɴᴏ ɴᴏᴛᴇꜱ ɪɴ ᴛʜɪꜱ ᴄʜᴀᴛ ʙᴀʙʏ🥀!")
        except BadRequest:
            update.effective_message.reply_text("ɴᴏ ɴᴏᴛᴇꜱ ɪɴ ᴛʜɪꜱ ᴄʜᴀᴛ ʙᴀʙʏ🥀!", quote=False)

    elif len(msg) != 0:
        update.effective_message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)


def __import_data__(chat_id, data):
    failures = []
    for notename, notedata in data.get("extra", {}).items():
        match = FILE_MATCHER.match(notedata)
        matchsticker = STICKER_MATCHER.match(notedata)
        matchbtn = BUTTON_MATCHER.match(notedata)
        matchfile = MYFILE_MATCHER.match(notedata)
        matchphoto = MYPHOTO_MATCHER.match(notedata)
        matchaudio = MYAUDIO_MATCHER.match(notedata)
        matchvoice = MYVOICE_MATCHER.match(notedata)
        matchvideo = MYVIDEO_MATCHER.match(notedata)
        matchvn = MYVIDEONOTE_MATCHER.match(notedata)

        if match:
            failures.append(notename)
            notedata = notedata[match.end() :].strip()
            if notedata:
                sql.add_note_to_db(chat_id, notename[1:], notedata, sql.Types.TEXT)
        elif matchsticker:
            content = notedata[matchsticker.end() :].strip()
            if content:
                sql.add_note_to_db(
                    chat_id,
                    notename[1:],
                    notedata,
                    sql.Types.STICKER,
                    file=content,
                )
        elif matchbtn:
            parse = notedata[matchbtn.end() :].strip()
            notedata = parse.split("<###button###>")[0]
            buttons = parse.split("<###button###>")[1]
            buttons = ast.literal_eval(buttons)
            if buttons:
                sql.add_note_to_db(
                    chat_id,
                    notename[1:],
                    notedata,
                    sql.Types.BUTTON_TEXT,
                    buttons=buttons,
                )
        elif matchfile:
            file = notedata[matchfile.end() :].strip()
            file = file.split("<###TYPESPLIT###>")
            notedata = file[1]
            content = file[0]
            if content:
                sql.add_note_to_db(
                    chat_id,
                    notename[1:],
                    notedata,
                    sql.Types.DOCUMENT,
                    file=content,
                )
        elif matchphoto:
            photo = notedata[matchphoto.end() :].strip()
            photo = photo.split("<###TYPESPLIT###>")
            notedata = photo[1]
            content = photo[0]
            if content:
                sql.add_note_to_db(
                    chat_id,
                    notename[1:],
                    notedata,
                    sql.Types.PHOTO,
                    file=content,
                )
        elif matchaudio:
            audio = notedata[matchaudio.end() :].strip()
            audio = audio.split("<###TYPESPLIT###>")
            notedata = audio[1]
            content = audio[0]
            if content:
                sql.add_note_to_db(
                    chat_id,
                    notename[1:],
                    notedata,
                    sql.Types.AUDIO,
                    file=content,
                )
        elif matchvoice:
            voice = notedata[matchvoice.end() :].strip()
            voice = voice.split("<###TYPESPLIT###>")
            notedata = voice[1]
            content = voice[0]
            if content:
                sql.add_note_to_db(
                    chat_id,
                    notename[1:],
                    notedata,
                    sql.Types.VOICE,
                    file=content,
                )
        elif matchvideo:
            video = notedata[matchvideo.end() :].strip()
            video = video.split("<###TYPESPLIT###>")
            notedata = video[1]
            content = video[0]
            if content:
                sql.add_note_to_db(
                    chat_id,
                    notename[1:],
                    notedata,
                    sql.Types.VIDEO,
                    file=content,
                )
        elif matchvn:
            video_note = notedata[matchvn.end() :].strip()
            video_note = video_note.split("<###TYPESPLIT###>")
            notedata = video_note[1]
            content = video_note[0]
            if content:
                sql.add_note_to_db(
                    chat_id,
                    notename[1:],
                    notedata,
                    sql.Types.VIDEO_NOTE,
                    file=content,
                )
        else:
            sql.add_note_to_db(chat_id, notename[1:], notedata, sql.Types.TEXT)

    if failures:
        with BytesIO(str.encode("\n".join(failures))) as output:
            output.name = "failed_imports.txt"
            dispatcher.bot.send_document(
                chat_id,
                document=output,
                filename="failed_imports.txt",
                caption="ᴛʜᴇꜱᴇ ꜰɪʟᴇꜱ/ᴘʜᴏᴛᴏꜱ ꜰᴀɪʟᴇᴅ ᴛᴏ ɪᴍᴘᴏʀᴛ ᴅᴜᴇ ᴛᴏ ᴏʀɪɢɪɴᴀᴛɪɴɢ "
                "ꜰʀᴏᴍ ᴀɴᴏᴛʜᴇʀ ʙᴏᴛ ʙᴀʙʏ🥀. ᴛʜɪꜱ ɪꜱ ᴀ ᴛᴇʟᴇɢʀᴀᴍ ᴀᴘɪ ʀᴇꜱᴛʀɪᴄᴛɪᴏɴ, ᴀɴᴅ ᴄᴀɴ'ᴛ "
                "ʙᴇ ᴀᴠᴏɪᴅᴇᴅ. ꜱᴏʀʀʏ ꜰᴏʀ ᴛʜᴇ ɪɴᴄᴏɴᴠᴇɴɪᴇɴᴄᴇ ʙᴀʙʏ🥀!",
            )


def __stats__():
    return f"× {sql.num_notes()} ɴᴏᴛᴇꜱ, ᴀᴄʀᴏꜱꜱ {sql.num_chats()} ᴄʜᴀᴛꜱ ʙᴀʙʏ🥀."


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)


def __chat_settings__(chat_id, user_id):
    notes = sql.get_all_chat_notes(chat_id)
    return f"ᴛʜᴇʀᴇ ᴀʀᴇ `{len(notes)}` ɴᴏᴛᴇꜱ ɪɴ ᴛʜɪꜱ ᴄʜᴀᴛ ʙᴀʙʏ🥀."


__help__ = """
» `/get` <notename>*:* ɢᴇᴛ ᴛʜᴇ ɴᴏᴛᴇ ᴡɪᴛʜ ᴛʜɪꜱ ɴᴏᴛᴇɴᴀᴍᴇ
» #<notename>*:* ꜱᴀᴍᴇ ᴀꜱ /get
» `/notes` or `/saved`*:* ʟɪꜱᴛ ᴀʟʟ ꜱᴀᴠᴇᴅ ɴᴏᴛᴇꜱ ɪɴ ᴛʜɪꜱ ᴄʜᴀᴛ
» `/number` *:* ᴡɪʟʟ ᴘᴜʟʟ ᴛʜᴇ ɴᴏᴛᴇ ᴏꜰ ᴛʜᴀᴛ ɴᴜᴍʙᴇʀ ɪɴ ᴛʜᴇ ʟɪꜱᴛ
ɪꜰ ʏᴏᴜ ᴡᴏᴜʟᴅ ʟɪᴋᴇ ᴛᴏ ʀᴇᴛʀɪᴇᴠᴇ ᴛʜᴇ ᴄᴏɴᴛᴇɴᴛꜱ ᴏꜰ ᴀ ɴᴏᴛᴇ ᴡɪᴛʜᴏᴜᴛ ᴀɴʏ ꜰᴏʀᴍᴀᴛᴛɪɴɢ, ᴜꜱᴇ `/get <ɴᴏᴛᴇɴᴀᴍᴇ> ɴᴏꜰᴏʀᴍᴀᴛ`. ᴛʜɪꜱ ᴄᴀɴ \
ʙᴇ ᴜꜱᴇꜰᴜʟ ᴡʜᴇɴ ᴜᴘᴅᴀᴛɪɴɢ ᴀ ᴄᴜʀʀᴇɴᴛ ɴᴏᴛᴇ

*Admins only:*
» `/save` <notename> <notedata>*:* ꜱᴀᴠᴇꜱ ɴᴏᴛᴇᴅᴀᴛᴀ ᴀꜱ ᴀ ɴᴏᴛᴇ ᴡɪᴛʜ ɴᴀᴍᴇ ɴᴏᴛᴇɴᴀᴍᴇ
ᴀ ʙᴜᴛᴛᴏɴ ᴄᴀɴ ʙᴇ ᴀᴅᴅᴇᴅ ᴛᴏ ᴀ ɴᴏᴛᴇ ʙʏ ᴜꜱɪɴɢ ꜱᴛᴀɴᴅᴀʀᴅ ᴍᴀʀᴋᴅᴏᴡɴ ʟɪɴᴋ ꜱʏɴᴛᴀx - ᴛʜᴇ ʟɪɴᴋ ꜱʜᴏᴜʟᴅ ᴊᴜꜱᴛ ʙᴇ ᴘʀᴇᴘᴇɴᴅᴇᴅ ᴡɪᴛʜ ᴀ \
`buttonurl:` ꜱᴇᴄᴛɪᴏɴ, ᴀꜱ ꜱᴜᴄʜ: `[ꜱᴏᴍᴇʟɪɴᴋ](ʙᴜᴛᴛᴏɴᴜʀʟ:ᴇxᴀᴍᴘʟᴇ.ᴄᴏᴍ)`. ᴄʜᴇᴄᴋ `/markdownhelp` ꜰᴏʀ ᴍᴏʀᴇ ɪɴꜰᴏ
» `/save` <notename>*:* ꜱᴀᴠᴇ ᴛʜᴇ ʀᴇᴘʟɪᴇᴅ ᴍᴇꜱꜱᴀɢᴇ ᴀꜱ ᴀ ɴᴏᴛᴇ ᴡɪᴛʜ ɴᴀᴍᴇ ɴᴏᴛᴇɴᴀᴍᴇ
ꜱᴇᴘᴀʀᴀᴛᴇ ᴅɪꜰꜰ ʀᴇᴘʟɪᴇꜱ ʙʏ `%%%` ᴛᴏ ɢᴇᴛ ʀᴀɴᴅᴏᴍ ɴᴏᴛᴇꜱ
 *ᴇxᴀᴍᴘʟᴇ:*
 `/save ɴᴏᴛᴇɴᴀᴍᴇ
ʀᴇᴘʟʏ 1
%%% 
ʀᴇᴘʟʏ 2
%%%
ʀᴇᴘʟʏ 3`
» `/clear` <notename>*:* ᴄʟᴇᴀʀ ɴᴏᴛᴇ ᴡɪᴛʜ ᴛʜɪꜱ ɴᴀᴍᴇ
» `/removeallnotes`*:* ʀᴇᴍᴏᴠᴇꜱ ᴀʟʟ ɴᴏᴛᴇꜱ ꜰʀᴏᴍ ᴛʜᴇ ɢʀᴏᴜᴘ

 *ɴᴏᴛᴇ:* ɴᴏᴛᴇ ɴᴀᴍᴇꜱ ᴀʀᴇ ᴄᴀꜱᴇ-ɪɴꜱᴇɴꜱɪᴛɪᴠᴇ, ᴀɴᴅ ᴛʜᴇʏ ᴀʀᴇ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴄᴏɴᴠᴇʀᴛᴇᴅ ᴛᴏ ʟᴏᴡᴇʀᴄᴀꜱᴇ ʙᴇꜰᴏʀᴇ ɢᴇᴛᴛɪɴɢ ꜱᴀᴠᴇᴅ.
"""

__mod_name__ = "NOTES"

GET_HANDLER = CommandHandler("get", cmd_get, run_async=True)
HASH_GET_HANDLER = MessageHandler(Filters.regex(r"^#[^\s]+"), hash_get, run_async=True)
SLASH_GET_HANDLER = MessageHandler(Filters.regex(r"^/\d+$"), slash_get, run_async=True)
SAVE_HANDLER = CommandHandler("save", save, run_async=True)
DELETE_HANDLER = CommandHandler("clear", clear, run_async=True)
LIST_HANDLER = DisableAbleCommandHandler(
    ["notes", "saved"], list_notes, admin_ok=True, run_async=True
)
CLEARALL = DisableAbleCommandHandler("removeallnotes", clearall, run_async=True)
CLEARALL_BTN = CallbackQueryHandler(clearall_btn, pattern=r"notes_.*", run_async=True)

dispatcher.add_handler(GET_HANDLER)
dispatcher.add_handler(SAVE_HANDLER)
dispatcher.add_handler(LIST_HANDLER)
dispatcher.add_handler(DELETE_HANDLER)
dispatcher.add_handler(HASH_GET_HANDLER)
dispatcher.add_handler(SLASH_GET_HANDLER)
dispatcher.add_handler(CLEARALL)
dispatcher.add_handler(CLEARALL_BTN)
