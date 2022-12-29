import html
import json
import os
from typing import Optional

from KRISTY import (DEV_USERS, OWNER_ID, DRAGONS, SUPPORT_CHAT, DEMONS,
                          TIGERS, WOLVES, dispatcher)
from KRISTY.modules.helper_funcs.chat_status import (dev_plus, sudo_plus,
                                                           whitelist_plus)
from KRISTY.modules.helper_funcs.extraction import extract_user
from KRISTY.modules.log_channel import gloggable
from telegram import ParseMode, TelegramError, Update
from telegram.ext import CallbackContext, CommandHandler, run_async
from telegram.utils.helpers import mention_html

ELEVATED_USERS_FILE = os.path.join(os.getcwd(),
                                   'KRISTY/elevated_users.json')


def check_user_id(user_id: int, context: CallbackContext) -> Optional[str]:
    bot = context.bot
    if not user_id:
        reply = "ᴛʜᴀᴛ...ɪꜱ ᴀ ᴄʜᴀᴛ ʙᴀʙʏ🥀! ʙᴀᴋᴀ ᴋᴀ ᴏᴍᴀᴇ?"

    elif user_id == bot.id:
        reply = "ᴛʜɪꜱ ᴅᴏᴇꜱ ɴᴏᴛ ᴡᴏʀᴋ ᴛʜᴀᴛ ᴡᴀʏ ʙᴀʙʏ🥀."

    else:
        reply = None
    return reply


# This can serve as a deeplink example.
#disasters =
# """ Text here """

# do not async, not a handler
#def send_disasters(update):
#    update.effective_message.reply_text(
#        disasters, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

### Deep link example ends


