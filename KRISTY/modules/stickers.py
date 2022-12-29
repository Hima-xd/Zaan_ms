import math
import os
import urllib.request as urllib
from html import escape

import requests
from bs4 import BeautifulSoup as bs
from PIL import Image
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ParseMode,
    TelegramError,
    Update,
)
from telegram.ext import CallbackContext, run_async
from telegram.utils.helpers import mention_html

from KRISTY import dispatcher
from KRISTY.modules.disable import DisableAbleCommandHandler

combot_stickers_url = "https://combot.org/telegram/stickers?q="


@run_async
def stickerid(update: Update, context: CallbackContext):
    msg = update.effective_message
    if msg.reply_to_message and msg.reply_to_message.sticker:
        update.effective_message.reply_text(
            "ʜᴇʏ "
            + f"{mention_html(msg.from_user.id, msg.from_user.first_name)} ʙᴀʙʏ🥀!"
            + ", ᴛʜᴇ ꜱᴛɪᴄᴋᴇʀ ɪᴅ ʏᴏᴜ ᴀʀᴇ ʀᴇᴘʟʏɪɴɢ ɪꜱ  :\n <code>"
            + escape(msg.reply_to_message.sticker.file_id)
            + "</code>",
            parse_mode=ParseMode.HTML,
        )
    else:
        update.effective_message.reply_text(
            "ʜᴇʏ "
            + f"{mention_html(msg.from_user.id, msg.from_user.first_name)} ʙᴀʙʏ🥀!"
            + ", ᴘʟᴇᴀꜱᴇ ʀᴇᴘʟʏ ᴛᴏ ꜱᴛɪᴄᴋᴇʀ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ɢᴇᴛ ꜱᴛɪᴄᴋᴇʀ ɪᴅ",
            parse_mode=ParseMode.HTML,
        )


@run_async
def cb_sticker(update: Update, context: CallbackContext):
    msg = update.effective_message
    split = msg.text.split(" ", 1)
    if len(split) == 1:
        msg.reply_text("ᴘʀᴏᴠɪᴅᴇ ꜱᴏᴍᴇ ɴᴀᴍᴇ ᴛᴏ ꜱᴇᴀʀᴄʜ ꜰᴏʀ ᴘᴀᴄᴋ ʙᴀʙʏ🥀.")
        return
    text = requests.get(combot_stickers_url + split[1]).text
    soup = bs(text, "lxml")
    results = soup.find_all("a", {"class": "sticker-pack__btn"})
    titles = soup.find_all("div", "sticker-pack__title")
    if not results:
        msg.reply_text("ɴᴏ ʀᴇꜱᴜʟᴛꜱ ꜰᴏᴜɴᴅ ʙᴀʙʏ🥀.")
        return
    reply = f"ꜱᴛɪᴄᴋᴇʀꜱ ꜰᴏʀ *{split[1]}*:"
    for result, title in zip(results, titles):
        link = result["href"]
        reply += f"\n• [{title.get_text()}]({link})"
    msg.reply_text(reply, parse_mode=ParseMode.MARKDOWN)


def getsticker(update: Update, context: CallbackContext):
    bot = context.bot
    msg = update.effective_message
    chat_id = update.effective_chat.id
    if msg.reply_to_message and msg.reply_to_message.sticker:
        file_id = msg.reply_to_message.sticker.file_id
        new_file = bot.get_file(file_id)
        new_file.download("sticker.png")
        bot.send_document(chat_id, document=open("sticker.png", "rb"))
        os.remove("sticker.png")
    else:
        update.effective_message.reply_text(
            "ᴘʟᴇᴀꜱᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ꜱᴛɪᴄᴋᴇʀ ꜰᴏʀ ᴍᴇ ᴛᴏ ᴜᴘʟᴏᴀᴅ ɪᴛꜱ ᴘɴɢ ʙᴀʙʏ🥀."
        )

