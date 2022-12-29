from os import remove

from pyrogram import filters

from KRISTY import pbot, arq, BOT_USERNAME as bn
from KRISTY.utils.errors import capture_err
from KRISTY.utils.permissions import adminsOnly
from KRISTY.services.dbfunctions import is_nsfw_on, nsfw_off, nsfw_on


__help__ = """
 » `/nsfwscan` <reply to a sticker> :  ᴄʜᴇᴄᴋ ᴀᴅᴜʟᴛ ᴄᴏɴᴛᴇɴᴛꜱ
 » `/antinsfw`  [on/off] :  ɪᴛ ᴡɪʟʟ ꜱᴛᴏᴘ ᴛʜᴇ ᴀʟʟᴏᴡᴀɴᴄᴇ ᴏꜰ ᴀᴅᴜʟᴛ ᴄᴏɴᴛᴇɴᴛꜱ ɪɴ ɢʀᴏᴜᴘ
 """
__mod_name__ = "ANIT-NSFW"


async def get_file_id_from_message(message):
    file_id = None
    if message.document:
        if int(message.document.file_size) > 3145728:
            return
        mime_type = message.document.mime_type
        if mime_type != "image/png" and mime_type != "image/jpeg":
            return
        file_id = message.document.file_id

    if message.sticker:
        if message.sticker.is_animated:
            if not message.sticker.thumbs:
                return
            file_id = message.sticker.thumbs[0].file_id
        else:
            file_id = message.sticker.file_id

    if message.photo:
        file_id = message.photo.file_id

    if message.animation:
        if not message.animation.thumbs:
            return
        file_id = message.animation.thumbs[0].file_id

    if message.video:
        if not message.video.thumbs:
            return
        file_id = message.video.thumbs[0].file_id
    return file_id


@pbot.on_message(
    (
        filters.document
        | filters.photo
        | filters.sticker
        | filters.animation
        | filters.video
    )
    & ~filters.private,
    group=8,
)
@capture_err
async def detect_nsfw(_, message):
    if not await is_nsfw_on(message.chat.id):
        return
    if not message.from_user:
        return
    file_id = await get_file_id_from_message(message)
    if not file_id:
        return
    file = await pbot.download_media(file_id)
    try:
        results = await arq.nsfw_scan(file=file)
    except Exception:
        return
    if not results.ok:
        return
    results = results.result
    remove(file)
    nsfw = results.is_nsfw
    if not nsfw:
        return
    try:
        await message.delete()
    except Exception:
        return
    await message.reply_text(
        f"""
**NSFW Image Detected & Deleted Successfully ʙᴀʙʏ🥀!
————————————————————**
**ᴜꜱᴇʀ:** {message.from_user.mention} [`{message.from_user.id}`]
**ꜱᴀꜰᴇ:** `{results.neutral} %`
**ᴘᴏʀɴ:** `{results.porn} %`
**ᴀᴅᴜʟᴛ:** `{results.sexy} %`
**ʜᴇɴᴛᴀɪ:** `{results.hentai} %`
**ᴅʀᴀᴡɪɴɢꜱ:** `{results.drawings} %`
**————————————————————**
__ᴜꜱᴇ `/antinsfw off` ᴛᴏ ᴅɪꜱᴀʙʟᴇ ᴛʜɪꜱ.__
"""
    )


@pbot.on_message(filters.command("nsfwscan"))
@capture_err
async def nsfw_scan_command(_, message):
    if not message.reply_to_message:
        await message.reply_text(
            "`ʀᴇᴘʟʏ ᴛᴏ ᴀɴ ɪᴍᴀɢᴇ/ᴅᴏᴄᴜᴍᴇɴᴛ/ꜱᴛɪᴄᴋᴇʀ/ᴀɴɪᴍᴀᴛɪᴏɴ ᴛᴏ ꜱᴄᴀɴ ɪᴛ ʙᴀʙʏ🥀.`"
        )
        return
    reply = message.reply_to_message
    if (
        not reply.document
        and not reply.photo
        and not reply.sticker
        and not reply.animation
        and not reply.video
    ):
        await message.reply_text(
            "ʀᴇᴘʟʏ ᴛᴏ ᴀɴ ɪᴍᴀɢᴇ/ᴅᴏᴄᴜᴍᴇɴᴛ/ꜱᴛɪᴄᴋᴇʀ/ᴀɴɪᴍᴀᴛɪᴏɴ ᴛᴏ ꜱᴄᴀɴ ɪᴛ ʙᴀʙʏ🥀."
        )
        return
    m = await message.reply_text("`ꜱᴄᴀɴɴɪɴɢ ʙᴀʙʏ🥀...`")
    file_id = await get_file_id_from_message(reply)
    if not file_id:
        return await m.edit("`ꜱᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ ʜᴀᴘᴘᴇɴᴇᴅ ʙᴀʙʏ🥀...|")
    file = await pbot.download_media(file_id)
    try:
        results = await arq.nsfw_scan(file=file)
    except Exception:
        return
    remove(file)
    if not results.ok:
        return await m.edit(results.result)
    results = results.result
    await m.edit(
        f"""
**ɴᴇᴜᴛʀᴀʟ:** `{results.neutral} %`
**ᴘᴏʀɴ:** `{results.porn} %`
**ʜᴇɴᴛᴀɪ:** `{results.hentai} %`
**ꜱᴇxʏ:** `{results.sexy} %`
**ᴅʀᴀᴡɪɴɢꜱ:** `{results.drawings} %`
**ɴꜱꜰᴡ:** `{results.is_nsfw}`
"""
    )


@pbot.on_message(filters.command(["antinsfw", f"antinsfw@{bn}"]) & ~filters.private)
@adminsOnly("can_change_info")
async def nsfw_enable_disable(_, message):
    if len(message.command) != 2:
        await message.reply_text("ᴜꜱᴀɢᴇ: /antinsfw [on/off] ʙᴀʙʏ🥀")
        return
    status = message.text.split(None, 1)[1].strip()
    status = status.lower()
    chat_id = message.chat.id
    if status == "on" or status == "yes":
        await nsfw_on(chat_id)
        await message.reply_text(
            "ᴇɴᴀʙʟᴇᴅ ᴀɴᴛɪɴꜱꜰᴡ ꜱʏꜱᴛᴇᴍ. ɪ ᴡɪʟʟ ᴅᴇʟᴇᴛᴇ ᴍᴇꜱꜱᴀɢᴇꜱ ᴄᴏɴᴛᴀɪɴɪɴɢ ɪɴᴀᴘᴘʀᴏᴘʀɪᴀᴛᴇ ᴄᴏɴᴛᴇɴᴛ ʙᴀʙʏ🥀."
        )
    elif status == "off" or status == "no":
        await nsfw_off(chat_id)
        await message.reply_text("ᴅɪꜱᴀʙʟᴇᴅ ᴀɴᴛɪɴꜱꜰᴡ ꜱʏꜱᴛᴇᴍ ʙᴀʙʏ🥀.")
    else:
        await message.reply_text("ᴜɴᴋɴᴏᴡɴ ꜱᴜꜰꜰɪx, ᴜꜱᴇ /antinsfw [on/off] ʙᴀʙʏ🥀")
