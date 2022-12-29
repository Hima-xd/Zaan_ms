import logging
import time

from pyrogram import filters
from pyrogram.errors.exceptions.bad_request_400 import (
    ChatAdminRequired,
    PeerIdInvalid,
    UsernameNotOccupied,
    UserNotParticipant,
)
from pyrogram.types import ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup

from KRISTY import DRAGONS as SUDO_USERS
from KRISTY import pbot
from KRISTY.modules.sql import forceSubscribe_sql as sql

logging.basicConfig(level=logging.INFO)

static_data_filter = filters.create(
    lambda _, __, query: query.data == "onUnMuteRequest"
)


@pbot.on_callback_query(static_data_filter)
def _onUnMuteRequest(client, cb):
    user_id = cb.from_user.id
    chat_id = cb.message.chat.id
    chat_db = sql.fs_settings(chat_id)
    if chat_db:
        channel = chat_db.channel
        chat_member = client.get_chat_member(chat_id, user_id)
        if chat_member.restricted_by:
            if chat_member.restricted_by.id == (client.get_me()).id:
                try:
                    client.get_chat_member(channel, user_id)
                    client.unban_chat_member(chat_id, user_id)
                    cb.message.delete()
                    # if cb.message.reply_to_message.from_user.id == user_id:
                    # cb.message.delete()
                except UserNotParticipant:
                    client.answer_callback_query(
                        cb.id,
                        text=f"ᴊᴏɪɴ ᴏᴜʀ @{channel} ᴄʜᴀɴɴᴇʟ ᴀɴᴅ ᴘʀᴇꜱꜱ 'ᴜɴᴍᴜᴛᴇ ᴍᴇ' ʙᴜᴛᴛᴏɴ ʙᴀʙʏ🥀.",
                        show_alert=True,
                    )
            else:
                client.answer_callback_query(
                    cb.id,
                    text="❗ ʏᴏᴜ ʜᴀᴠᴇ ʙᴇᴇɴ ᴍᴜᴛᴇᴅ ʙʏ ᴀᴅᴍɪɴꜱ ᴅᴜᴇ ᴛᴏ ꜱᴏᴍᴇ ᴏᴛʜᴇʀ ʀᴇᴀꜱᴏɴ ʙᴀʙʏ🥀.",
                    show_alert=True,
                )
        else:
            if (not client.get_chat_member(chat_id, (client.get_me()).id).status == "administrator"
            ):
                client.send_message(
                    chat_id,
                    f" **{cb.from_user.mention} ɪꜱ ᴛʀʏɪɴɢ ᴛᴏ ᴜɴᴍᴜᴛᴇ ʜɪᴍꜱᴇʟꜰ ʙᴜᴛ ɪ ᴄᴀɴ'ᴛ ᴜɴᴍᴜᴛᴇ ʜɪᴍ ʙᴇᴄᴀᴜꜱᴇ ɪ ᴀᴍ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ ɪɴ ᴛʜɪꜱ ᴄʜᴀᴛ ᴀᴅᴅ ᴍᴇ ᴀꜱ ᴀᴅᴍɪɴ ᴀɢᴀɪɴ ʙᴀʙʏ🥀.**\n__#ʟᴇᴀᴠɪɴɢ ᴛʜɪꜱ ᴄʜᴀᴛ...__",
                )

            else:
                client.answer_callback_query(
                    cb.id,
                    text=" ᴡᴀʀɴɪɴɢ! ᴅᴏɴ'ᴛ ᴘʀᴇꜱꜱ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ᴡʜᴇɴ ʏᴏᴜ ᴄᴀɴ ᴛᴀʟᴋ ʙᴀʙʏ🥀.",
                    show_alert=True,
                )


