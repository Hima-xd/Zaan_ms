import asyncio
import datetime
import os
import time
import traceback

import aiohttp
from telethon import events

from KRISTY import telethn as bot
from KRISTY.modules.urluploader import download_file
from KRISTY.utils.uputils import humanbytes, progress

DOWNLOADPATH = "Downloads/"


def get_date_in_two_weeks():
    """
    get maximum date of storage for file
    :return: date in two weeks
    """
    today = datetime.datetime.today()
    date_in_two_weeks = today + datetime.timedelta(days=14)
    return date_in_two_weeks.date()


async def send_to_transfersh_async(file):

    size = os.path.getsize(file)
    size_of_file = humanbytes(size)
    final_date = get_date_in_two_weeks()
    file_name = os.path.basename(file)

    print("\nᴜᴘʟᴏᴀᴅɪɴɢ ꜰɪʟᴇ: {} (ꜱɪᴢᴇ ᴏꜰ ᴛʜᴇ ꜰɪʟᴇ: {}) ʙᴀʙʏ🥀".format(file_name, size_of_file))
    url = "https://transfer.sh/"

    with open(file, "rb") as f:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data={str(file): f}) as response:
                download_link = await response.text()

    print(
        "ʟɪɴᴋ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ꜰɪʟᴇ(ᴡɪʟʟ ʙᴇ ꜱᴀᴠᴇᴅ ᴛɪʟʟ {}):\n{} ʙᴀʙʏ🥀".format(
            final_date, download_link
        )
    )
    return download_link, final_date, size_of_file


async def send_to_tmp_async(file):
    url = "https://tmp.ninja/api.php?d=upload-tool"

    with open(file, "rb") as f:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data={"file": f}) as response:
                download_link = await response.text()

    return download_link


@bot.on(events.NewMessage(pattern="/transfersh"))
async def tsh(event):
    if event.reply_to_msg_id:
        start = time.time()
        url = await event.get_reply_message()
        ilk = await event.respond("ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ʙᴀʙʏ🥀...")
        try:
            file_path = await url.download_media(
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, ilk, start, "ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ʙᴀʙʏ🥀...")
                )
            )
        except Exception as e:
            traceback.print_exc()
            print(e)
            await event.respond(f"ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ꜰᴀɪʟᴇᴅ\n\n**ᴇʀʀᴏʀ:** {e} ʙᴀʙʏ🥀")

        await ilk.delete()

        try:
            orta = await event.respond("ᴜᴘʟᴏᴀᴅɪɴɢ ᴛᴏ ᴛʀᴀɴꜱꜰᴇʀꜱʜ ʙᴀʙʏ🥀...")
            download_link, final_date, size = await send_to_transfersh_async(file_path)

            str(time.time() - start)
            await orta.edit(
                f"File ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴜᴘʟᴏᴀᴅᴇᴅ ᴛᴏ ᴛʀᴀɴꜱꜰᴇʀꜱʜ.\n\nʟɪɴᴋ 👉 {download_link}\nᴇxᴘɪʀᴇᴅ ᴅᴀᴛᴇ 👉{final_date}\n\nᴜᴘʟᴏᴀᴅᴇᴅ ʙʏ ᴋʀɪꜱᴛʏ ʙᴀʙʏ🥀"
            )
        except Exception as e:
            traceback.print_exc()
            print(e)
            await event.respond(f"ᴜᴘʟᴏᴀᴅɪɴɢ ꜰᴀɪʟᴇᴅ\n\n**ᴇʀʀᴏʀ:** {e} ʙᴀʙʏ🥀")

    raise events.StopPropagation


@bot.on(events.NewMessage(pattern="/tmpninja"))
async def tmp(event):
    if event.reply_to_msg_id:
        start = time.time()
        url = await event.get_reply_message()
        ilk = await event.respond("ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ʙᴀʙʏ🥀...")
        try:
            file_path = await url.download_media(
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, ilk, start, "ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ʙᴀʙʏ🥀...")
                )
            )
        except Exception as e:
            traceback.print_exc()
            print(e)
            await event.respond(f"ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ꜰᴀɪʟᴇᴅ\n\n**ᴇʀʀᴏʀ:** {e} ʙᴀʙʏ🥀")

        await ilk.delete()

        try:
            orta = await event.respond("ᴜᴘʟᴏᴀᴅɪɴɢ ᴛᴏ ᴛᴍᴘɴɪɴᴊᴀ ʙᴀʙʏ🥀...")
            download_link = await send_to_tmp_async(file_path)

            str(time.time() - start)
            await orta.edit(
                f"ꜰɪʟᴇ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴜᴘʟᴏᴀᴅᴇᴅ ᴛᴏ ᴛᴍᴘɴɪɴᴊᴀ.\n\nʟɪɴᴋ 👉 {download_link}\n\nᴜᴘʟᴏᴀᴅᴇᴅ ʙʏ ᴋʀɪꜱᴛʏ ʙᴀʙʏ🥀"
            )
        except Exception as e:
            traceback.print_exc()
            print(e)
            await event.respond(f"ᴜᴘʟᴏᴀᴅɪɴɢ ꜰᴀɪʟᴇᴅ\n\n**ᴇʀʀᴏʀ:** {e} ʙᴀʙʏ🥀")

    raise events.StopPropagation


@bot.on(events.NewMessage(pattern="/up"))
async def up(event):
    if event.reply_to_msg_id:
        start = time.time()
        url = await event.get_reply_message()
        ilk = await event.respond("ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ʙᴀʙʏ🥀...")

        try:
            filename = os.path.join(DOWNLOADPATH, os.path.basename(url.text))
            await download_file(url.text, filename, ilk, start, bot)
        except Exception as e:
            print(e)
            await event.respond(f"ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ꜰᴀɪʟᴇᴅ\n\n**ᴇʀʀᴏʀ:** {e} ʙᴀʙʏ🥀")

        await ilk.delete()

        try:
            orta = await event.respond("ᴜᴘʟᴏᴀᴅɪɴɢ ᴛᴏ ᴛᴇʟᴇɢʀᴀᴍ ʙᴀʙʏ🥀...")

            dosya = await bot.upload_file(
                filename,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, orta, start, "ᴜᴘʟᴏᴀᴅɪɴɢ ᴛᴏ ᴛᴇʟᴇɢʀᴀᴍ ʙᴀʙʏ🥀...")
                ),
            )

            str(time.time() - start)
            await bot.send_file(
                event.chat.id,
                dosya,
                force_document=True,
                caption=f"ᴜᴘʟᴏᴀᴅᴇᴅ ʙʏ *ᴋʀɪꜱᴛʏ* ʙᴀʙʏ🥀",
            )
        except Exception as e:
            traceback.print_exc()

            print(e)
            await event.respond(f"ᴜᴘʟᴏᴀᴅɪɴɢ ꜰᴀɪʟᴇᴅ\n\n**ᴇʀʀᴏʀ:** {e} ʙᴀʙʏ🥀")

        await orta.delete()

    raise events.StopPropagation


def main():
    if not os.path.isdir(DOWNLOADPATH):
        os.mkdir(DOWNLOADPATH)


if __name__ == "__main__":
    main()