@run_async
@dev_plus
@gloggable
def addsudo(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in DRAGONS:
        message.reply_text("ᴛʜɪꜱ ᴍᴇᴍʙᴇʀ ɪꜱ ᴀʟʀᴇᴀᴅʏ ᴀ ᴅʀᴀɢᴏɴ ᴅɪꜱᴀꜱᴛᴇʀ ʙᴀʙʏ🥀")
        return ""

    if user_id in DEMONS:
        rt += "Requested HA to promote a Demon Disaster to Dragon."
        data['supports'].remove(user_id)
        DEMONS.remove(user_id)

    if user_id in WOLVES:
        rt += "Requested HA to promote a Wolf Disaster to Dragon."
        data['whitelists'].remove(user_id)
        WOLVES.remove(user_id)

    data['sudos'].append(user_id)
    DRAGONS.append(user_id)

    with open(ELEVATED_USERS_FILE, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt + "\nꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ꜱᴇᴛ ᴅɪꜱᴀꜱᴛᴇʀ ʟᴇᴠᴇʟ ᴏꜰ {} ᴛᴏ ᴅʀᴀɢᴏɴ ʙᴀʙʏ🥀!".format(
            user_member.first_name))

    log_message = (
        f"#ꜱᴜᴅᴏ\n"
        f"<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>ᴜꜱᴇʀ:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != 'private':
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@run_async
@sudo_plus
@gloggable
def addsupport(
    update: Update,
    context: CallbackContext,
) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in DRAGONS:
        rt += "Requested HA to deomote this Dragon to Demon"
        data['sudos'].remove(user_id)
        DRAGONS.remove(user_id)

    if user_id in DEMONS:
        message.reply_text("ᴛʜɪꜱ ᴜꜱᴇʀ ɪꜱ ᴀʟʀᴇᴀᴅʏ ᴀ ᴅᴇᴍᴏɴ ᴅɪꜱᴀꜱᴛᴇʀ ʙᴀʙʏ🥀.")
        return ""

    if user_id in WOLVES:
        rt += "Requested HA to promote this Wolf Disaster to Demon"
        data['whitelists'].remove(user_id)
        WOLVES.remove(user_id)

    data['supports'].append(user_id)
    DEMONS.append(user_id)

    with open(ELEVATED_USERS_FILE, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt + f"\n{user_member.first_name} ᴡᴀꜱ ᴀᴅᴅᴇᴅ ᴀꜱ ᴀ ᴅᴇᴍᴏɴ ᴅɪꜱᴀꜱᴛᴇʀ ʙᴀʙʏ🥀!")

    log_message = (
        f"#ꜱᴜᴘᴘᴏʀᴛ\n"
        f"<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>ᴜꜱᴇʀ:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != 'private':
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@run_async
@sudo_plus
@gloggable
def addwhitelist(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in DRAGONS:
        rt += "This member is a Dragon Disaster, Demoting to Wolf."
        data['sudos'].remove(user_id)
        DRAGONS.remove(user_id)

    if user_id in DEMONS:
        rt += "This user is already a Demon Disaster, Demoting to Wolf."
        data['supports'].remove(user_id)
        DEMONS.remove(user_id)

    if user_id in WOLVES:
        message.reply_text("ᴛʜɪꜱ ᴜꜱᴇʀ ɪꜱ ᴀʟʀᴇᴀᴅʏ ᴀ ᴡᴏʟꜰ ᴅɪꜱᴀꜱᴛᴇʀ ʙᴀʙʏ🥀.")
        return ""

    data['whitelists'].append(user_id)
    WOLVES.append(user_id)

    with open(ELEVATED_USERS_FILE, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt +
        f"\nꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴘʀᴏᴍᴏᴛᴇᴅ {user_member.first_name} ᴛᴏ ᴀ ᴡᴏʟꜰ ᴅɪꜱᴀꜱᴛᴇʀ ʙᴀʙʏ🥀!")

    log_message = (
        f"#ᴡʜɪᴛᴇʟɪꜱᴛ\n"
        f"<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, html.escape(user.first_name))} \n"
        f"<b>ᴜꜱᴇʀ:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != 'private':
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@run_async
@sudo_plus
@gloggable
def addtiger(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in DRAGONS:
        rt += "This member is a Dragon Disaster, Demoting to Tiger."
        data['sudos'].remove(user_id)
        DRAGONS.remove(user_id)

    if user_id in DEMONS:
        rt += "This user is already a Demon Disaster, Demoting to Tiger."
        data['supports'].remove(user_id)
        DEMONS.remove(user_id)

    if user_id in WOLVES:
        rt += "This user is already a Wolf Disaster, Demoting to Tiger."
        data['whitelists'].remove(user_id)
        WOLVES.remove(user_id)

    if user_id in TIGERS:
        message.reply_text("ᴛʜɪꜱ ᴜꜱᴇʀ ɪꜱ ᴀʟʀᴇᴀᴅʏ ᴀ ᴛɪɢᴇʀ ʙᴀʙʏ🥀.")
        return ""

    data['tigers'].append(user_id)
    TIGERS.append(user_id)

    with open(ELEVATED_USERS_FILE, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt +
        f"\nꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴘʀᴏᴍᴏᴛᴇᴅ {user_member.first_name} ᴛᴏ ᴀ ᴛɪɢᴇʀ ᴅɪꜱᴀꜱᴛᴇʀ ʙᴀʙʏ🥀!"
    )

    log_message = (
        f"#ᴛɪɢᴇʀ\n"
        f"<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, html.escape(user.first_name))} \n"
        f"<b>ᴜꜱᴇʀ:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != 'private':
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@run_async
@dev_plus
@gloggable
def removesudo(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in DRAGONS:
        message.reply_text("ʀᴇQᴜᴇꜱᴛᴇᴅ ʜᴀ ᴛᴏ ᴅᴇᴍᴏᴛᴇ ᴛʜɪꜱ ᴜꜱᴇʀ ᴛᴏ ᴄɪᴠɪʟɪᴀɴ ʙᴀʙʏ🥀")
        DRAGONS.remove(user_id)
        data['sudos'].remove(user_id)

        with open(ELEVATED_USERS_FILE, 'w') as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#ᴜɴꜱᴜᴅᴏ\n"
            f"<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>ᴜꜱᴇʀ:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != 'private':
            log_message = "<b>{}:</b>\n".format(html.escape(
                chat.title)) + log_message

        return log_message

    else:
        message.reply_text("ᴛʜɪꜱ ᴜꜱᴇʀ ɪꜱ ɴᴏᴛ ᴀ ᴅʀᴀɢᴏɴ ᴅɪꜱᴀꜱᴛᴇʀ ʙᴀʙʏ🥀!")
        return ""


@run_async
@sudo_plus
@gloggable
def removesupport(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in DEMONS:
        message.reply_text("ʀᴇQᴜᴇꜱᴛᴇᴅ ʜᴀ ᴛᴏ ᴅᴇᴍᴏᴛᴇ ᴛʜɪꜱ ᴜꜱᴇʀ ᴛᴏ ᴄɪᴠɪʟɪᴀɴ ʙᴀʙʏ🥀")
        DEMONS.remove(user_id)
        data['supports'].remove(user_id)

        with open(ELEVATED_USERS_FILE, 'w') as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#ᴜɴꜱᴜᴘᴘᴏʀᴛ\n"
            f"<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>ᴜꜱᴇʀ:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != 'private':
            log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

        return log_message

    else:
        message.reply_text("ᴛʜɪꜱ ᴜꜱᴇʀ ɪꜱ ɴᴏᴛ ᴀ ᴅᴇᴍᴏɴ ʟᴇᴠᴇʟ ᴅɪꜱᴀꜱᴛᴇʀ ʙᴀʙʏ🥀!")
        return ""


@run_async
@sudo_plus
@gloggable
def removewhitelist(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in WOLVES:
        message.reply_text("ᴅᴇᴍᴏᴛɪɴɢ ᴛᴏ ɴᴏʀᴍᴀʟ ᴜꜱᴇʀ")
        WOLVES.remove(user_id)
        data['whitelists'].remove(user_id)

        with open(ELEVATED_USERS_FILE, 'w') as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#ᴜɴᴡʜɪᴛᴇʟɪꜱᴛ\n"
            f"<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>ᴜꜱᴇʀ:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != 'private':
            log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

        return log_message
    else:
        message.reply_text("ᴛʜɪꜱ ᴜꜱᴇʀ ɪꜱ ɴᴏᴛ ᴀ ᴡᴏʟꜰ ᴅɪꜱᴀꜱᴛᴇʀ ʙᴀʙʏ🥀!")
        return ""


@run_async
@sudo_plus
@gloggable
def removetiger(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in TIGERS:
        message.reply_text("ᴅᴇᴍᴏᴛɪɴɢ ᴛᴏ ɴᴏʀᴍᴀʟ ᴜꜱᴇʀ ʙᴀʙʏ🥀")
        TIGERS.remove(user_id)
        data['tigers'].remove(user_id)

        with open(ELEVATED_USERS_FILE, 'w') as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#ᴜɴᴛɪɢᴇʀ\n"
            f"<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>ᴜꜱᴇʀ:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != 'private':
            log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

        return log_message
    else:
        message.reply_text("ᴛʜɪꜱ ᴜꜱᴇʀ ɪꜱ ɴᴏᴛ ᴀ ᴛɪɢᴇʀ ᴅɪꜱᴀꜱᴛᴇʀ ʙᴀʙʏ🥀!")
        return ""


@run_async
@whitelist_plus
def whitelistlist(update: Update, context: CallbackContext):
    reply = "<b>ᴋɴᴏᴡɴ ᴡᴏʟꜰ ᴅɪꜱᴀꜱᴛᴇʀꜱ 🐺:</b>\n"
    bot = context.bot
    for each_user in WOLVES:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)

            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)


@run_async
@whitelist_plus
def tigerlist(update: Update, context: CallbackContext):
    reply = "<b>ᴋɴᴏᴡɴ ᴛɪɢᴇʀ ᴅɪꜱᴀꜱᴛᴇʀꜱ 🐯:</b>\n"
    bot = context.bot
    for each_user in TIGERS:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)


@run_async
@whitelist_plus
def supportlist(update: Update, context: CallbackContext):
    bot = context.bot
    reply = "<b>ᴋɴᴏᴡɴ ᴅᴇᴍᴏɴ ᴅɪꜱᴀꜱᴛᴇʀꜱ 👹:</b>\n"
    for each_user in DEMONS:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)


@run_async
@whitelist_plus
def sudolist(update: Update, context: CallbackContext):
    bot = context.bot
    true_sudo = list(set(DRAGONS) - set(DEV_USERS))
    reply = "<b>ᴋɴᴏᴡɴ ᴅʀᴀɢᴏɴ ᴅɪꜱᴀꜱᴛᴇʀꜱ 🐉:</b>\n"
    for each_user in true_sudo:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)


@run_async
@whitelist_plus
def devlist(update: Update, context: CallbackContext):
    bot = context.bot
    true_dev = list(set(DEV_USERS) - {OWNER_ID})
    reply = "<b>ʜᴇʀᴏ ᴀꜱꜱᴏᴄɪᴀᴛɪᴏɴ ᴍᴇᴍʙᴇʀꜱ ⚡️:</b>\n"
    for each_user in true_dev:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)


__help__ = f"""
*⚠️ Notice:*
ᴄᴏᴍᴍᴀɴᴅꜱ ʟɪꜱᴛᴇᴅ ʜᴇʀᴇ ᴏɴʟʏ ᴡᴏʀᴋ ꜰᴏʀ ᴜꜱᴇʀꜱ ᴡɪᴛʜ ꜱᴘᴇᴄɪᴀʟ ᴀᴄᴄᴇꜱꜱ ᴀʀᴇ ᴍᴀɪɴʟʏ ᴜꜱᴇᴅ ꜰᴏʀ ᴛʀᴏᴜʙʟᴇꜱʜᴏᴏᴛɪɴɢ, ᴅᴇʙᴜɢɢɪɴɢ ᴘᴜʀᴘᴏꜱᴇꜱ.
ɢʀᴏᴜᴘ ᴀᴅᴍɪɴꜱ/ɢʀᴏᴜᴘ-ᴏᴡɴᴇʀꜱ ᴅᴏ ɴᴏᴛ ɴᴇᴇᴅ ᴛʜᴇꜱᴇ ᴄᴏᴍᴍᴀɴᴅꜱ.
 *List all special users:*
 » `/dragons`*:* ʟɪꜱᴛꜱ ᴀʟʟ ᴅʀᴀɢᴏɴ ᴅɪꜱᴀꜱᴛᴇʀꜱ
 » `/dragons`*:*ʟɪꜱᴛꜱ ᴀʟʟ ᴅᴇᴍᴏɴ ᴅɪꜱᴀꜱᴛᴇʀꜱ
 » `/tigers`*:* ʟɪꜱᴛꜱ ᴀʟʟ ᴛɪɢᴇʀꜱ ᴅɪꜱᴀꜱᴛᴇʀꜱ
 » `/wolves`*:* ʟɪꜱᴛꜱ ᴀʟʟ ᴡᴏʟꜰ ᴅɪꜱᴀꜱᴛᴇʀꜱ
 » `/heroes`*:* ʟɪꜱᴛꜱ ᴀʟʟ ʜᴇʀᴏ ᴅɪꜱᴀꜱᴛᴇʀꜱ ᴍᴇᴍʙᴇʀꜱ
  *Ping:*
 » `/ping`*:* ɢᴇᴛꜱ ᴘɪɴɢ ᴛɪᴍᴇ ᴏꜰ ʙᴏᴛ ᴛᴏ ᴛᴇʟᴇɢʀᴀᴍ ꜱᴇʀᴠᴇʀ
 » `/pingall`*:* ɢᴇᴛꜱ ᴀʟʟ ʟɪꜱᴛᴇᴅ ᴘɪɴɢ ᴛɪᴍᴇꜱ
  *ʙʀᴏᴀᴅᴄᴀꜱᴛ: (ʙᴏᴛ ᴏᴡɴᴇʀ ᴏɴʟʏ)*
 »  *Note:* ᴛʜɪꜱ ꜱᴜᴘᴘᴏʀᴛꜱ ʙᴀꜱɪᴄ ᴍᴀʀᴋᴅᴏᴡɴ
 » `/broadcastall`*:* ʙʀᴏᴀᴅᴄᴀꜱᴛꜱ ᴇᴠᴇʀʏᴡʜᴇʀᴇ
 » `/broadcastusers`*:* ʙʀᴏᴀᴅᴄᴀꜱᴛꜱ ᴛᴏᴏ ᴀʟʟ ᴜꜱᴇʀꜱ
 » `/broadcastgroups`*:* ʙʀᴏᴀᴅᴄᴀꜱᴛꜱ ᴛᴏᴏ ᴀʟʟ ɢʀᴏᴜᴘꜱ
 *ɢʀᴏᴜᴘꜱ ɪɴꜰᴏ:*
 » `/groups`*:* ʟɪꜱᴛ ᴛʜᴇ ɢʀᴏᴜᴘꜱ ᴡɪᴛʜ ɴᴀᴍᴇ， ɪᴅ， ᴍᴇᴍʙᴇʀꜱ ᴄᴏᴜɴᴛ ᴀꜱ ᴀ ᴛｘᴛ
 » `/getchats`*:* ɢᴇᴛꜱ ᴀ ʟɪꜱᴛ ᴏꜰ ɢʀᴏᴜᴘ ɴᴀᴍᴇꜱ ᴛʜᴇ ᴜꜱᴇʀ ʜᴀꜱ ʙᴇᴇɴ ꜱᴇᴇɴ ɪɴ. ʙᴏᴛ ᴏᴡɴᴇʀ ᴏɴʟʏ
  *ʙʟᴀᴄᴋʟɪꜱᴛ:* 
 » `/ignore`*:* ʙʟᴀᴄᴋʟɪꜱᴛꜱ ᴀ ᴜꜱᴇʀ ꜰʀᴏᴍ ᴜꜱɪɴɢ ᴛʜᴇ ʙᴏᴛ ᴇɴᴛɪʀᴇʟʏ
 » `/notice`*:* ᴡʜɪᴛᴇʟɪꜱᴛꜱ ᴛʜᴇ ᴜꜱᴇʀ ᴛᴏ ᴀʟʟᴏᴡ ʙᴏᴛ ᴜꜱᴀɢᴇ
 *Module loading:*
 » `/listmodules`*:* ʟɪꜱᴛꜱ ɴᴀᴍᴇꜱ ᴏꜰ ᴀʟʟ ᴍᴏᴅᴜʟᴇꜱ
 » `/load` modulename*:* ʟᴏᴀᴅꜱ ᴛʜᴇ ꜱᴀɪᴅ ᴍᴏᴅᴜʟᴇ ᴛᴏ ᴍᴇᴍᴏʀʏ ᴡɪᴛʜᴏᴜᴛ ʀᴇꜱᴛᴀʀᴛɪɴɢ.
 » `/unload` modulename*:* ʟᴏᴀᴅꜱ ᴛʜᴇ ꜱᴀɪᴅ ᴍᴏᴅᴜʟᴇ ꜰʀᴏᴍ ᴍᴇᴍᴏʀʏ ᴡɪᴛʜᴏᴜᴛ ʀᴇꜱᴛᴀʀᴛɪɴɢ.ᴍᴇᴍᴏʀʏ ᴡɪᴛʜᴏᴜᴛ ʀᴇꜱᴛᴀʀᴛɪɴɢ ᴛʜᴇ ʙᴏᴛ 
 *Windows self hosted only:*
 » `/reboot`*:* ʀᴇꜱᴛᴀʀᴛꜱ ᴛʜᴇ ʙᴏᴛꜱ ꜱᴇʀᴠɪᴄᴇ
 » `/gitpull`*:* ᴘᴜʟʟꜱ ᴛʜᴇ ʀᴇᴘᴏ ᴀɴᴅ ᴛʜᴇɴ ʀᴇꜱᴛᴀʀᴛꜱ ᴛʜᴇ ʙᴏᴛꜱ ꜱᴇʀᴠɪᴄᴇ
 *ᴅᴇʙᴜɢɢɪɴɢ ᴀɴᴅ ꜱʜᴇʟʟ:* 
 » `/debug` <on/off>*:* ʟᴏɢꜱ ᴄᴏᴍᴍᴀɴᴅꜱ ᴛᴏ ᴜᴘᴅᴀᴛᴇꜱ.ᴛxᴛ
 » `/logs`*:* ʀᴜɴ ᴛʜɪꜱ ɪɴ ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ ᴛᴏ ɢᴇᴛ ʟᴏɢꜱ ɪɴ ᴘᴍ
 » `/eval`*:* ꜱᴇʟꜰ ᴇxᴘʟᴀɴᴀᴛᴏʀʏ
 » `/sh`*:* ꜱᴇʟꜰ ᴇxᴘʟᴀɴᴀᴛᴏʀʏ
 » `/py`*:* ꜱᴇʟꜰ ᴇxᴘʟᴀɴᴀᴛᴏʀʏ

"""

SUDO_HANDLER = CommandHandler(("addsudo", "adddragon"), addsudo)
SUPPORT_HANDLER = CommandHandler(("addsupport", "adddemon"), addsupport)
TIGER_HANDLER = CommandHandler(("addtiger"), addtiger)
WHITELIST_HANDLER = CommandHandler(("addwhitelist", "addwolf"), addwhitelist)
UNSUDO_HANDLER = CommandHandler(("removesudo", "removedragon"), removesudo)
UNSUPPORT_HANDLER = CommandHandler(("removesupport", "removedemon"),
                                   removesupport)
UNTIGER_HANDLER = CommandHandler(("removetiger"), removetiger)
UNWHITELIST_HANDLER = CommandHandler(("removewhitelist", "removewolf"),
                                     removewhitelist)

WHITELISTLIST_HANDLER = CommandHandler(["whitelistlist", "wolves"],
                                       whitelistlist)
TIGERLIST_HANDLER = CommandHandler(["tigers"], tigerlist)
SUPPORTLIST_HANDLER = CommandHandler(["supportlist", "demons"], supportlist)
SUDOLIST_HANDLER = CommandHandler(["sudolist", "dragons"], sudolist)
DEVLIST_HANDLER = CommandHandler(["devlist", "heroes"], devlist)

dispatcher.add_handler(SUDO_HANDLER)
dispatcher.add_handler(SUPPORT_HANDLER)
dispatcher.add_handler(TIGER_HANDLER)
dispatcher.add_handler(WHITELIST_HANDLER)
dispatcher.add_handler(UNSUDO_HANDLER)
dispatcher.add_handler(UNSUPPORT_HANDLER)
dispatcher.add_handler(UNTIGER_HANDLER)
dispatcher.add_handler(UNWHITELIST_HANDLER)

dispatcher.add_handler(WHITELISTLIST_HANDLER)
dispatcher.add_handler(TIGERLIST_HANDLER)
dispatcher.add_handler(SUPPORTLIST_HANDLER)
dispatcher.add_handler(SUDOLIST_HANDLER)
dispatcher.add_handler(DEVLIST_HANDLER)

__mod_name__ = "DISASTERS"
__handlers__ = [
    SUDO_HANDLER, SUPPORT_HANDLER, TIGER_HANDLER, WHITELIST_HANDLER,
    UNSUDO_HANDLER, UNSUPPORT_HANDLER, UNTIGER_HANDLER, UNWHITELIST_HANDLER,
    WHITELISTLIST_HANDLER, TIGERLIST_HANDLER, SUPPORTLIST_HANDLER,
    SUDOLIST_HANDLER, DEVLIST_HANDLER]
