from bs4 import BeautifulSoup
import urllib
import glob
import io
import os
import re
import aiohttp
import urllib.request
from urllib.parse import urlencode
import requests
from bs4 import BeautifulSoup
from PIL import Image
from search_engine_parser import GoogleSearch

import bs4
import html2text
from bing_image_downloader import downloader
from telethon import *
from telethon.tl import functions
from telethon.tl import types
from telethon.tl.types import *

from KRISTY import *

from KRISTY.events import register
from KRISTY import telethn as tbot

opener = urllib.request.build_opener()
useragent = "Mozilla/5.0 (Linux; Android 9; SM-G960F Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.157 Mobile Safari/537.36"
opener.addheaders = [("User-agent", useragent)]


@register(pattern="^/google (.*)")
async def _(event):
    if event.fwd_from:
        return

    webevent = await event.reply("ꜱᴇᴀʀᴄʜɪɴɢ ʙᴀʙʏ🥀...")
    match = event.pattern_match.group(1)
    page = re.findall(r"page=\d+", match)
    try:
        page = page[0]
        page = page.replace("page=", "")
        match = match.replace("page=" + page[0], "")
    except IndexError:
        page = 1
    search_args = (str(match), int(page))
    gsearch = GoogleSearch()
    gresults = await gsearch.async_search(*search_args)
    msg = ""
    for i in range(len(gresults["links"])):
        try:
            title = gresults["titles"][i]
            link = gresults["links"][i]
            desc = gresults["descriptions"][i]
            msg += f"»[{title}]({link})\n**{desc}**\n\n"
        except IndexError:
            break
    await webevent.edit(
        "**ꜱᴇᴀʀᴄʜ Qᴜᴇʀʏ:**\n`" + match + "`\n\n**ʀᴇꜱᴜʟᴛꜱ:**\n" + msg, link_preview=False
    )


@register(pattern="^/image (.*)")
async def img_sampler(event):
    if event.fwd_from:
        return

    query = event.pattern_match.group(1)
    jit = f'"{query}"'
    downloader.download(
        jit,
        limit=4,
        output_dir="store",
        adult_filter_off=False,
        force_replace=False,
        timeout=60,
    )
    os.chdir(f'./store/"{query}"')
    types = ("*.png", "*.jpeg", "*.jpg")  # the tuple of file types
    files_grabbed = []
    for files in types:
        files_grabbed.extend(glob.glob(files))
    await tbot.send_file(event.chat_id, files_grabbed, reply_to=event.id)
    os.chdir("/app")
    os.system("rm -rf store")


opener = urllib.request.build_opener()
useragent = "Mozilla/5.0 (Linux; Android 9; SM-G960F Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.157 Mobile Safari/537.36"
opener.addheaders = [("User-agent", useragent)]


@register(pattern=r"^/reverse(?: |$)(\d*)")
async def okgoogle(img):
    """For .reverse command, Google search images and stickers."""
    if os.path.isfile("okgoogle.png"):
        os.remove("okgoogle.png")

    message = await img.get_reply_message()
    if message and message.media:
        photo = io.BytesIO()
        await tbot.download_media(message, photo)
    else:
        await img.reply("`ʀᴇᴘʟʏ ᴛᴏ ᴘʜᴏᴛᴏ ᴏʀ ꜱᴛɪᴄᴋᴇʀ ʙᴀʙʏ🥀.`")
        return

    if photo:
        dev = await img.reply("`ᴘʀᴏᴄᴇꜱꜱɪɴɢ ʙᴀʙʏ🥀...`")
        try:
            image = Image.open(photo)
        except OSError:
            await dev.edit("`ᴜɴꜱᴜᴘᴘᴏʀᴛᴇᴅ ꜱᴇxᴜᴀʟɪᴛʏ, ᴍᴏꜱᴛ ʟɪᴋᴇʟʏ ʙᴀʙʏ🥀.`")
            return
        name = "okgoogle.png"
        image.save(name, "PNG")
        image.close()
        # https://stackoverflow.com/questions/23270175/google-reverse-image-search-using-post-request#28792943
        searchUrl = "https://www.google.com/searchbyimage/upload"
        multipart = {"encoded_image": (name, open(name, "rb")), "image_content": ""}
        response = requests.post(searchUrl, files=multipart, allow_redirects=False)
        fetchUrl = response.headers["Location"]

        if response != 400:
            await dev.edit(
                "`ɪᴍᴀɢᴇ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴜᴘʟᴏᴀᴅᴇᴅ ᴛᴏ ɢᴏᴏɢʟᴇ ʙᴀʙʏ🥀.`"
                "\n`ᴘᴀʀꜱɪɴɢ ꜱᴏᴜʀᴄᴇ ɴᴏᴡ. ᴍᴀʏʙᴇ.`"
            )
        else:
            await dev.edit("`ɢᴏᴏɢʟᴇ ᴛᴏʟᴅ ᴍᴇ ᴛᴏ ꜰᴜᴄᴋ ᴏꜰꜰ ʙᴀʙʏ🥀.`")
            return

        os.remove(name)
        match = await ParseSauce(fetchUrl + "&preferences?hl=en&fg=1#languages")
        guess = match["best_guess"]
        imgspage = match["similar_images"]

        if guess and imgspage:
            await dev.edit(f"[{guess}]({fetchUrl})\n\n`ʟᴏᴏᴋɪɴɢ ꜰᴏʀ ᴛʜɪꜱ ɪᴍᴀɢᴇ ʙᴀʙʏ🥀...`")
        else:
            await dev.edit("`ᴄᴀɴ'ᴛ ꜰɪɴᴅ ᴛʜɪꜱ ᴘɪᴇᴄᴇ ᴏꜰ ꜱʜɪᴛ ʙᴀʙʏ🥀.`")
            return

        if img.pattern_match.group(1):
            lim = img.pattern_match.group(1)
        else:
            lim = 3
        images = await scam(match, lim)
        yeet = []
        for i in images:
            k = requests.get(i)
            yeet.append(k.content)
        try:
            await tbot.send_file(
                entity=await tbot.get_input_entity(img.chat_id),
                file=yeet,
                reply_to=img,
            )
        except TypeError:
            pass
        await dev.edit(
            f"[{guess}]({fetchUrl})\n\n[ᴠɪꜱᴜᴀʟʟʏ ꜱɪᴍɪʟᴀʀ ɪᴍᴀɢᴇꜱ ʙᴀʙʏ🥀]({imgspage})"
        )


async def ParseSauce(googleurl):
    """Parse/Scrape the HTML code for the info we want."""

    source = opener.open(googleurl).read()
    soup = BeautifulSoup(source, "html.parser")

    results = {"similar_images": "", "best_guess": ""}

    try:
        for similar_image in soup.findAll("input", {"class": "gLFyf"}):
            url = "https://www.google.com/search?tbm=isch&q=" + urllib.parse.quote_plus(
                similar_image.get("value")
            )
            results["similar_images"] = url
    except BaseException:
        pass

    for best_guess in soup.findAll("div", attrs={"class": "r5a77d"}):
        results["best_guess"] = best_guess.get_text()

    return results


async def scam(results, lim):

    single = opener.open(results["similar_images"]).read()
    decoded = single.decode("utf-8")

    imglinks = []
    counter = 0

    pattern = r"^,\[\"(.*[.png|.jpg|.jpeg])\",[0-9]+,[0-9]+\]$"
    oboi = re.findall(pattern, decoded, re.I | re.M)

    for imglink in oboi:
        counter += 1
        if counter < int(lim):
            imglinks.append(imglink)
        else:
            break

    return imglinks

__mod_name__ = "SEARCH"

