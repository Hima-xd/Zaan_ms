import html
import re
import os
import requests
import datetime
import platform
import time

from psutil import cpu_percent, virtual_memory, disk_usage, boot_time
from platform import python_version
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import ChannelParticipantsAdmins
from telethon import events

from telegram import MAX_MESSAGE_LENGTH, ParseMode, Update, MessageEntity, __version__ as ptbver, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler
from telegram.ext.dispatcher import run_async
from telegram.error import BadRequest
from telegram.utils.helpers import escape_markdown, mention_html
    
from KRISTY import (
    DEV_USERS,
    OWNER_ID,
    DRAGONS,
    DEMONS,
    TIGERS,
    WOLVES,
    INFOPIC,
    dispatcher,
    sw,
    StartTime,
    SUPPORT_CHAT,
    BOT_NAME,
)
from KRISTY.__main__ import STATS, TOKEN, USER_INFO
from KRISTY.modules.sql import SESSION
import KRISTY.modules.sql.userinfo_sql as sql
from KRISTY.modules.disable import DisableAbleCommandHandler
from KRISTY.modules.sql.global_bans_sql import is_user_gbanned
from KRISTY.modules.sql.afk_sql import is_afk, set_afk
from KRISTY.modules.sql.users_sql import get_user_num_chats
from KRISTY.modules.helper_funcs.chat_status import sudo_plus
from KRISTY.modules.helper_funcs.extraction import extract_user
from KRISTY import telethn

def no_by_per(totalhp, percentage):
    """
    rtype: num of `percentage` from total
    eg: 1000, 10 -> 10% of 1000 (100)
    """
    return totalhp * percentage / 100


def get_percentage(totalhp, earnedhp):
    """
    rtype: percentage of `totalhp` num
    eg: (1000, 100) will return 10%
    """

    matched_less = totalhp - earnedhp
    per_of_totalhp = 100 - matched_less * 100.0 / totalhp
    per_of_totalhp = str(int(per_of_totalhp))
    return per_of_totalhp

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time

def hpmanager(user):
    total_hp = (get_user_num_chats(user.id) + 10) * 10

    if not is_user_gbanned(user.id):

        # Assign new var `new_hp` since we need `total_hp` in
        # end to calculate percentage.
        new_hp = total_hp

        # if no username decrease 25% of hp.
        if not user.username:
            new_hp -= no_by_per(total_hp, 25)
        try:
            dispatcher.bot.get_user_profile_photos(user.id).photos[0][-1]
        except IndexError:
            # no profile photo ==> -25% of hp
            new_hp -= no_by_per(total_hp, 25)
        # if no /setme exist ==> -20% of hp
        if not sql.get_user_me_info(user.id):
            new_hp -= no_by_per(total_hp, 20)
        # if no bio exsit ==> -10% of hp
        if not sql.get_user_bio(user.id):
            new_hp -= no_by_per(total_hp, 10)

        if is_afk(user.id):
            afkst = set_afk(user.id)
            # if user is afk and no reason then decrease 7%
            # else if reason exist decrease 5%
            new_hp -= no_by_per(total_hp, 7) if not afkst else no_by_per(total_hp, 5)
            # fbanned users will have (2*number of fbans) less from max HP
            # Example: if HP is 100 but user has 5 diff fbans
            # Available HP is (2*5) = 10% less than Max HP
            # So.. 10% of 100HP = 90HP

    else:
        new_hp = no_by_per(total_hp, 5)

    return {
        "earnedhp": int(new_hp),
        "totalhp": int(total_hp),
        "percentage": get_percentage(total_hp, new_hp),
    }


def make_bar(per):
    done = min(round(per / 10), 10)
    return "■" * done + "□" * (10 - done)


