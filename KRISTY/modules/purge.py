import asyncio
import time
from telethon import events

from KRISTY import telethn
from KRISTY.modules.helper_funcs.telethn.chatstatus import (
    can_delete_messages,
    user_is_admin,
)


async def purge_messages(event):
    start = time.perf_counter()
    if event.from_id is None:
        return

    if (
        not await user_is_admin(
            user_id=event.sender_id,
            message=event,
        )
        and event.from_id not in [1087968824]
    ):
        await event.reply("ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴀʀᴇ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ʙᴀʙʏ🥀")
        return

    if not await can_delete_messages(message=event):
        await event.reply("ᴄᴀɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ᴘᴜʀɢᴇ ᴛʜᴇ ᴍᴇꜱꜱᴀɢᴇ ʙᴀʙʏ🥀")
        return

    reply_msg = await event.get_reply_message()
    if not reply_msg:
        await event.reply("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ꜱᴇʟᴇᴄᴛ ᴡʜᴇʀᴇ ᴛᴏ ꜱᴛᴀʀᴛ ᴘᴜʀɢɪɴɢ ꜰʀᴏᴍ ʙᴀʙʏ🥀.")
        return
    messages = []
    message_id = reply_msg.id
    delete_to = event.message.id

    messages.append(event.reply_to_msg_id)
    for msg_id in range(message_id, delete_to + 1):
        messages.append(msg_id)
        if len(messages) == 100:
            await event.client.delete_messages(event.chat_id, messages)
            messages = []

    try:
        await event.client.delete_messages(event.chat_id, messages)
    except:
        pass
    time_ = time.perf_counter() - start
    text = f"ᴘᴜʀɢᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ɪɴ {time_:0.2f} ꜱᴇᴄᴏɴᴅ(s) ʙᴀʙʏ🥀"
    await event.respond(text, parse_mode="markdown")

async def delete_messages(event):
    if event.from_id is None:
        return

    if (
        not await user_is_admin(
            user_id=event.sender_id,
            message=event,
        )
        and event.from_id not in [1087968824]
    ):
        await event.reply("ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴀʀᴇ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ʙᴀʙʏ🥀")
        return

    if not await can_delete_messages(message=event):
        await event.reply("ᴄᴀɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴛʜɪꜱ ʙᴀʙʏ🥀?")
        return

    message = await event.get_reply_message()
    if not message:
        await event.reply("ᴡʜᴀᴅʏᴀ ᴡᴀɴᴛ ᴛᴏ ᴅᴇʟᴇᴛᴇ ʙᴀʙʏ🥀?")
        return
    chat = await event.get_input_chat()
    del_message = [message, event.message]
    await event.client.delete_messages(chat, del_message)

PURGE_HANDLER = purge_messages, events.NewMessage(pattern="^[!/]purge$")
DEL_HANDLER = delete_messages, events.NewMessage(pattern="^[!/]del$")

telethn.add_event_handler(*PURGE_HANDLER)
telethn.add_event_handler(*DEL_HANDLER)

__mod_name__ = "Purges"
__command_list__ = ["del", "purge"]
__handlers__ = [PURGE_HANDLER, DEL_HANDLER]
