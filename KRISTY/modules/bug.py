from datetime import datetime

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from KRISTY import OWNER_ID, START_IMG, SUPPORT_CHAT, pbot
from KRISTY.utils.errors import capture_err


def content(msg: Message) -> [None, str]:
    text_to_return = msg.text

    if msg.text is None:
        return None
    if " " in text_to_return:
        try:
            return msg.text.split(None, 1)[1]
        except IndexError:
            return None
    else:
        return None


@pbot.on_message(filters.command("bug"))
@capture_err
async def bug(_, msg: Message):
    if msg.chat.username:
        chat_username = f"@{msg.chat.username} [`{msg.chat.id}`]"
    else:
        chat_username = f"ᴩʀɪᴠᴀᴛᴇ ɢʀᴏᴜᴩ [`{msg.chat.id}`]"
    bugs = content(msg)
    datetimes_fmt = "%d-%m-%Y"
    datetimes = datetime.utcnow().strftime(datetimes_fmt)

    bug_report = f"""
**#ʙᴜɢ**

ᴜsᴇʀ ɪᴅ : `{msg.from_user.id}`
ᴄʜᴀᴛ : @{chat_username}
ʀᴇᴩᴏʀᴛᴇᴅ ʙʏ : {msg.from_user.mention}

ʙᴜɢ : `{bugs}`

ᴇᴠᴇɴᴛ sᴛᴀᴍᴩ : `{datetimes}`"""

    if msg.chat.type == ChatType.PRIVATE:
        return await msg.reply_text("<b>» ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪs ᴏɴʟʏ ғᴏʀ ɢʀᴏᴜᴩs ʙᴀʙʏ🥀.</b>")

    elif msg.from_user.id == OWNER_ID:
        return await msg.reply_text(
                "<b>» ᴀʀᴇ ʏᴏᴜ ᴄᴏᴍᴇᴅʏ ᴍᴇ ʙᴀʙʏ🥀, ʏᴏᴜ'ʀᴇ ᴛʜᴇ ᴏᴡɴᴇʀ ᴏғ ᴛʜᴇ ʙᴏᴛ.</b>",
            )
    else:
        if bugs:
            await msg.reply_text(
                f"<b>ʙᴜɢ ʀᴇᴩᴏʀᴛ :</b> `{bugs}`\n\n"
                "<b>» ʙᴜɢ sᴜᴄᴄᴇssғᴜʟʟʏ ʀᴇᴩᴏʀᴛᴇᴅ ᴀᴛ sᴜᴩᴩᴏʀᴛ ᴄʜᴀᴛ ʙᴀʙʏ🥀!!</b>",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("• ᴄʟᴏsᴇ •", callback_data="close")]]
                ),
            )
            await pbot.send_photo(
                SUPPORT_CHAT,
                photo=START_IMG,
                caption=bug_report,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("• ᴠɪᴇᴡ ʙᴜɢ •", url=msg.link),
                            InlineKeyboardButton("• ᴄʟᴏsᴇ •", callback_data="close_")
                        ],
                    ]
                ),
            )
        else:
            await msg.reply_text(
                f"<b>» ɴᴏ ʙᴜɢ ᴛᴏ ʀᴇᴩᴏʀᴛ ʙᴀʙʏ🥀!</b>",
            )


@pbot.on_callback_query(filters.regex("close"))
async def close_reply(_, CallbackQuery):
    await CallbackQuery.message.delete()


@pbot.on_callback_query(filters.regex("close_"))
async def close_send_photo(_, CallbackQuery):
    if CallbackQuery.from_user.id != OWNER_ID:
        return await CallbackQuery.answer(
            "ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ʀɪɢʜᴛs ᴛᴏ ᴄʟᴏsᴇ ᴛʜɪs ʙᴀʙʏ🥀!.", show_alert=True
        )
    else:
        await CallbackQuery.message.delete()


__help__ = """
 » `/bug` <text> :  ꜰᴏʀ ʀᴇᴘᴏʀᴛɪɴɢ ᴀɴʏ ʙᴜɢ ɪɴ ʙᴏᴛ
 """
__mod_name__ = "BUG"
