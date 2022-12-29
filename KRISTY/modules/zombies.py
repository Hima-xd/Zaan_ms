from asyncio import sleep

from telethon import events
from telethon.errors import ChatAdminRequiredError, UserAdminInvalidError
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChannelParticipantsAdmins, ChatBannedRights

from KRISTY import DEMONS, DEV_USERS, DRAGONS, OWNER_ID, telethn

# =================== CONSTANT ===================

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)


UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

OFFICERS = [OWNER_ID] + DEV_USERS + DRAGONS + DEMONS

# Check if user has admin rights


async def is_administrator(user_id: int, message):
    admin = False
    async for user in telethn.iter_participants(
        message.chat_id, filter=ChannelParticipantsAdmins
    ):
        if user_id == user.id or user_id in OFFICERS:
            admin = True
            break
    return admin


@telethn.on(events.NewMessage(pattern="^[!/]zombies ?(.*)"))
async def rm_deletedacc(show):
    con = show.pattern_match.group(1).lower()
    del_u = 0
    del_status = "**ɢʀᴏᴜᴘ ᴄʟᴇᴀɴ, 0 ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛꜱ ꜰᴏᴜɴᴅ ʙᴀʙʏ🥀.**"
    if con != "clean":
        kontol = await show.reply("`ꜱᴇᴀʀᴄʜɪɴɢ ꜰᴏʀ ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛ ᴛᴏ ᴘʜᴜᴋ ʙᴀʙʏ🥀...`")
        async for user in show.client.iter_participants(show.chat_id):
            if user.deleted:
                del_u += 1
                await sleep(1)
        if del_u > 0:
            del_status = (
                f"**ꜱᴇᴀʀᴄʜɪɴɢ...** `{del_u}` **ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛ/zombie ᴏɴ ᴛʜɪꜱ ɢʀᴏᴜᴘ,"
                "\nᴄʟᴇᴀɴ ɪᴛ ᴡɪᴛʜ ᴄᴏᴍᴍᴀɴᴅ** `/zombies clean` ʙᴀʙʏ🥀"
            )
        return await kontol.edit(del_status)
    chat = await show.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        return await show.reply("**ꜱᴏʀʀʏ ʏᴏᴜ'ʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ʙᴀʙʏ🥀!**")
    memek = await show.reply("`ᴘʜᴜᴄᴋɪɴɢ ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛꜱ ʙᴀʙʏ🥀...`")
    del_u = 0
    del_a = 0
    async for user in telethn.iter_participants(show.chat_id):
        if user.deleted:
            try:
                await show.client(
                    EditBannedRequest(show.chat_id, user.id, BANNED_RIGHTS)
                )
            except ChatAdminRequiredError:
                return await show.edit("ɴᴏᴛ ʜᴀᴠᴇ ᴀ ʙᴀɴɴᴇᴅ ʀɪɢʜᴛꜱ ᴏɴ ᴛʜɪꜱ ɢʀᴏᴜᴘ ʙᴀʙʏ🥀")
            except UserAdminInvalidError:
                del_u -= 1
                del_a += 1
            await telethn(EditBannedRequest(show.chat_id, user.id, UNBAN_RIGHTS))
            del_u += 1
    if del_u > 0:
        del_status = f"**ᴄʟᴇᴀɴᴇᴅ** `{del_u}` **ᴢᴏᴍʙɪᴇꜱ** ʙᴀʙʏ🥀"
    if del_a > 0:
        del_status = (
            f"**ᴄʟᴇᴀɴᴇᴅ** `{del_u}` **ᴢᴏᴍʙɪᴇꜱ** "
            f"\n`{del_a}` **ᴀᴅᴍɪɴ ᴢᴏᴍʙɪᴇꜱ ɴᴏᴛ ᴅᴇʟᴇᴛᴇᴅ ʙᴀʙʏ🥀.**"
        )
    await memek.edit(del_status)


__help__ = """
 » `/zombies` :  ꜱᴛᴀʀᴛꜱ ꜱᴇᴀʀᴄʜɪɴɢ ꜰᴏʀ ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛꜱ ɪɴ ᴛʜᴇ ɢʀᴏᴜᴘ.
 » `/zombies clean` :  ʀᴇᴍᴏᴠᴇꜱ ᴛʜᴇ ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛꜱ ꜰʀᴏᴍ ᴛʜᴇ ɢʀᴏᴜᴘ.
 """
__mod_name__ = "ZOMBIE"