@run_async
def kang(update: Update, context: CallbackContext):
    msg = update.effective_message
    user = update.effective_user
    args = context.args
    packnum = 0
    packname = "a" + str(user.id) + "_by_" + context.bot.username
    packname_found = 0
    max_stickers = 120
    while packname_found == 0:
        try:
            stickerset = context.bot.get_sticker_set(packname)
            if len(stickerset.stickers) >= max_stickers:
                packnum += 1
                packname = (
                    "a"
                    + str(packnum)
                    + "_"
                    + str(user.id)
                    + "_by_"
                    + context.bot.username
                )
            else:
                packname_found = 1
        except TelegramError as e:
            if e.message == "Stickerset_invalid":
                packname_found = 1
    kangsticker = "kangsticker.png"
    is_animated = False
    file_id = ""

    if msg.reply_to_message:
        if msg.reply_to_message.sticker:
            if msg.reply_to_message.sticker.is_animated:
                is_animated = True
            file_id = msg.reply_to_message.sticker.file_id

        elif msg.reply_to_message.photo:
            file_id = msg.reply_to_message.photo[-1].file_id
        elif msg.reply_to_message.document:
            file_id = msg.reply_to_message.document.file_id
        else:
            msg.reply_text("ʏᴇᴀ, ɪ ᴄᴀɴ'ᴛ ᴋᴀɴɢ ᴛʜᴀᴛ ʙᴀʙʏ🥀.")

        kang_file = context.bot.get_file(file_id)
        if not is_animated:
            kang_file.download("kangsticker.png")
        else:
            kang_file.download("kangsticker.tgs")

        if args:
            sticker_emoji = str(args[0])
        elif msg.reply_to_message.sticker and msg.reply_to_message.sticker.emoji:
            sticker_emoji = msg.reply_to_message.sticker.emoji
        else:
            sticker_emoji = "🤔"

        if not is_animated:
            try:
                im = Image.open(kangsticker)
                maxsize = (512, 512)
                if (im.width and im.height) < 512:
                    size1 = im.width
                    size2 = im.height
                    if im.width > im.height:
                        scale = 512 / size1
                        size1new = 512
                        size2new = size2 * scale
                    else:
                        scale = 512 / size2
                        size1new = size1 * scale
                        size2new = 512
                    size1new = math.floor(size1new)
                    size2new = math.floor(size2new)
                    sizenew = (size1new, size2new)
                    im = im.resize(sizenew)
                else:
                    im.thumbnail(maxsize)
                if not msg.reply_to_message.sticker:
                    im.save(kangsticker, "PNG")
                context.bot.add_sticker_to_set(
                    user_id=user.id,
                    name=packname,
                    png_sticker=open("kangsticker.png", "rb"),
                    emojis=sticker_emoji,
                )
                msg.reply_text(
                    f"ʏᴏᴜʀ ꜱᴛɪᴄᴋᴇʀ ʜᴀꜱ ʙᴇᴇɴ ᴀᴅᴅᴇᴅ ᴛᴏ [ᴘᴀᴄᴋ](t.me/addstickers/{packname})"
                    + f"\nᴇᴍᴏᴊɪ ɪꜱ: {sticker_emoji} ʙᴀʙʏ🥀!",
                    parse_mode=ParseMode.MARKDOWN,
                )

            except OSError as e:
                msg.reply_text("ɪ ᴄᴀɴ ᴏɴʟʏ ᴋᴀɴɢ ɪᴍᴀɢᴇꜱ ʙᴀʙʏ🥀.")
                print(e)
                return

            except TelegramError as e:
                if e.message == "Stickerset_invalid":
                    makepack_internal(
                        update,
                        context,
                        msg,
                        user,
                        sticker_emoji,
                        packname,
                        packnum,
                        png_sticker=open("kangsticker.png", "rb"),
                    )
                elif e.message == "Sticker_png_dimensions":
                    im.save(kangsticker, "PNG")
                    context.bot.add_sticker_to_set(
                        user_id=user.id,
                        name=packname,
                        png_sticker=open("kangsticker.png", "rb"),
                        emojis=sticker_emoji,
                    )
                    msg.reply_text(
                        f"ʏᴏᴜʀ ꜱᴛɪᴄᴋᴇʀ ʜᴀꜱ ʙᴇᴇɴ ᴀᴅᴅᴇᴅ ᴛᴏ [ᴘᴀᴄᴋ](t.me/addstickers/{packname})"
                        + f"\nᴇᴍᴏᴊɪ ɪꜱ: {sticker_emoji} ʙᴀʙʏ🥀!",
                        parse_mode=ParseMode.MARKDOWN,
                    )
                elif e.message == "Invalid sticker emojis":
                    msg.reply_text("Invalid emoji(s).")
                elif e.message == "Stickers_too_much":
                    msg.reply_text("ᴍᴀx ᴘᴀᴄᴋꜱɪᴢᴇ ʀᴇᴀᴄʜᴇᴅ. ᴘʀᴇꜱꜱ ꜰ ᴛᴏ ᴘᴀʏ ʀᴇꜱᴘᴇᴄᴄ ʙᴀʙʏ🥀.")
                elif e.message == "Internal Server Error: sticker set not found (500)":
                    msg.reply_text(
                        "ꜱᴛɪᴄᴋᴇʀ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴀᴅᴅᴇᴅ ᴛᴏ [ᴘᴀᴄᴋ](t.me/addstickers/%s)"
                        % packname
                        + "\n"
                        "ᴇᴍᴏᴊɪ ɪꜱ:" + " " + sticker_emoji,
                        parse_mode=ParseMode.MARKDOWN,
                    )
                print(e)

        else:
            packname = "animated" + str(user.id) + "_by_" + context.bot.username
            packname_found = 0
            max_stickers = 50
            while packname_found == 0:
                try:
                    stickerset = context.bot.get_sticker_set(packname)
                    if len(stickerset.stickers) >= max_stickers:
                        packnum += 1
                        packname = (
                            "animated"
                            + str(packnum)
                            + "_"
                            + str(user.id)
                            + "_by_"
                            + context.bot.username
                        )
                    else:
                        packname_found = 1
                except TelegramError as e:
                    if e.message == "Stickerset_invalid":
                        packname_found = 1
            try:
                context.bot.add_sticker_to_set(
                    user_id=user.id,
                    name=packname,
                    tgs_sticker=open("kangsticker.tgs", "rb"),
                    emojis=sticker_emoji,
                )
                msg.reply_text(
                    f"ꜱᴛɪᴄᴋᴇʀ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴀᴅᴅᴇᴅ ᴛᴏ [ᴘᴀᴄᴋ](t.me/addstickers/{packname})"
                    + f"\nᴇᴍᴏᴊɪ ɪꜱ: {sticker_emoji} ʙᴀʙʏ🥀",
                    parse_mode=ParseMode.MARKDOWN,
                )
            except TelegramError as e:
                if e.message == "Stickerset_invalid":
                    makepack_internal(
                        update,
                        context,
                        msg,
                        user,
                        sticker_emoji,
                        packname,
                        packnum,
                        tgs_sticker=open("kangsticker.tgs", "rb"),
                    )
                elif e.message == "Invalid sticker emojis":
                    msg.reply_text("ɪɴᴠᴀʟɪᴅ ᴇᴍᴏᴊɪ(s) ʙᴀʙʏ🥀.")
                elif e.message == "Internal Server Error: sticker set not found (500)":
                    msg.reply_text(
                        "ꜱᴛɪᴄᴋᴇʀ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴀᴅᴅᴇᴅ ᴛᴏ [ᴘᴀᴄᴋ](t.me/addstickers/%s)"
                        % packname
                        + "\n"
                        "ᴇᴍᴏᴊɪ ɪꜱ:" + " " + sticker_emoji,
                        parse_mode=ParseMode.MARKDOWN,
                    )
                print(e)

    elif args:
        try:
            try:
                urlemoji = msg.text.split(" ")
                png_sticker = urlemoji[1]
                sticker_emoji = urlemoji[2]
            except IndexError:
                sticker_emoji = "🤔"
            urllib.urlretrieve(png_sticker, kangsticker)
            im = Image.open(kangsticker)
            maxsize = (512, 512)
            if (im.width and im.height) < 512:
                size1 = im.width
                size2 = im.height
                if im.width > im.height:
                    scale = 512 / size1
                    size1new = 512
                    size2new = size2 * scale
                else:
                    scale = 512 / size2
                    size1new = size1 * scale
                    size2new = 512
                size1new = math.floor(size1new)
                size2new = math.floor(size2new)
                sizenew = (size1new, size2new)
                im = im.resize(sizenew)
            else:
                im.thumbnail(maxsize)
            im.save(kangsticker, "PNG")
            msg.reply_photo(photo=open("kangsticker.png", "rb"))
            context.bot.add_sticker_to_set(
                user_id=user.id,
                name=packname,
                png_sticker=open("kangsticker.png", "rb"),
                emojis=sticker_emoji,
            )
            msg.reply_text(
                    f"ꜱᴛɪᴄᴋᴇʀ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴀᴅᴅᴇᴅ ᴛᴏ [ᴘᴀᴄᴋ](t.me/addstickers/{packname})"
                    + f"\nᴇᴍᴏᴊɪ ɪꜱ: {sticker_emoji} ʙᴀʙʏ🥀",
                parse_mode=ParseMode.MARKDOWN,
            )
        except OSError as e:
            msg.reply_text("ɪ ᴄᴀɴ ᴏɴʟʏ ᴋᴀɴɢ ɪᴍᴀɢᴇꜱ ʙᴀʙʏ🥀.")
            print(e)
            return
        except TelegramError as e:
            if e.message == "Stickerset_invalid":
                makepack_internal(
                    update,
                    context,
                    msg,
                    user,
                    sticker_emoji,
                    packname,
                    packnum,
                    png_sticker=open("kangsticker.png", "rb"),
                )
            elif e.message == "Sticker_png_dimensions":
                im.save(kangsticker, "PNG")
                context.bot.add_sticker_to_set(
                    user_id=user.id,
                    name=packname,
                    png_sticker=open("kangsticker.png", "rb"),
                    emojis=sticker_emoji,
                )
                msg.reply_text(
                    "ꜱᴛɪᴄᴋᴇʀ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴀᴅᴅᴇᴅ ᴛᴏ [ᴘᴀᴄᴋ](t.me/addstickers/%s)"
                    % packname
                    + "\n"
                    + "ᴇᴍᴏᴊɪ ɪꜱ:"
                    + " "
                    + sticker_emoji,
                    parse_mode=ParseMode.MARKDOWN,
                )
            elif e.message == "Invalid sticker emojis":
                msg.reply_text("ɪɴᴠᴀʟɪᴅ ᴇᴍᴏᴊɪ(s) ʙᴀʙʏ🥀.")
            elif e.message == "Stickers_too_much":
                msg.reply_text("ᴍᴀx ᴘᴀᴄᴋꜱɪᴢᴇ ʀᴇᴀᴄʜᴇᴅ. ᴘʀᴇꜱꜱ ꜰ ᴛᴏ ᴘᴀʏ ʀᴇꜱᴘᴇᴄᴄ ʙᴀʙʏ🥀.")
            elif e.message == "Internal Server Error: sticker set not found (500)":
                msg.reply_text(
                    "ꜱᴛɪᴄᴋᴇʀ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴀᴅᴅᴇᴅ ᴛᴏ [ᴘᴀᴄᴋ](t.me/addstickers/%s)"
                    % packname
                    + "\n"
                    "ᴇᴍᴏᴊɪ ɪꜱ:" + " " + sticker_emoji,
                    parse_mode=ParseMode.MARKDOWN,
                )
            print(e)
    else:
        packs = "ᴘʟᴇᴀꜱᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ꜱᴛɪᴄᴋᴇʀ, ᴏʀ ɪᴍᴀɢᴇ ᴛᴏ ᴋᴀɴɢ ɪᴛ ʙᴀʙʏ🥀!\nᴏʜ, ʙʏ ᴛʜᴇ ᴡᴀʏ. ʜᴇʀᴇ ᴀʀᴇ ʏᴏᴜʀ ᴘᴀᴄᴋꜱ ʙᴀʙʏ🥀:\n"
        if packnum > 0:
            firstpackname = "a" + str(user.id) + "_by_" + context.bot.username
            for i in range(0, packnum + 1):
                if i == 0:
                    packs += f"[pack](t.me/addstickers/{firstpackname})\n"
                else:
                    packs += f"[pack{i}](t.me/addstickers/{packname})\n"
        else:
            packs += f"[pack](t.me/addstickers/{packname})"
        msg.reply_text(packs, parse_mode=ParseMode.MARKDOWN)
    try:
        if os.path.isfile("kangsticker.png"):
            os.remove("kangsticker.png")
        elif os.path.isfile("kangsticker.tgs"):
            os.remove("kangsticker.tgs")
    except:
        pass


