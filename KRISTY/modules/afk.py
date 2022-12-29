
import random, html

from KRISTY import dispatcher
from KRISTY.modules.disable import (
    DisableAbleCommandHandler,
    DisableAbleMessageHandler,
)
from KRISTY.modules.sql import afk_sql as sql
from KRISTY.modules.users import get_user_id
from telegram import MessageEntity, Update
from telegram.error import BadRequest
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
    run_async,
)

AFK_GROUP = 7
AFK_REPLY_GROUP = 8


def afk(update: Update, context: CallbackContext):
    args = update.effective_message.text.split(None, 1)
    user = update.effective_user

    if not user:  # ignore channels
        return

    if user.id in [777000, 1087968824]:
        return

    notice = ""
    if len(args) >= 2:
        reason = args[1]
        if len(reason) > 150:
            reason = reason[:150]
            notice = "\nʏᴏᴜʀ ᴀꜰᴋ ʀᴇᴀꜱᴏɴ ᴡᴀꜱ ꜱʜᴏʀᴛᴇɴᴇᴅ ᴛᴏ 150 ᴄʜᴀʀᴀᴄᴛᴇʀꜱ ʙᴀʙʏ🥀."
    else:
        reason = ""

    
    fname = update.effective_user.first_name
    try:
        update.effective_message.reply_text("{} ɪꜱ ɴᴏᴡ ᴀᴡᴀʏ ʙᴀʙʏ🥀!{}".format(fname, notice))
    except BadRequest:
        pass
    sql.set_afk(update.effective_user.id, reason)


def no_longer_afk(update: Update, context: CallbackContext):
    user = update.effective_user
    message = update.effective_message

    if not user:  # ignore channels
        return

    res = sql.rm_afk(user.id)
    if res:
        if message.new_chat_members:  # dont say msg
            return
        firstname = update.effective_user.first_name
        try:
            options = [

                "{} ɪꜱ ʜᴇʀᴇ ʙᴀʙʏ🥀!",
                "{} ɪꜱ ʙᴀᴄᴋ ʙᴀʙʏ🥀!",
                "{} ɪꜱ ɴᴏᴡ ɪɴ ᴛʜᴇ ᴄʜᴀᴛ ʙᴀʙʏ🥀!",
                "{} ɪꜱ ᴀᴡᴀᴋᴇ ʙᴀʙʏ🥀!",
                "{} ɪꜱ ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ʙᴀʙʏ🥀!",
                "{} ɪꜱ ꜰɪɴᴀʟʟʏ ʜᴇʀᴇ ʙᴀʙʏ🥀!",
                "ᴡᴇʟᴄᴏᴍᴇ ʙᴀᴄᴋ ʙᴀʙʏ🥀! {}",
                "ᴡʜᴇʀᴇ ɪꜱ {}?\nɪɴ ᴛʜᴇ ᴄʜᴀᴛ ʙᴀʙʏ🥀!",
            ]
            chosen_option = random.choice(options)
            update.effective_message.reply_text(chosen_option.format(firstname))
        except:
            return


def reply_afk(update: Update, context: CallbackContext):
    bot = context.bot
    message = update.effective_message
    userc = update.effective_user
    userc_id = userc.id
    if message.entities and message.parse_entities(
        [MessageEntity.TEXT_MENTION, MessageEntity.MENTION]
    ):
        entities = message.parse_entities(
            [MessageEntity.TEXT_MENTION, MessageEntity.MENTION]
        )

        chk_users = []
        for ent in entities:
            if ent.type == MessageEntity.TEXT_MENTION:
                user_id = ent.user.id
                fst_name = ent.user.first_name

                if user_id in chk_users:
                    return
                chk_users.append(user_id)

            if ent.type != MessageEntity.MENTION:
                return

            user_id = get_user_id(message.text[ent.offset : ent.offset + ent.length])
            if not user_id:
                # Should never happen, since for a user to become AFK they must have spoken. Maybe changed username?
                return

            if user_id in chk_users:
                return
            chk_users.append(user_id)

            try:
                chat = bot.get_chat(user_id)
            except BadRequest:
                print("ᴇʀʀᴏʀ: ᴄᴏᴜʟᴅ ɴᴏᴛ ꜰᴇᴛᴄʜ ᴜꜱᴇʀɪᴅ {} ꜰᴏʀ ᴀꜰᴋ ᴍᴏᴅᴜʟᴇ ʙᴀʙʏ🥀".format(user_id))
                return
            fst_name = chat.first_name

            check_afk(update, context, user_id, fst_name, userc_id)

    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        fst_name = message.reply_to_message.from_user.first_name
        check_afk(update, context, user_id, fst_name, userc_id)


def check_afk(update, context, user_id, fst_name, userc_id):
    if sql.is_afk(user_id):
        user = sql.check_afk_status(user_id)
        if int(userc_id) == int(user_id):
            return
        if not user.reason:
            res = "{} ɪꜱ ᴀꜰᴋ ʙᴀʙʏ🥀".format(fst_name)
            update.effective_message.reply_text(res)
        else:
            res = "{} ɪꜱ ᴀꜰᴋ.\nʀᴇᴀꜱᴏɴ: <code>{}</code> ʙᴀʙʏ🥀".format(
                html.escape(fst_name), html.escape(user.reason)
            )
            update.effective_message.reply_text(res, parse_mode="html")


AFK_HANDLER = DisableAbleCommandHandler("afk", afk, run_async=True)
AFK_REGEX_HANDLER = DisableAbleMessageHandler(
    Filters.regex(r"^(?i)brb(.*)$"), afk, friendly="afk", run_async=True
)
NO_AFK_HANDLER = MessageHandler(Filters.all & Filters.chat_type.groups, no_longer_afk)
AFK_REPLY_HANDLER = MessageHandler(Filters.all & Filters.chat_type.groups, reply_afk)

dispatcher.add_handler(AFK_HANDLER, AFK_GROUP)
dispatcher.add_handler(AFK_REGEX_HANDLER, AFK_GROUP)
dispatcher.add_handler(NO_AFK_HANDLER, AFK_GROUP)
dispatcher.add_handler(AFK_REPLY_HANDLER, AFK_REPLY_GROUP)

__help__ = """
 » `/afk` <text> :  ɢɪᴠᴇꜱ ᴀᴜᴛᴏ ʀᴇᴘʟʏ ᴡʜᴇɴ ʏᴏᴜ ᴀʀᴇ ᴏꜰꜰʟɪɴᴇ
 » `brb` <text> :   ɢɪᴠᴇꜱ ᴀᴜᴛᴏ ʀᴇᴘʟʏ ᴡʜᴇɴ ʏᴏᴜ ᴀʀᴇ ᴏꜰꜰʟɪɴᴇ
 """
__mod_name__ = "AFK-ᴏꜰꜰʟɪɴᴇ"
__command_list__ = ["afk"]
__handlers__ = [
    (AFK_HANDLER, AFK_GROUP),
    (AFK_REGEX_HANDLER, AFK_GROUP),
    (NO_AFK_HANDLER, AFK_GROUP),
    (AFK_REPLY_HANDLER, AFK_REPLY_GROUP),
]