@pbot.on_message(filters.text & ~filters.private, group=1)
def _check_member(client, message):
    chat_id = message.chat.id
    chat_db = sql.fs_settings(chat_id)
    if chat_db:
        user_id = message.from_user.id
        if (not client.get_chat_member(chat_id, user_id).status in ("administrator", "creator")
            and not user_id in SUDO_USERS
        ):
            channel = chat_db.channel
            try:
                client.get_chat_member(channel, user_id)
            except UserNotParticipant:
                try:
                    sent_message = message.reply_text(
                        "ᴡᴇʟᴄᴏᴍᴇ {} 🙏 \n **ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ ᴊᴏɪɴᴇᴅ ᴏᴜʀ @{} ᴄʜᴀɴɴᴇʟ ʏᴇᴛ ʙᴀʙʏ🥀**👷 \n \nᴘʟᴇᴀꜱᴇ ᴊᴏɪɴ [ᴏᴜʀ ᴄʜᴀɴɴᴇʟ](https://t.me/{}) ᴀɴᴅ ʜɪᴛ ᴛʜᴇ **ᴜɴᴍᴜᴛᴇ ᴍᴇ** ʙᴜᴛᴛᴏɴ. \n \n ".format(
                            message.from_user.mention, channel, channel
                        ),
                        disable_web_page_preview=True,
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        "ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ",
                                        url="https://t.me/{}".format(channel),
                                    )
                                ],
                                [
                                    InlineKeyboardButton(
                                        "ᴜɴᴍᴜᴛᴇ ᴍᴇ", callback_data="onUnMuteRequest"
                                    )
                                ],
                            ]
                        ),
                    )
                    client.restrict_chat_member(
                        chat_id, user_id, ChatPermissions(can_send_messages=False)
                    )
                except ChatAdminRequired:
                    sent_message.edit(
                        " **ʙᴏᴛ ɪꜱ ɴᴏᴛ ᴀᴅᴍɪɴ ʜᴇʀᴇ ʙᴀʙʏ🥀..**\n__ɢɪᴠᴇ ᴍᴇ ʙᴀɴ ᴘᴇʀᴍɪꜱꜱɪᴏɴꜱ ᴀɴᴅ ʀᴇᴛʀʏ.. \n#ᴇɴᴅɪɴɢ ꜰꜱᴜʙ...__"
                    )

            except ChatAdminRequired:
                client.send_message(
                    chat_id,
                    text=f" **ɪ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ ᴏꜰ @{channel} ᴄʜᴀɴɴᴇʟ ʙᴀʙʏ🥀.**\n__ɢɪᴠᴇ ᴍᴇ ᴀᴅᴍɪɴ ᴏꜰ ᴛʜᴀᴛ ᴄʜᴀɴɴᴇʟ ᴀɴᴅ ʀᴇᴛʀʏ.\n#ᴇɴᴅɪɴɢ ꜰꜱᴜʙ...__",
                )


