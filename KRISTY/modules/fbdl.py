import os
import re
import requests
import youtube_dl

from yt_dlp import YoutubeDL
from datetime import datetime
from telethon import events

from KRISTY.utils.plh import is_admin
from KRISTY import telethn, BOT_USERNAME, SUPPORT_CHAT


def main(url, filename):
    try:
        download_video("HD", url, filename)
    except (KeyboardInterrupt):
        download_video("SD", url, filename)


def download_video(quality, url, filename):
    html = requests.get(url).content.decode("utf-8")
    video_url = re.search(rf'{quality.lower()}_src:"(.+?)"', html).group(1)
    file_size_request = requests.get(video_url, stream=True)
    int(file_size_request.headers["Content-Length"])
    block_size = 1024
    with open(filename + ".mp4", "wb") as f:
        for data in file_size_request.iter_content(block_size):
            f.write(data)
    print("\nᴠɪᴅᴇᴏ ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ʙᴀʙʏ🥀.")


@telethn.on(events.NewMessage(pattern="^/fbdl (.*)"))
async def _(event):
    if event.fwd_from:
        return
    if await is_admin(event, event.message.sender_id):
        url = event.pattern_match.group(1)
        x = re.match(r"^(https:|)[/][/]www.([^/]+[.])*facebook.com", url)

        if x:
            html = requests.get(url).content.decode("utf-8")
            await event.reply(
                "ꜱᴛᴀʀᴛɪɴɢ ᴠɪᴅᴇᴏ ᴅᴏᴡɴʟᴏᴀᴅ... \n ᴘʟᴇᴀꜱᴇ ɴᴏᴛᴇ: ꜰʙᴅʟ ɪꜱ ɴᴏᴛ ꜰᴏʀ ʙɪɢ ꜰɪʟᴇꜱ ʙᴀʙʏ🥀."
            )
        else:
            await event.reply(
                "ᴛʜɪꜱ ᴠɪᴅᴇᴏ ɪꜱ ᴇɪᴛʜᴇʀ ᴘʀɪᴠᴀᴛᴇ ᴏʀ ᴜʀʟ ɪꜱ ɪɴᴠᴀʟɪᴅ. ᴇxɪᴛɪɴɢ ʙᴀʙʏ🥀... "
            )
            return

        _qualityhd = re.search('hd_src:"https', html)
        _qualitysd = re.search('sd_src:"https', html)
        _hd = re.search("hd_src:null", html)
        _sd = re.search("sd_src:null", html)

        _thelist = [_qualityhd, _qualitysd, _hd, _sd]
        list = [id for id, val in enumerate(_thelist) if val is not None]
        filename = datetime.strftime(datetime.now(), "%Y-%m-%d-%H-%M-%S")

        main(url, filename)
        await event.reply("ᴠɪᴅᴇᴏ ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ. ꜱᴛᴀʀᴛɪɴɢ ᴛᴏ ᴜᴘʟᴏᴀᴅ ʙᴀʙʏ🥀.")

        kk = f"{filename}.mp4"
        caption = f"ꜰᴀᴄᴇʙᴏᴏᴋ ᴠɪᴅᴇᴏ ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ʙʏ [@{BOT_USERNAME}](https://t.me/Miss_Kristy_bot) ʙᴀʙʏ🥀."

        await telethn.send_file(
            event.chat_id,
            kk,
            caption = f"ꜰᴀᴄᴇʙᴏᴏᴋ ᴠɪᴅᴇᴏ ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ʙʏ [@{BOT_USERNAME}](https://t.me/Miss_Kristy_bot) ʙᴀʙʏ🥀.",
        )
        os.system(f"rm {kk}")
    else:
        await event.reply("`ʏᴏᴜ ꜱʜᴏᴜʟᴅ ʙᴇ ᴀᴅᴍɪɴ ᴛᴏ ᴅᴏ ᴛʜɪꜱ ʙᴀʙʏ🥀!`")
        return
