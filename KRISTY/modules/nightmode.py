from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telethon import functions, types
from telethon.tl.types import ChatBannedRights

from KRISTY import BOT_NAME
from KRISTY import telethn as tbot
from KRISTY.events import register
from KRISTY.modules.sql.night_mode_sql import (
    add_nightmode,
    get_all_chat_id,
    is_nightmode_indb,
    rmnightmode,
)


async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):

        return isinstance(
            (
                await tbot(functions.channels.GetParticipantRequest(chat, user))
            ).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    elif isinstance(chat, types.InputPeerChat):

        ui = await tbot.get_peer_id(user)
        ps = (
            await tbot(functions.messages.GetFullChatRequest(chat.chat_id))
        ).full_chat.participants.participants
        return isinstance(
            next((p for p in ps if p.user_id == ui), None),
            (types.ChatParticipantAdmin, types.ChatParticipantCreator),
        )
    else:
        return None


hehes = ChatBannedRights(
    until_date=None,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    send_polls=True,
    invite_users=True,
    pin_messages=True,
    change_info=True,
)
openhehe = ChatBannedRights(
    until_date=None,
    send_messages=False,
    send_media=False,
    send_stickers=False,
    send_gifs=False,
    send_games=False,
    send_inline=False,
    send_polls=False,
    invite_users=True,
    pin_messages=True,
    change_info=True,
)


@register(pattern="^/nightmode")
async def close_ws(event):
    if event.is_group:
        if not (await is_register_admin(event.input_chat, event.message.sender_id)):
            await event.reply("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ꜱᴏ ʏᴏᴜ ᴄᴀɴ'ᴛ ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ʙᴀʙʏ🥀...")
            return

    if not event.is_group:
        await event.reply("ʏᴏᴜ ᴄᴀɴ ᴏɴʟʏ ᴇɴᴀʙʟᴇ ɴɪɢʜᴛ ᴍᴏᴅᴇ ɪɴ ɢʀᴏᴜᴘꜱ ʙᴀʙʏ🥀.")
        return
    if is_nightmode_indb(str(event.chat_id)):
        await event.reply("ᴛʜɪꜱ ᴄʜᴀᴛ ɪꜱ ʜᴀꜱ ᴀʟʀᴇᴀᴅʏ ᴇɴᴀʙʟᴇᴅ ɴɪɢʜᴛ ᴍᴏᴅᴇ ʙᴀʙʏ🥀.")
        return
    add_nightmode(str(event.chat_id))
    await event.reply(
        f"ᴀᴅᴅᴇᴅ ᴄʜᴀᴛ {event.chat.title} ᴡɪᴛʜ ɪᴅ {event.chat_id} ᴛᴏ ᴅᴀᴛᴀʙᴀꜱᴇ. **ᴛʜɪꜱ ɢʀᴏᴜᴘ ᴡɪʟʟ ʙᴇ ᴄʟᴏꜱᴇᴅ ᴏɴ 12ᴀᴍ(ɪꜱᴛ) ᴀɴᴅ ᴡɪʟʟ ᴏᴘᴇɴᴇᴅ ᴏɴ 06ᴀᴍ(ɪꜱᴛ) ʙᴀʙʏ🥀**"
    )


@register(pattern="^/rmnight")
async def disable_ws(event):
    if event.is_group:
        if not (await is_register_admin(event.input_chat, event.message.sender_id)):
            await event.reply("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ꜱᴏ ʏᴏᴜ ᴄᴀɴ'ᴛ ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ʙᴀʙʏ🥀...")
            return

    if not event.is_group:
        await event.reply("ʏᴏᴜ ᴄᴀɴ ᴏɴʟʏ ᴅɪꜱᴀʙʟᴇ ɴɪɢʜᴛ ᴍᴏᴅᴇ ɪɴ ɢʀᴏᴜᴘꜱ ʙᴀʙʏ🥀.")
        return
    if not is_nightmode_indb(str(event.chat_id)):
        await event.reply("ᴛʜɪꜱ ᴄʜᴀᴛ ɪꜱ ʜᴀꜱ ɴᴏᴛ ᴇɴᴀʙʟᴇᴅ ɴɪɢʜᴛ ᴍᴏᴅᴇ ʙᴀʙʏ🥀.")
        return
    rmnightmode(str(event.chat_id))
    await event.reply(
        f"ʀᴇᴍᴏᴠᴇᴅ ᴄʜᴀᴛ {event.chat.title} ᴡɪᴛʜ ɪᴅ {event.chat_id} ꜰʀᴏᴍ ᴅᴀᴛᴀʙᴀꜱᴇ ʙᴀʙʏ🥀."
    )


async def job_close():
    ws_chats = get_all_chat_id()
    if len(ws_chats) == 0:
        return
    for warner in ws_chats:
        try:
            await tbot.send_message(
                int(warner.chat_id),
                f"**ɴɪɢʜᴛ ᴍᴏᴅᴇ ꜱᴛᴀʀᴛᴇᴅ**\n\n`ɢʀᴏᴜᴘ ɪꜱ ᴄʟᴏꜱɪɴɢ ᴛɪʟʟ 6 ᴀᴍ, ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ᴍᴇꜱꜱᴀɢᴇꜱ ɪɴ ᴛʜɪꜱ ᴄʜᴀᴛ.`\n\n__ᴘᴏᴡᴇʀᴇᴅ ʙʏ {BOT_NAME}__ ʙᴀʙʏ🥀",
            )
            await tbot(
                functions.messages.EditChatDefaultBannedRightsRequest(
                    peer=int(warner.chat_id), banned_rights=hehes
                )
            )
        except Exception as e:
            logger.info(f"ᴜɴᴀʙʟᴇ ᴛᴏ ᴄʟᴏꜱᴇ ɢʀᴏᴜᴘ {warner} - {e} ʙᴀʙʏ🥀")


# Run everyday at 12am
scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")
scheduler.add_job(job_close, trigger="cron", hour=23, minute=59)
scheduler.start()


async def job_open():
    ws_chats = get_all_chat_id()
    if len(ws_chats) == 0:
        return
    for warner in ws_chats:
        try:
            await tbot.send_message(
                int(warner.chat_id),
                f"**ɴɪɢʜᴛ ᴍᴏᴅᴇ ᴇɴᴅᴇᴅ**\n\n`ɢʀᴏᴜᴘ ɪꜱ ᴏᴘᴇɴɪɴɢ ᴀɢᴀɪɴ ɴᴏᴡ ᴇᴠᴇʀʏᴏɴᴇ ᴄᴀɴ ꜱᴇɴᴅ ᴍᴇꜱꜱᴀɢᴇꜱ ɪɴ ᴛʜɪꜱ ᴄʜᴀᴛ.`\n__ᴘᴏᴡᴇʀᴇᴅ ʙʏ {BOT_NAME}__ ʙᴀʙʏ🥀",
            )
            await tbot(
                functions.messages.EditChatDefaultBannedRightsRequest(
                    peer=int(warner.chat_id), banned_rights=openhehe
                )
            )
        except Exception as e:
            logger.info(f"ᴜɴᴀʙʟᴇ ᴛᴏ ᴏᴘᴇɴ ɢʀᴏᴜᴘ {warner.chat_id} - {e} ʙᴀʙʏ🥀")


# Run everyday at 06
scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")
scheduler.add_job(job_open, trigger="cron", hour=6, minute=1)
scheduler.start()

__help__ = """
 » `/nightmode`*:* ᴀᴅᴅ ɢʀᴏᴜᴘ ꜰʀᴏᴍ ɴɪɢʜᴛᴍᴏᴅᴇ ᴄʜᴀᴛꜱ
 » `/rmnight`*:* ʀᴇᴍᴏᴠᴇꜱ ɢʀᴏᴜᴘ ꜰʀᴏᴍ ɴɪɢʜᴛᴍᴏᴅᴇ ᴄʜᴀᴛꜱ

*ɴᴏᴛᴇ:* ɴɪɢʜᴛ ᴍᴏᴅᴇ ᴄʜᴀᴛꜱ ɢᴇᴛ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴄʟᴏꜱᴇᴅ ᴀᴛ 12 ᴀᴍ(ɪꜱᴛ) ᴀɴᴅ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴏᴘᴇɴɴᴇᴅ ᴀᴛ 6 ᴀᴍ(ɪꜱᴛ) ᴛᴏ ᴘʀᴇᴠᴇɴᴛ ɴɪɢʜᴛ ꜱᴘᴀᴍꜱ.
"""

__mod_name__ = "NIGHT-MODE"