@pbot.on_message(filters.command(["forcesubscribe", "fsub"]) & ~filters.private)
def config(client, message):
    user = client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status == "creator" or user.user.id in SUDO_USERS:
        chat_id = message.chat.id
        if len(message.command) > 1:
            input_str = message.command[1]
            input_str = input_str.replace("@", "")
            if input_str.lower() in ("off", "no", "disable"):
                sql.disapprove(chat_id)
                message.reply_text(" **ꜰᴏʀᴄᴇ ꜱᴜʙꜱᴄʀɪʙᴇ ɪꜱ ᴅɪꜱᴀʙʟᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ʙᴀʙʏ🥀.**")
            elif input_str.lower() in ("clear"):
                sent_message = message.reply_text(
                    "**ᴜɴᴍᴜᴛɪɴɢ ᴀʟʟ ᴍᴇᴍʙᴇʀꜱ ᴡʜᴏ ᴀʀᴇ ᴍᴜᴛᴇᴅ ʙʏ ᴍᴇ ʙᴀʙʏ🥀...**"
                )
                try:
                    for chat_member in client.get_chat_members(
                        message.chat.id, filter="restricted"
                    ):
                        if chat_member.restricted_by.id == (client.get_me()).id:
                            client.unban_chat_member(chat_id, chat_member.user.id)
                            time.sleep(1)
                    sent_message.edit(" **ᴜɴᴍᴜᴛᴇᴅ ᴀʟʟ ᴍᴇᴍʙᴇʀꜱ ᴡʜᴏ ᴀʀᴇ ᴍᴜᴛᴇᴅ ʙʏ ᴍᴇ ʙᴀʙʏ🥀.**")
                except ChatAdminRequired:
                    sent_message.edit(
                        "**ɪ ᴀᴍ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ ɪɴ ᴛʜɪꜱ ᴄʜᴀᴛ ʙᴀʙʏ🥀.**\n__ɪ ᴄᴀɴ'ᴛ ᴜɴᴍᴜᴛᴇ ᴍᴇᴍʙᴇʀꜱ ʙᴇᴄᴀᴜꜱᴇ ɪ ᴀᴍ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ ɪɴ ᴛʜɪꜱ ᴄʜᴀᴛ ᴍᴀᴋᴇ ᴍᴇ ᴀᴅᴍɪɴ ᴡɪᴛʜ ʙᴀɴ ᴜꜱᴇʀ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ʙᴀʙʏ🥀.__"
                    )
            else:
                try:
                    client.get_chat_member(input_str, "me")
                    sql.add_channel(chat_id, input_str)
                    message.reply_text(
                        f" **ꜰᴏʀᴄᴇ ꜱᴜʙꜱᴄʀɪʙᴇ ɪꜱ ᴇɴᴀʙʟᴇᴅ ʙᴀʙʏ🥀**\n__ꜰᴏʀᴄᴇ ꜱᴜʙꜱᴄʀɪʙᴇ ɪꜱ ᴇɴᴀʙʟᴇᴅ, ᴀʟʟ ᴛʜᴇ ɢʀᴏᴜᴘ ᴍᴇᴍʙᴇʀꜱ ʜᴀᴠᴇ ᴛᴏ ꜱᴜʙꜱᴄʀɪʙᴇ ᴛʜɪꜱ [ᴄʜᴀɴɴᴇʟ](ʜᴛᴛᴘꜱ://ᴛ.ᴍᴇ/{input_str}) ɪɴ ᴏʀᴅᴇʀ ᴛᴏ ꜱᴇɴᴅ ᴍᴇꜱꜱᴀɢᴇꜱ ɪɴ ᴛʜɪꜱ ɢʀᴏᴜᴘ ʙᴀʙʏ🥀.__",
                        disable_web_page_preview=True,
                    )
                except UserNotParticipant:
                    message.reply_text(
                        f" **ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ ɪɴ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ ʙᴀʙʏ🥀**\n__ɪ ᴀᴍ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ ɪɴ ᴛʜᴇ [ᴄʜᴀɴɴᴇʟ](https://t.me/{input_str}). ᴀᴅᴅ ᴍᴇ ᴀꜱ ᴀ ᴀᴅᴍɪɴ ɪɴ ᴏʀᴅᴇʀ ᴛᴏ ᴇɴᴀʙʟᴇ ꜰᴏʀᴄᴇꜱᴜʙꜱᴄʀɪʙᴇ.__",
                        disable_web_page_preview=True,
                    )
                except (UsernameNotOccupied, PeerIdInvalid):
                    message.reply_text(f"**ɪɴᴠᴀʟɪᴅ ᴄʜᴀɴɴᴇʟ ᴜꜱᴇʀɴᴀᴍᴇ ʙᴀʙʏ🥀.**")
                except Exception as err:
                    message.reply_text(f"**ᴇʀʀᴏʀ:** ```{err}``` ʙᴀʙʏ🥀")
        else:
            if sql.fs_settings(chat_id):
                message.reply_text(
                    f" **ꜰᴏʀᴄᴇ ꜱᴜʙꜱᴄʀɪʙᴇ ɪꜱ ᴇɴᴀʙʟᴇᴅ ɪɴ ᴛʜɪꜱ ᴄʜᴀᴛ ʙᴀʙʏ🥀.**\n__ꜰᴏʀ ᴛʜɪꜱ [Channel](https://t.me/{sql.fs_settings(chat_id).channel})__",
                    disable_web_page_preview=True,
                )
            else:
                message.reply_text("**ꜰᴏʀᴄᴇ ꜱᴜʙꜱᴄʀɪʙᴇ ɪꜱ ᴅɪꜱᴀʙʟᴇᴅ ɪɴ ᴛʜɪꜱ ᴄʜᴀᴛ ʙᴀʙʏ🥀.**")
    else:
        message.reply_text(
            "❗ **ɢʀᴏᴜᴘ ᴄʀᴇᴀᴛᴏʀ ʀᴇQᴜɪʀᴇᴅ**\n__ʏᴏᴜ ʜᴀᴠᴇ ᴛᴏ ʙᴇ ᴛʜᴇ ɢʀᴏᴜᴘ ᴄʀᴇᴀᴛᴏʀ ᴛᴏ ᴅᴏ ᴛʜᴀᴛ ʙᴀʙʏ🥀.__"
        )