def get_id(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message
    chat = update.effective_chat
    msg = update.effective_message
    user_id = extract_user(msg, args)

    if user_id:

        if msg.reply_to_message and msg.reply_to_message.forward_from:

            user1 = message.reply_to_message.from_user
            user2 = message.reply_to_message.forward_from

            msg.reply_text(
                f"<b>ᴛᴇʟᴇɢʀᴀᴍ ɪᴅ:</b>\n"
                f"• {html.escape(user2.first_name)} - <code>{user2.id}</code>.\n"
                f"• {html.escape(user1.first_name)} - <code>{user1.id}</code> ʙᴀʙʏ🥀.",
                parse_mode=ParseMode.HTML,
            )

        else:

            user = bot.get_chat(user_id)
            msg.reply_text(
                f"{html.escape(user.first_name)}'s id is <code>{user.id}</code> ʙᴀʙʏ🥀.",
                parse_mode=ParseMode.HTML,
            )

    elif chat.type == "private":
        msg.reply_text(
            f"ʏᴏᴜʀ ɪᴅ ɪꜱ <code>{chat.id}</code> ʙᴀʙʏ🥀.", parse_mode=ParseMode.HTML,
        )

    else:
        msg.reply_text(
            f"ᴛʜɪꜱ ɢʀᴏᴜᴘ'ꜱ ɪᴅ ɪꜱ <code>{chat.id}</code> ʙᴀʙʏ🥀.", parse_mode=ParseMode.HTML,
        )


@telethn.on(
    events.NewMessage(
        pattern="/ginfo ", from_users=(TIGERS or []) + (DRAGONS or []) + (DEMONS or []),
    ),
)
async def group_info(event) -> None:
    chat = event.text.split(" ", 1)[1]
    try:
        entity = await event.client.get_entity(chat)
        totallist = await event.client.get_participants(
            entity, filter=ChannelParticipantsAdmins,
        )
        ch_full = await event.client(GetFullChannelRequest(channel=entity))
    except:
        await event.reply(
            "ᴄᴀɴ'ᴛ ꜰᴏʀ ꜱᴏᴍᴇ ʀᴇᴀꜱᴏɴ, ᴍᴀʏʙᴇ ɪᴛ ɪꜱ ᴀ ᴘʀɪᴠᴀᴛᴇ ᴏɴᴇ ᴏʀ ᴛʜᴀᴛ ɪ ᴀᴍ ʙᴀɴɴᴇᴅ ᴛʜᴇʀᴇ ʙᴀʙʏ🥀.",
        )
        return
    msg = f"**ɪᴅ**: `{entity.id}`"
    msg += f"\n**ᴛɪᴛʟᴇ**: `{entity.title}`"
    msg += f"\n**ᴅᴀᴛᴀᴄᴇɴᴛᴇʀ**: `{entity.photo.dc_id}`"
    msg += f"\n**ᴠɪᴅᴇᴏ ᴘꜰᴘ**: `{entity.photo.has_video}`"
    msg += f"\n**ꜱᴜᴘᴇʀɢʀᴏᴜᴘ**: `{entity.megagroup}`"
    msg += f"\n**ʀᴇꜱᴛʀɪᴄᴛᴇᴅ**: `{entity.restricted}`"
    msg += f"\n**ꜱᴄᴀᴍ**: `{entity.scam}`"
    msg += f"\n**ꜱʟᴏᴡᴍᴏᴅᴇ**: `{entity.slowmode_enabled}`"
    if entity.username:
        msg += f"\n**ᴜꜱᴇʀɴᴀᴍᴇ**: {entity.username}"
    msg += "\n\n**ᴍᴇᴍʙᴇʀ ꜱᴛᴀᴛꜱ:**"
    msg += f"\n`ᴀᴅᴍɪɴꜱ:` `{len(totallist)}`"
    msg += f"\n`ᴜꜱᴇʀꜱ`: `{totallist.total}`"
    msg += "\n\n**ᴀᴅᴍɪɴꜱ ʟɪꜱᴛ:**"
    for x in totallist:
        msg += f"\n• [{x.id}](tg://user?id={x.id})"
    msg += f"\n\n**ᴅᴇꜱᴄʀɪᴘᴛɪᴏɴ**:\n`{ch_full.full_chat.about}`"
    await event.reply(msg)



def gifid(update: Update, context: CallbackContext):
    msg = update.effective_message
    if msg.reply_to_message and msg.reply_to_message.animation:
        update.effective_message.reply_text(
            f"ɢɪꜰ ɪᴅ:\n<code>{msg.reply_to_message.animation.file_id}</code> ʙᴀʙʏ🥀",
            parse_mode=ParseMode.HTML,
        )
    else:
        update.effective_message.reply_text("ᴘʟᴇᴀꜱᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ɢɪꜰ ᴛᴏ ɢᴇᴛ ɪᴛꜱ ɪᴅ ʙᴀʙʏ🥀.")


def info(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message
    chat = update.effective_chat
    user_id = extract_user(update.effective_message, args)

    if user_id:
        user = bot.get_chat(user_id)

    elif not message.reply_to_message and not args:
        user = message.from_user

    elif not message.reply_to_message and (
        not args
        or (
            len(args) >= 1
            and not args[0].startswith("@")
            and not args[0].isdigit()
            and not message.parse_entities([MessageEntity.TEXT_MENTION])
        )
    ):
        message.reply_text("ɪ ᴄᴀɴ'ᴛ ᴇxᴛʀᴀᴄᴛ ᴀ ᴜꜱᴇʀ ꜰʀᴏᴍ ᴛʜɪꜱ ʙᴀʙʏ🥀.")
        return

    else:
        return

    rep = message.reply_text(
        "<code> ɢᴇᴛᴛɪɴɢ ɪɴꜰᴏ ʙᴀʙʏ🥀 </code>", parse_mode=ParseMode.HTML)

    text = (f"╒═══「<b> ᴜꜱᴇʀ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ:</b> 」\n"
        f"» ɪᴅ : <code>{user.id}</code>\n"
        f"» ꜰɪʀꜱᴛ ɴᴀᴍᴇ: {html.escape(user.first_name)}"
    )    
    if user.last_name:
        text += f"\n» ʟᴀꜱᴛ ɴᴀᴍᴇ: {html.escape(user.last_name)}"

    if user.username:
        text += f"\n» ᴜꜱᴇʀɴᴀᴍᴇ: @{html.escape(user.username)}"

    text += f"\n» ᴜꜱᴇʀʟɪɴᴋ: {mention_html(user.id, 'link')}"

    if chat.type != "private" and user_id != bot.id:
        _stext = "\n» ᴘʀᴇꜱᴇɴᴄᴇ: <code>{}</code>"

        afk_st = is_afk(user.id)
        if afk_st:
            text += _stext.format("AFK")
        else:
            status = status = bot.get_chat_member(chat.id, user.id).status
            if status:
                if status in {"left", "kicked"}:
                    text += _stext.format("Not here")
                elif status == "member":
                    text += _stext.format("Detected")
                elif status in {"administrator", "creator"}:
                    text += _stext.format("Admin")
    if user_id not in [bot.id, 777000, 1087968824]:
        userhp = hpmanager(user)
        text += f"\n\n<b>ʜᴇᴀʟᴛʜ:</b> <code>{userhp['earnedhp']}/{userhp['totalhp']}</code>\n[<i>{make_bar(int(userhp['percentage']))} </i>{userhp['percentage']}%]"

    try:
        spamwtc = sw.get_ban(int(user.id))
        if spamwtc:
            text += "\n\n<b>ᴛʜɪꜱ ᴘᴇʀꜱᴏɴ ɪꜱ ꜱᴘᴀᴍᴡᴀᴛᴄʜᴇᴅ ʙᴀʙʏ🥀!</b>"
            text += f"\nʀᴇᴀꜱᴏɴ: <pre>{spamwtc.reason}</pre>"
            text += "\nᴀᴘᴘᴇᴀʟ ᴀᴛ @SpamWatchSupport"
        else:
            pass
    except:
        pass  # don't crash if api is down somehow...

    disaster_level_present = False

    if user.id == OWNER_ID:
        text += "\n\nᴛʜᴇ ᴅɪꜱᴀꜱᴛᴇʀ ʟᴇᴠᴇʟ ᴏꜰ ᴛʜɪꜱ ᴘᴇʀꜱᴏɴ ɪꜱ ᴋɪɴɢ ʙᴀʙʏ🥀."
        disaster_level_present = True
    elif user.id in DEV_USERS:
        text += "\n\nᴛʜɪꜱ ᴜꜱᴇʀ ɪꜱ ᴍᴇᴍʙᴇʀ ᴏꜰ 'Prince' ʙᴀʙʏ🥀."
        disaster_level_present = True
    elif user.id in DRAGONS:
        text += "\n\nᴛʜᴇ ᴅɪꜱᴀꜱᴛᴇʀ ʟᴇᴠᴇʟ ᴏꜰ ᴛʜɪꜱ ᴘᴇʀꜱᴏɴ ɪꜱ ᴇᴍᴘᴇʀᴏʀ ʙᴀʙʏ🥀."
        disaster_level_present = True
    elif user.id in DEMONS:
        text += "\n\nᴛʜᴇ ᴅɪꜱᴀꜱᴛᴇʀ ʟᴇᴠᴇʟ ᴏꜰ ᴛʜɪꜱ ᴘᴇʀꜱᴏɴ ɪꜱ ɢᴏᴠᴇʀɴᴏʀ ʙᴀʙʏ🥀."
        disaster_level_present = True
    elif user.id in TIGERS:
        text += "\n\nᴛʜᴇ ᴅɪꜱᴀꜱᴛᴇʀ ʟᴇᴠᴇʟ ᴏꜰ ᴛʜɪꜱ ᴘᴇʀꜱᴏɴ ɪꜱ ᴄᴀᴘᴛᴀɪɴ ʙᴀʙʏ🥀."
        disaster_level_present = True
    elif user.id in WOLVES:
        text += "\n\nᴛʜᴇ ᴅɪꜱᴀꜱᴛᴇʀ ʟᴇᴠᴇʟ ᴏꜰ ᴛʜɪꜱ ᴘᴇʀꜱᴏɴ ɪꜱ ꜱᴏʟᴅɪᴇʀ ʙᴀʙʏ🥀."
        disaster_level_present = True
    elif user.id == 1820525265:
         text += "\n\nᴅᴇᴠᴇʟᴏᴘᴇʀ ᴏꜰ ʙᴏᴛ ʙᴀʙʏ🥀."
         disaster_level_present = True

    try:
        user_member = chat.get_member(user.id)
        if user_member.status == "administrator":
            result = requests.post(
                f"https://api.telegram.org/bot{TOKEN}/getChatMember?chat_id={chat.id}&user_id={user.id}",
            )
            result = result.json()["result"]
            if "custom_title" in result.keys():
                custom_title = result["custom_title"]
                text += f"\n\nᴛɪᴛʟᴇ:\n<b>{custom_title}</b>"
    except BadRequest:
        pass

    for mod in USER_INFO:
        try:
            mod_info = mod.__user_info__(user.id).strip()
        except TypeError:
            mod_info = mod.__user_info__(user.id, chat.id).strip()
        if mod_info:
            text += "\n\n" + mod_info

    if INFOPIC:
        try:
            profile = context.bot.get_user_profile_photos(user.id).photos[0][-1]
            context.bot.sendChatAction(chat.id, "upload_photo")
            context.bot.send_photo(
            chat.id,
            photo=profile,
            caption=(text),reply_markup=InlineKeyboardMarkup(
                [
                    [
                            InlineKeyboardButton(
                                "ʜᴇᴀʟᴛʜ", url="https://t.me/Kristy_Mf/6"),
                            InlineKeyboardButton(
                                "ꜱᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_CHAT}")
                    ],
                ]
            ),
                parse_mode=ParseMode.HTML,
            )

            os.remove(f"{user.id}.png")
        # Incase user don't have profile pic, send normal text
        except IndexError:
            message.reply_text(
                text, 
                reply_markup=InlineKeyboardMarkup(
                    [
[
                            InlineKeyboardButton(
                                "ʜᴇᴀʟᴛʜ", url="https://t.me/Kristy_Mf/6"),
                            InlineKeyboardButton(
                                "ꜱᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_CHAT}")
                    ],
                    ]
                ),
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True
            )

    else:
        message.reply_text(
            text, parse_mode=ParseMode.HTML,
        )

    rep.delete()


def about_me(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message
    user_id = extract_user(message, args)

    user = bot.get_chat(user_id) if user_id else message.from_user
    info = sql.get_user_me_info(user.id)

    if info:
        update.effective_message.reply_text(
            f"*{user.first_name}*:\n{escape_markdown(info)}",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
    elif message.reply_to_message:
        username = message.reply_to_message.from_user.first_name
        update.effective_message.reply_text(
            f"{username} ʜᴀꜱɴ'ᴛ ꜱᴇᴛ ᴀɴ ɪɴꜰᴏ ᴍᴇꜱꜱᴀɢᴇ ᴀʙᴏᴜᴛ ᴛʜᴇᴍꜱᴇʟᴠᴇꜱ ʏᴇᴛ ʙᴀʙʏ🥀!",
        )
    else:
        update.effective_message.reply_text("ᴛʜᴇʀᴇ ɪꜱɴᴛ ᴏɴᴇ, ᴜꜱᴇ /setme ᴛᴏ ꜱᴇᴛ ᴏɴᴇ ʙᴀʙʏ🥀.")


def set_about_me(update: Update, context: CallbackContext):
    message = update.effective_message
    user_id = message.from_user.id
    if user_id in [777000, 1087968824]:
        message.reply_text("ᴇʀʀᴏʀ! ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ ʙᴀʙʏ🥀")
        return
    bot = context.bot
    if message.reply_to_message:
        repl_message = message.reply_to_message
        repl_user_id = repl_message.from_user.id
        if repl_user_id in [bot.id, 777000, 1087968824] and (user_id in DEV_USERS):
            user_id = repl_user_id
    text = message.text
    info = text.split(None, 1)
    if len(info) == 2:
        if len(info[1]) < MAX_MESSAGE_LENGTH // 4:
            sql.set_user_me_info(user_id, info[1])
            if user_id in [777000, 1087968824]:
                message.reply_text("ᴀᴜᴛʜᴏʀɪᴢᴇᴅ...ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ ᴜᴘᴅᴀᴛᴇᴅ ʙᴀʙʏ🥀!")
            elif user_id == bot.id:
                message.reply_text("ɪ ʜᴀᴠᴇ ᴜᴘᴅᴀᴛᴇᴅ ᴍʏ ɪɴꜰᴏ ᴡɪᴛʜ ᴛʜᴇ ᴏɴᴇ ʏᴏᴜ ᴘʀᴏᴠɪᴅᴇᴅ ʙᴀʙʏ🥀!")
            else:
                message.reply_text("ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ ᴜᴘᴅᴀᴛᴇᴅ ʙᴀʙʏ🥀!")
        else:
            message.reply_text(
                "ᴛʜᴇ ɪɴꜰᴏ ɴᴇᴇᴅꜱ ᴛᴏ ʙᴇ ᴜɴᴅᴇʀ {} ᴄʜᴀʀᴀᴄᴛᴇʀꜱ! ʏᴏᴜ ʜᴀᴠᴇ {} ʙᴀʙʏ🥀.".format(
                    MAX_MESSAGE_LENGTH // 4,
                    len(info[1]),
                ),
            )

@sudo_plus
def stats(update: Update, context: CallbackContext):
    stats = "<b>╔═━「 ᴄᴜʀʀᴇɴᴛ ʙᴏᴛ ꜱᴛᴀᴛɪꜱᴛɪᴄꜱ 」</b>\n" + "\n".join([mod.__stats__() for mod in STATS])
    result = re.sub(r"(\d+)", r"<code>\1</code>", stats)
    result += f"\n<b>╘═━「 ᴘᴏᴡᴇʀᴇᴅ ʙʏ {BOT_NAME} 」</b>"
    update.effective_message.reply_text(
        result,
        parse_mode=ParseMode.HTML, 
        disable_web_page_preview=True
   )
        
        
def about_bio(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message

    user_id = extract_user(message, args)
    user = bot.get_chat(user_id) if user_id else message.from_user
    info = sql.get_user_bio(user.id)

    if info:
        update.effective_message.reply_text(
            "*{}*:\n{}".format(user.first_name, escape_markdown(info)),
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
    elif message.reply_to_message:
        username = user.first_name
        update.effective_message.reply_text(
            f"{username} ʜᴀꜱɴ'ᴛ ʜᴀᴅ ᴀ ᴍᴇꜱꜱᴀɢᴇ ꜱᴇᴛ ᴀʙᴏᴜᴛ ᴛʜᴇᴍꜱᴇʟᴠᴇꜱ ʏᴇᴛ!\nꜱᴇᴛ ᴏɴᴇ ᴜꜱɪɴɢ /setbio ʙᴀʙʏ🥀",
        )
    else:
        update.effective_message.reply_text(
            "ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ ʜᴀᴅ ᴀ ʙɪᴏ ꜱᴇᴛ ᴀʙᴏᴜᴛ ʏᴏᴜʀꜱᴇʟꜰ ʏᴇᴛ ʙᴀʙʏ🥀!",
        )


def set_about_bio(update: Update, context: CallbackContext):
    message = update.effective_message
    sender_id = update.effective_user.id
    bot = context.bot

    if message.reply_to_message:
        repl_message = message.reply_to_message
        user_id = repl_message.from_user.id

        if user_id == message.from_user.id:
            message.reply_text(
                "ʏᴏᴜ ᴄᴀɴ'ᴛ ꜱᴇᴛ ʏᴏᴜʀ ᴏᴡɴ ʙɪᴏ! ʏᴏᴜ'ʀᴇ ᴀᴛ ᴛʜᴇ ᴍᴇʀᴄʏ ᴏꜰ ᴏᴛʜᴇʀꜱ ʜᴇʀᴇ ʙᴀʙʏ🥀...",
            )
            return

        if user_id in [777000, 1087968824] and sender_id not in DEV_USERS:
            message.reply_text("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪꜱᴇᴅ ʙᴀʙʏ🥀")
            return

        if user_id == bot.id and sender_id not in DEV_USERS:
            message.reply_text(
                "ᴇʀᴍ... ʏᴇᴀʜ, ɪ ᴏɴʟʏ ᴛʀᴜꜱᴛ ᴛʜᴇ ᴀᴄᴋᴇʀᴍᴀɴꜱ ᴛᴏ ꜱᴇᴛ ᴍʏ ʙɪᴏ ʙᴀʙʏ🥀.",
            )
            return

        text = message.text
        bio = text.split(
            None, 1,
        )  # use python's maxsplit to only remove the cmd, hence keeping newlines.

        if len(bio) == 2:
            if len(bio[1]) < MAX_MESSAGE_LENGTH // 4:
                sql.set_user_bio(user_id, bio[1])
                message.reply_text(
                    "ᴜᴘᴅᴀᴛᴇᴅ {}'ꜱ ʙɪᴏ ʙᴀʙʏ🥀!".format(repl_message.from_user.first_name),
                )
            else:
                message.reply_text(
                    "ʙɪᴏ ɴᴇᴇᴅꜱ ᴛᴏ ʙᴇ ᴜɴᴅᴇʀ {} ᴄʜᴀʀᴀᴄᴛᴇʀꜱ! ʏᴏᴜ ᴛʀɪᴇᴅ ᴛᴏ ꜱᴇᴛ {} ʙᴀʙʏ🥀.".format(
                        MAX_MESSAGE_LENGTH // 4, len(bio[1]),
                    ),
                )
    else:
        message.reply_text("ʀᴇᴘʟʏ ᴛᴏ ꜱᴏᴍᴇᴏɴᴇ ᴛᴏ ꜱᴇᴛ ᴛʜᴇɪʀ ʙɪᴏ ʙᴀʙʏ🥀!")


def __user_info__(user_id):
    bio = html.escape(sql.get_user_bio(user_id) or "")
    me = html.escape(sql.get_user_me_info(user_id) or "")
    result = ""
    if me:
        result += f"<b>ᴀʙᴏᴜᴛ ᴜꜱᴇʀ:</b>\n{me}\n"
    if bio:
        result += f"<b>ᴡʜᴀᴛ ᴏᴛʜᴇʀ ꜱᴀʏ:</b>\n{bio}\n"
    result = result.strip("\n")
    return result


__help__ = """

*ɪᴅ:*
» `/id`*:* ɢᴇᴛ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ɢʀᴏᴜᴘ ɪᴅ. ɪꜰ ᴜꜱᴇᴅ ʙʏ ʀᴇᴘʟʏɪɴɢ ᴛᴏ ᴀ ᴍᴇꜱꜱᴀɢᴇ, ɢᴇᴛꜱ ᴛʜᴀᴛ ᴜꜱᴇʀ'ꜱ ɪᴅ.
» `/gifid`*:* ʀᴇᴘʟʏ ᴛᴏ ᴀ ɢɪꜰ ᴛᴏ ᴍᴇ ᴛᴏ ᴛᴇʟʟ ʏᴏᴜ ɪᴛꜱ ꜰɪʟᴇ ɪᴅ.

 *ꜱᴇʟꜰ ᴀᴅᴅᴅᴇᴅ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ:* 
» `/setme` <ᴛᴇxᴛ>*:* ᴡɪʟʟ ꜱᴇᴛ ʏᴏᴜʀ ɪɴꜰᴏ
» `/me`*:* ᴡɪʟʟ ɢᴇᴛ ʏᴏᴜʀ ᴏʀ ᴀɴᴏᴛʜᴇʀ ᴜꜱᴇʀ'ꜱ ɪɴꜰᴏ.
ᴇxᴀᴍᴘʟᴇꜱ:
» `/setme` ɪ ᴀᴍ ᴀ ᴡᴏʟꜰ.
» `/me` @ᴜꜱᴇʀɴᴀᴍᴇ(ᴅᴇꜰᴀᴜʟᴛꜱ ᴛᴏ ʏᴏᴜʀꜱ ɪꜰ ɴᴏ ᴜꜱᴇʀ ꜱᴘᴇᴄɪꜰɪᴇᴅ) 

*ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ ᴏᴛʜᴇʀꜱ ᴀᴅᴅ ᴏɴ ʏᴏᴜ:* 
» `/bio`*:* ᴡɪʟʟ ɢᴇᴛ ʏᴏᴜʀ ᴏʀ ᴀɴᴏᴛʜᴇʀ ᴜꜱᴇʀ'ꜱ ʙɪᴏ. ᴛʜɪꜱ ᴄᴀɴɴᴏᴛ ʙᴇ ꜱᴇᴛ ʙʏ ʏᴏᴜʀꜱᴇʟꜰ.
» `/setbio` <ᴛᴇxᴛ>*:* ᴡʜɪʟᴇ ʀᴇᴘʟʏɪɴɢ, ᴡɪʟʟ ꜱᴀᴠᴇ ᴀɴᴏᴛʜᴇʀ ᴜꜱᴇʀ'ꜱ 
ʙɪᴏ ᴇxᴀᴍᴘʟᴇꜱ:
» `/bio` @ᴜꜱᴇʀɴᴀᴍᴇ(ᴅᴇꜰᴀᴜʟᴛꜱ ᴛᴏ ʏᴏᴜʀꜱ ɪꜰ ɴᴏᴛ ꜱᴘᴇᴄɪꜰɪᴇᴅ).
» `/setbio` ᴛʜɪꜱ ᴜꜱᴇʀ ɪꜱ ᴀ ᴡᴏʟꜰ (ʀᴇᴘʟʏ ᴛᴏ ᴛʜᴇ ᴜꜱᴇʀ) 

*ᴏᴠᴇʀᴀʟʟ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ʏᴏᴜ:*
» `/info`*:* ɢᴇᴛ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴀ ᴜꜱᴇʀ. 

 *ᴡʜᴀᴛ ɪꜱ ᴛʜᴀᴛ ʜᴇᴀʟᴛʜ ᴛʜɪɴɢʏ?*
  ᴄᴏᴍᴇ ᴀɴᴅ ꜱᴇᴇ [ʜᴘ ꜱʏꜱᴛᴇᴍ ᴇxᴘʟᴀɪɴᴇᴅ](https://t.me/Kristy_Mf/6)


"""

SET_BIO_HANDLER = DisableAbleCommandHandler("setbio", set_about_bio, run_async=True)
GET_BIO_HANDLER = DisableAbleCommandHandler("bio", about_bio, run_async=True)

STATS_HANDLER = CommandHandler(["stats", "statistics"], stats, run_async=True)
ID_HANDLER = DisableAbleCommandHandler("id", get_id, run_async=True)
GIFID_HANDLER = DisableAbleCommandHandler("gifid", gifid, run_async=True)
INFO_HANDLER = DisableAbleCommandHandler("info", info, run_async=True)

SET_ABOUT_HANDLER = DisableAbleCommandHandler("setme", set_about_me, run_async=True)
GET_ABOUT_HANDLER = DisableAbleCommandHandler("me", about_me, run_async=True)

dispatcher.add_handler(STATS_HANDLER)
dispatcher.add_handler(ID_HANDLER)
dispatcher.add_handler(GIFID_HANDLER)
dispatcher.add_handler(INFO_HANDLER)
dispatcher.add_handler(SET_BIO_HANDLER)
dispatcher.add_handler(GET_BIO_HANDLER)
dispatcher.add_handler(SET_ABOUT_HANDLER)
dispatcher.add_handler(GET_ABOUT_HANDLER)

__mod_name__ = "INFO"
__command_list__ = ["setbio", "bio", "setme", "me", "info"]
__handlers__ = [
    ID_HANDLER,
    GIFID_HANDLER,
    INFO_HANDLER,
    SET_BIO_HANDLER,
    GET_BIO_HANDLER,
    SET_ABOUT_HANDLER,
    GET_ABOUT_HANDLER,
    STATS_HANDLER,
]