def makepack_internal(
    update,
    context,
    msg,
    user,
    emoji,
    packname,
    packnum,
    png_sticker=None,
    tgs_sticker=None,
):
    name = user.first_name
    name = name[:50]
    try:
        extra_version = ""
        if packnum > 0:
            extra_version = " " + str(packnum)
        if png_sticker:
            success = context.bot.create_new_sticker_set(
                user.id,
                packname,
                f"{name}ꜱ ᴋᴀɴɢ ᴘᴀᴄᴋ ʙᴀʙʏ🥀" + extra_version,
                png_sticker=png_sticker,
                emojis=emoji,
            )
        if tgs_sticker:
            success = context.bot.create_new_sticker_set(
                user.id,
                packname,
                f"{name}ꜱ ᴀɴɪᴍᴀᴛᴇᴅ ᴋᴀɴɢ ᴘᴀᴄᴋ ʙᴀʙʏ🥀" + extra_version,
                tgs_sticker=tgs_sticker,
                emojis=emoji,
            )

    except TelegramError as e:
        print(e)
        if e.message == "Sticker set name is already occupied":
            msg.reply_text(
                "ʏᴏᴜʀ ᴘᴀᴄᴋ ᴄᴀɴ ʙᴇ ꜰᴏᴜɴᴅ [ʜᴇʀᴇ](t.me/addstickers/%s) ʙᴀʙʏ🥀" % packname,
                parse_mode=ParseMode.MARKDOWN,
            )
        elif e.message in ("Peer_id_invalid", "bot was blocked by the user"):
            msg.reply_text(
                "ᴄᴏɴᴛᴀᴄᴛ ᴍᴇ ɪɴ ᴘᴍ ꜰɪʀꜱᴛ ʙᴀʙʏ🥀.",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="ꜱᴛᴀʀᴛ", url=f"t.me/{context.bot.username}"
                            )
                        ]
                    ]
                ),
            )
        elif e.message == "Internal Server Error: created sticker set not found (500)":
            msg.reply_text(
                "ꜱᴛɪᴄᴋᴇʀ ᴘᴀᴄᴋ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴄʀᴇᴀᴛᴇᴅ. ɢᴇᴛ ɪᴛ [ʜᴇʀᴇ](t.me/addstickers/%s) ʙᴀʙʏ🥀"
                % packname,
                parse_mode=ParseMode.MARKDOWN,
            )
        return

    if success:
        msg.reply_text(
            "ꜱᴛɪᴄᴋᴇʀ ᴘᴀᴄᴋ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴄʀᴇᴀᴛᴇᴅ. ɢᴇᴛ ɪᴛ [ʜᴇʀᴇ](t.me/addstickers/%s) ʙᴀʙʏ🥀"
            % packname,
            parse_mode=ParseMode.MARKDOWN,
        )
    else:
        msg.reply_text("ꜰᴀɪʟᴇᴅ ᴛᴏ ᴄʀᴇᴀᴛᴇ ꜱᴛɪᴄᴋᴇʀ ᴘᴀᴄᴋ. ᴘᴏꜱꜱɪʙʟʏ ᴅᴜᴇ ᴛᴏ ʙʟᴀᴄᴋ ᴍᴀɢɪᴄ ʙᴀʙʏ🥀.")