__help__ = """
» `/fsub` {channel username} - ᴛᴏ ᴛᴜʀɴ ᴏɴ ᴀɴᴅ ꜱᴇᴛᴜᴘ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ.
  💡ᴅᴏ ᴛʜɪꜱ ꜰɪʀꜱᴛ...
» `/fsub` - ᴛᴏ ɢᴇᴛ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ꜱᴇᴛᴛɪɴɢꜱ.
» `/fsub disable` - ᴛᴏ ᴛᴜʀɴ ᴏꜰ ꜰᴏʀᴄᴇꜱᴜʙꜱᴄʀɪʙᴇ..
💡ɪꜰ ʏᴏᴜ ᴅɪꜱᴀʙʟᴇ ꜰꜱᴜʙ, ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ꜱᴇᴛ ᴀɢᴀɪɴ ꜰᴏʀ ᴡᴏʀᴋɪɴɢ.. /fsub {channel username} 
» `/fsub clear` - ᴛᴏ ᴜɴᴍᴜᴛᴇ ᴀʟʟ ᴍᴇᴍʙᴇʀꜱ ᴡʜᴏ ᴍᴜᴛᴇᴅ ʙʏ ᴍᴇ.
*ꜰᴇᴅᴇʀᴀᴛɪᴏɴ*

ᴇᴠᴇʀʏᴛʜɪɴɢ ɪꜱ ꜰᴜɴ, ᴜɴᴛɪʟ ᴀ ꜱᴘᴀᴍᴍᴇʀ ꜱᴛᴀʀᴛꜱ ᴇɴᴛᴇʀɪɴɢ ʏᴏᴜʀ ɢʀᴏᴜᴘ, ᴀɴᴅ ʏᴏᴜ ʜᴀᴠᴇ ᴛᴏ ʙʟᴏᴄᴋ ɪᴛ. ᴛʜᴇɴ ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ꜱᴛᴀʀᴛ ʙᴀɴɴɪɴɢ ᴍᴏʀᴇ, ᴀɴᴅ ᴍᴏʀᴇ, ᴀɴᴅ ɪᴛ ʜᴜʀᴛꜱ.
ʙᴜᴛ ᴛʜᴇɴ ʏᴏᴜ ʜᴀᴠᴇ ᴍᴀɴʏ ɢʀᴏᴜᴘꜱ, ᴀɴᴅ ʏᴏᴜ ᴅᴏɴ'ᴛ ᴡᴀɴᴛ ᴛʜɪꜱ ꜱᴘᴀᴍᴍᴇʀ ᴛᴏ ʙᴇ ɪɴ ᴏɴᴇ ᴏꜰ ʏᴏᴜʀ ɢʀᴏᴜᴘꜱ - ʜᴏᴡ ᴄᴀɴ ʏᴏᴜ ᴅᴇᴀʟ? ᴅᴏ ʏᴏᴜ ʜᴀᴠᴇ ᴛᴏ ᴍᴀɴᴜᴀʟʟʏ ʙʟᴏᴄᴋ ɪᴛ, ɪɴ ᴀʟʟ ʏᴏᴜʀ ɢʀᴏᴜᴘꜱ?\n
*ɴᴏ ʟᴏɴɢᴇʀ!* ᴡɪᴛʜ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ, ʏᴏᴜ ᴄᴀɴ ᴍᴀᴋᴇ ᴀ ʙᴀɴ ɪɴ ᴏɴᴇ ᴄʜᴀᴛ ᴏᴠᴇʀʟᴀᴘ ᴡɪᴛʜ ᴀʟʟ ᴏᴛʜᴇʀ ᴄʜᴀᴛꜱ.\n
ʏᴏᴜ ᴄᴀɴ ᴇᴠᴇɴ ᴅᴇꜱɪɢɴᴀᴛᴇ ꜰᴇᴅᴇʀᴀᴛɪᴏɴ ᴀᴅᴍɪɴꜱ, ꜱᴏ ʏᴏᴜʀ ᴛʀᴜꜱᴛᴇᴅ ᴀᴅᴍɪɴ ᴄᴀɴ ʙᴀɴ ᴀʟʟ ᴛʜᴇ ꜱᴘᴀᴍᴍᴇʀꜱ ꜰʀᴏᴍ ᴄʜᴀᴛꜱ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴘʀᴏᴛᴇᴄᴛ.\n

*ᴄᴏᴍᴍᴀɴᴅꜱ:*\n

ꜰᴇᴅꜱ ᴀʀᴇ ɴᴏᴡ ᴅɪᴠɪᴅᴇᴅ ɪɴᴛᴏ 3 ꜱᴇᴄᴛɪᴏɴꜱ ꜰᴏʀ ʏᴏᴜʀ ᴇᴀꜱᴇ.



» `/fedownerhelp`*:* ᴘʀᴏᴠɪᴅᴇꜱ ʜᴇʟᴘ ꜰᴏʀ ꜰᴇᴅ ᴄʀᴇᴀᴛɪᴏɴ ᴀɴᴅ ᴏᴡɴᴇʀ ᴏɴʟʏ ᴄᴏᴍᴍᴀɴᴅꜱ
» `/fedadminhelp`*:* ᴘʀᴏᴠɪᴅᴇꜱ ʜᴇʟᴘ ꜰᴏʀ ꜰᴇᴅ ᴀᴅᴍɪɴɪꜱᴛʀᴀᴛɪᴏɴ ᴄᴏᴍᴍᴀɴᴅꜱ
» `/feduserhelp`*:* ᴘʀᴏᴠɪᴅᴇꜱ ʜᴇʟᴘ ꜰᴏʀ ᴄᴏᴍᴍᴀɴᴅꜱ ᴀɴʏᴏɴᴇ ᴄᴀɴ ᴜꜱᴇ
"""
__mod_name__ = "F-SUB/FEDS"