__help__ = """

» `/stickerid`*:* ʀᴇᴘʟʏ ᴛᴏ ᴀ ꜱᴛɪᴄᴋᴇʀ ᴛᴏ ᴍᴇ ᴛᴏ ᴛᴇʟʟ ʏᴏᴜ ɪᴛꜱ ꜰɪʟᴇ ɪᴅ.
» `/getsticker`*:* ʀᴇᴘʟʏ ᴛᴏ ᴀ ꜱᴛɪᴄᴋᴇʀ ᴛᴏ ᴍᴇ ᴛᴏ ᴜᴘʟᴏᴀᴅ ɪᴛꜱ ʀᴀᴡ ᴘɴɢ ꜰɪʟᴇ.
» `/kang`*:* ʀᴇᴘʟʏ ᴛᴏ ᴀ ꜱᴛɪᴄᴋᴇʀ ᴛᴏ ᴀᴅᴅ ɪᴛ ᴛᴏ ʏᴏᴜʀ ᴘᴀᴄᴋ.
» `/stickers`*:* ꜰɪɴᴅ ꜱᴛɪᴄᴋᴇʀꜱ ꜰᴏʀ ɢɪᴠᴇɴ ᴛᴇʀᴍ ᴏɴ ᴄᴏᴍʙᴏᴛ ꜱᴛɪᴄᴋᴇʀ ᴄᴀᴛᴀʟᴏɢᴜᴇ
» `/tiny`*:* ᴛᴏ ᴍᴀᴋᴇ ꜱᴍᴀʟʟ ꜱᴛɪᴄᴋᴇʀ
» `/kamuii` <1-8> *:* ᴛᴏ ᴅᴇᴇᴘᴇꜰʏɪɴɢ ꜱᴛɪᴋᴇʀ
» `/mmf` <ʀᴇᴘʟʏ ᴡɪᴛʜ ᴛᴇxᴛ>*:* ᴛᴏ ᴅʀᴀᴡ ᴀ ᴛᴇxᴛ ꜰᴏʀ ꜱᴛɪᴄᴋᴇʀ ᴏʀ ᴘᴏʜᴏᴛꜱ
"""

__mod_name__ = "STICKER"
STICKERID_HANDLER = DisableAbleCommandHandler("stickerid", stickerid)
GETSTICKER_HANDLER = DisableAbleCommandHandler("getsticker", getsticker)
KANG_HANDLER = DisableAbleCommandHandler("kang", kang, admin_ok=True)
STICKERS_HANDLER = DisableAbleCommandHandler("stickers", cb_sticker)

dispatcher.add_handler(STICKERS_HANDLER)
dispatcher.add_handler(STICKERID_HANDLER)
dispatcher.add_handler(GETSTICKER_HANDLER)
dispatcher.add_handler(KANG_HANDLER)
