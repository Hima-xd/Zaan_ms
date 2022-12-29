import html

from KRISTY import LOGGER, DRAGONS, TIGERS, WOLVES, dispatcher
from KRISTY.modules.helper_funcs.chat_status import user_admin, user_not_admin
from KRISTY.modules.log_channel import loggable
from KRISTY.modules.sql import reporting_sql as sql
from telegram import Chat, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.error import BadRequest, Unauthorized
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
    run_async,
)
from telegram.utils.helpers import mention_html

REPORT_GROUP = 12
REPORT_IMMUNE_USERS = DRAGONS + TIGERS + WOLVES



@user_admin
def report_setting(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    chat = update.effective_chat
    msg = update.effective_message

    if chat.type == chat.PRIVATE:
        if len(args) >= 1:
            if args[0] in ("yes", "on"):
                sql.set_user_setting(chat.id, True)
                msg.reply_text(
                    "ᴛᴜʀɴᴇᴅ ᴏɴ ʀᴇᴘᴏʀᴛɪɴɢ! ʏᴏᴜ'ʟʟ ʙᴇ ɴᴏᴛɪꜰɪᴇᴅ ᴡʜᴇɴᴇᴠᴇʀ ᴀɴʏᴏɴᴇ ʀᴇᴘᴏʀᴛꜱ ꜱᴏᴍᴇᴛʜɪɴɢ ʙᴀʙʏ🥀.",
                )

            elif args[0] in ("no", "off"):
                sql.set_user_setting(chat.id, False)
                msg.reply_text("ᴛᴜʀɴᴇᴅ ᴏꜰꜰ ʀᴇᴘᴏʀᴛɪɴɢ! ʏᴏᴜ ᴡᴏɴᴛ ɢᴇᴛ ᴀɴʏ ʀᴇᴘᴏʀᴛꜱ ʙᴀʙʏ🥀.")
        else:
            msg.reply_text(
                f"ʏᴏᴜʀ ᴄᴜʀʀᴇɴᴛ ʀᴇᴘᴏʀᴛ ᴘʀᴇꜰᴇʀᴇɴᴄᴇ ɪꜱ: `{sql.user_should_report(chat.id)}` ʙᴀʙʏ🥀",
                parse_mode=ParseMode.MARKDOWN,
            )

    elif len(args) >= 1:
        if args[0] in ("yes", "on"):
            sql.set_chat_setting(chat.id, True)
            msg.reply_text(
                "ᴛᴜʀɴᴇᴅ ᴏɴ ʀᴇᴘᴏʀᴛɪɴɢ! ᴀᴅᴍɪɴꜱ ᴡʜᴏ ʜᴀᴠᴇ ᴛᴜʀɴᴇᴅ ᴏɴ ʀᴇᴘᴏʀᴛꜱ ᴡɪʟʟ ʙᴇ ɴᴏᴛɪꜰɪᴇᴅ ᴡʜᴇɴ /report "
                "ᴏʀ @admin ɪꜱ ᴄᴀʟʟᴇᴅ ʙᴀʙʏ🥀.",
            )

        elif args[0] in ("no", "off"):
            sql.set_chat_setting(chat.id, False)
            msg.reply_text(
                "ᴛᴜʀɴᴇᴅ ᴏꜰꜰ ʀᴇᴘᴏʀᴛɪɴɢ! ɴᴏ ᴀᴅᴍɪɴꜱ ᴡɪʟʟ ʙᴇ ɴᴏᴛɪꜰɪᴇᴅ ᴏɴ /report ᴏʀ @admin ʙᴀʙʏ🥀.",
            )
    else:
        msg.reply_text(
            f"ᴛʜɪꜱ ɢʀᴏᴜᴘ'ꜱ ᴄᴜʀʀᴇɴᴛ ꜱᴇᴛᴛɪɴɢ ɪꜱ: `{sql.chat_should_report(chat.id)}` ʙᴀʙʏ🥀",
            parse_mode=ParseMode.MARKDOWN,
        )



@user_not_admin
@loggable
def report(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    args = context.args
    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    if chat and message.reply_to_message and sql.chat_should_report(chat.id):
        reported_user = message.reply_to_message.from_user
        chat_name = chat.title or chat.first or chat.username
        admin_list = chat.get_administrators()
        message = update.effective_message

        if user.id == reported_user.id:
            message.reply_text("ᴜʜ ʏᴇᴀʜ, ꜱᴜʀᴇ ꜱᴜʀᴇ...ᴍᴀꜱᴏ ᴍᴜᴄʜ?")
            return

        elif user.id == bot.id:
            message.reply_text("ɴɪᴄᴇ ᴛʀʏ ʙᴀʙʏ🥀.")
            return

        elif reported_user.id in REPORT_IMMUNE_USERS:
            message.reply_text("ᴜʜ? ʏᴏᴜ ʀᴇᴘᴏʀᴛɪɴɢ ᴀ ᴅɪꜱᴀꜱᴛᴇʀ ʙᴀʙʏ🥀")
            return

        else:pass

        if chat.username and chat.type == Chat.SUPERGROUP:

            reported = f"{mention_html(user.id, user.first_name)} ʀᴇᴘᴏʀᴛᴇᴅ {mention_html(reported_user.id, reported_user.first_name)} ᴛᴏ ᴛʜᴇ ᴀᴅᴍɪɴ ʙᴀʙʏ🥀!"

            msg = (
                f"<b>⚠️ ʀᴇᴘᴏʀᴛ: </b>{html.escape(chat.title)}\n"
                f"<b> ❍ ʀᴇᴘᴏʀᴛᴇᴅ ʙʏ:</b> {mention_html(user.id, user.first_name)}(<code>{user.id}</code>)\n"
                f"<b> ❍ ʀᴇᴘᴏʀᴛᴇᴅ ᴜꜱᴇʀ:</b> {mention_html(reported_user.id, reported_user.first_name)} (<code>{reported_user.id}</code>)\n"
            )
            link = f'<b> ❍ ʀᴇᴘᴏʀᴛᴇᴅ ᴍᴇꜱꜱᴀɢᴇ:</b> <a href="https://t.me/{chat.username}/{message.reply_to_message.message_id}">ᴄʟɪᴄᴋ ʜᴇʀᴇ</a>'
            should_forward = False
            keyboard = [
                [
                    InlineKeyboardButton(
                        "➡ ᴍᴇꜱꜱᴀɢᴇ",
                        url=f"https://t.me/{chat.username}/{message.reply_to_message.message_id}",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        " ᴋɪᴄᴋ ",
                        callback_data=f"report_{chat.id}=kick={reported_user.id}={reported_user.first_name}",
                    ),
                    InlineKeyboardButton(
                        " ʙᴀɴ",
                        callback_data=f"report_{chat.id}=banned={reported_user.id}={reported_user.first_name}",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        " ᴅᴇʟᴇᴛᴇ ᴍᴀꜱꜱᴀɢᴇ",
                        callback_data=f"report_{chat.id}=delete={reported_user.id}={message.reply_to_message.message_id}",
                    ),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
        else:
            reported = (
                f"{mention_html(user.id, user.first_name)} ʀᴇᴘᴏʀᴛᴇᴅ "
                f"{mention_html(reported_user.id, reported_user.first_name)} ᴛᴏ ᴛʜᴇ ᴀᴅᴍɪɴꜱ! ʙᴀʙʏ🥀"
            )

            msg = f'{mention_html(user.id, user.first_name)} ɪꜱ ᴄᴀʟʟɪɴɢ ꜰᴏʀ ᴀᴅᴍɪɴꜱ ɪɴ "{html.escape(chat_name)}" ʙᴀʙʏ🥀!'
            link = ""
            should_forward = True

        for admin in admin_list:
            if admin.user.is_bot:  # can't message bots
                continue

            if sql.user_should_report(admin.user.id):
                try:
                    if chat.type != Chat.SUPERGROUP:
                        bot.send_message(
                            admin.user.id, msg + link, parse_mode=ParseMode.HTML,
                        )

                        if should_forward:
                            message.reply_to_message.forward(admin.user.id)

                            if (
                                len(message.text.split()) > 1
                            ):  # If user is giving a reason, send his message too
                                message.forward(admin.user.id)
                    if not chat.username:
                        bot.send_message(
                            admin.user.id, msg + link, parse_mode=ParseMode.HTML,
                        )

                        if should_forward:
                            message.reply_to_message.forward(admin.user.id)

                            if (
                                len(message.text.split()) > 1
                            ):  # If user is giving a reason, send his message too
                                message.forward(admin.user.id)

                    if chat.username and chat.type == Chat.SUPERGROUP:
                        bot.send_message(
                            admin.user.id,
                            msg + link,
                            parse_mode=ParseMode.HTML,
                            reply_markup=reply_markup,
                        )

                        if should_forward:
                            message.reply_to_message.forward(admin.user.id)

                            if (
                                len(message.text.split()) > 1
                            ):  # If user is giving a reason, send his message too
                                message.forward(admin.user.id)

                except Unauthorized:
                    pass
                except BadRequest as excp:  # TODO: cleanup exceptions
                    LOGGER.exception("Exception while reporting user")

        message.reply_to_message.reply_text(
            f"{mention_html(user.id, user.first_name)} ʀᴇᴘᴏʀᴛᴇᴅ ᴛʜᴇ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ᴛʜᴇ ᴀᴅᴍɪɴꜱ ʙᴀʙʏ🥀.",
            parse_mode=ParseMode.HTML,
        )
        return msg

    return ""


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)


def __chat_settings__(chat_id, _):
    return f"ᴛʜɪꜱ ᴄʜᴀᴛ ɪꜱ ꜱᴇᴛᴜᴘ ᴛᴏ ꜱᴇɴᴅ ᴜꜱᴇʀ ʀᴇᴘᴏʀᴛꜱ ᴛᴏ ᴀᴅᴍɪɴꜱ, ᴠɪᴀ /report ᴏʀ @admin: `{sql.chat_should_report(chat_id)}` ʙᴀʙʏ🥀"


def __user_settings__(user_id):
    return (
        "ʏᴏᴜ ᴡɪʟʟ ʀᴇᴄᴇɪᴠᴇ ʀᴇᴘᴏʀᴛꜱ ꜰʀᴏᴍ ᴄʜᴀᴛꜱ ʏᴏᴜ'ʀᴇ ᴀᴅᴍɪɴ ʙᴀʙʏ🥀."
        if sql.user_should_report(user_id) is True
        else "ʏᴏᴜ ᴡɪʟʟ *ɴᴏᴛ* ʀᴇᴄᴇɪᴠᴇ ʀᴇᴘᴏʀᴛꜱ ꜰʀᴏᴍ ᴄʜᴀᴛꜱ ʏᴏᴜ'ʀᴇ ᴀᴅᴍɪɴ ʙᴀʙʏ🥀."
    )


def buttons(update: Update, context: CallbackContext):
    bot = context.bot
    query = update.callback_query
    splitter = query.data.replace("report_", "").split("=")
    if splitter[1] == "kick":
        try:
            bot.kickChatMember(splitter[0], splitter[2])
            bot.unbanChatMember(splitter[0], splitter[2])
            query.answer("ꜱᴜᴄᴄᴇꜱꜰᴜʟʟʏ ᴋɪᴄᴋᴇᴅ ʙᴀʙʏ🥀")
            return ""
        except Exception as err:
            query.answer(" ꜰᴀɪʟᴇᴅ ᴛᴏ ᴋɪᴄᴋ ʙᴀʙʏ🥀")
            bot.sendMessage(
                text=f"Error: {err}",
                chat_id=query.message.chat_id,
                parse_mode=ParseMode.HTML,
            )
    elif splitter[1] == "banned":
        try:
            bot.kickChatMember(splitter[0], splitter[2])
            query.answer(" ꜱᴜᴄᴄᴇꜱꜰᴜʟʟʏ ʙᴀɴɴᴇᴅ ʙᴀʙʏ🥀")
            return ""
        except Exception as err:
            bot.sendMessage(
                text=f"Error: {err}",
                chat_id=query.message.chat_id,
                parse_mode=ParseMode.HTML,
            )
            query.answer(" ꜰᴀɪʟᴇᴅ ᴛᴏ ʙᴀɴ ʙᴀʙʏ🥀")
    elif splitter[1] == "delete":
        try:
            bot.deleteMessage(splitter[0], splitter[3])
            query.answer("ᴍᴇꜱꜱᴀɢᴇ ᴅᴇʟᴇᴛᴇᴅ ʙᴀʙʏ🥀")
            return ""
        except Exception as err:
            bot.sendMessage(
                text=f"Error: {err}",
                chat_id=query.message.chat_id,
                parse_mode=ParseMode.HTML,
            )
            query.answer("ꜰᴀɪʟᴇᴅ ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴍᴇꜱꜱᴀɢᴇ ʙᴀʙʏ🥀!")


__help__ = """
  » `/report <reason>`*:* ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ʀᴇᴘᴏʀᴛ ɪᴛ ᴛᴏ ᴀᴅᴍɪɴꜱ.
 » `@admins`*:* ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ʀᴇᴘᴏʀᴛ ɪᴛ ᴛᴏ ᴀᴅᴍɪɴꜱ.
*ɴᴏᴛᴇ:* ɴᴇɪᴛʜᴇʀ ᴏꜰ ᴛʜᴇꜱᴇ ᴡɪʟʟ ɢᴇᴛ ᴛʀɪɢɢᴇʀᴇᴅ ɪꜰ ᴜꜱᴇᴅ ʙʏ ᴀᴅᴍɪɴꜱ.

*Admins only:*
  » `/reports` <on/off>*:* ᴄʜᴀɴɢᴇ ʀᴇᴘᴏʀᴛ ꜱᴇᴛᴛɪɴɢ, ᴏʀ ᴠɪᴇᴡ ᴄᴜʀʀᴇɴᴛ ꜱᴛᴀᴛᴜꜱ.
   » ɪꜰ ᴅᴏɴᴇ ɪɴ ᴘᴍ, ᴛᴏɢɢʟᴇꜱ ʏᴏᴜʀ ꜱᴛᴀᴛᴜꜱ..
   » ɪꜰ ɪɴ ɢʀᴏᴜᴘ, ᴛᴏɢɢʟᴇꜱ ᴛʜᴀᴛ ɢʀᴏᴜᴘꜱ'ꜱ ꜱᴛᴀᴛᴜꜱ.
"""

SETTING_HANDLER = CommandHandler("reports", report_setting, run_async=True)
REPORT_HANDLER = CommandHandler("report", report, filters=Filters.chat_type.groups, run_async=True)
ADMIN_REPORT_HANDLER = MessageHandler(Filters.regex(r"(?i)@admins(s)?"), report, run_async=True)
REPORT_BUTTON_USER_HANDLER = CallbackQueryHandler(buttons, pattern=r"report_")
REPORT_HANDLER2 = MessageHandler(Filters.regex(r"(?i)@lomda(s)?"), report, run_async=True)

dispatcher.add_handler(REPORT_BUTTON_USER_HANDLER)
dispatcher.add_handler(SETTING_HANDLER)
dispatcher.add_handler(REPORT_HANDLER, REPORT_GROUP)
dispatcher.add_handler(ADMIN_REPORT_HANDLER, REPORT_GROUP)
dispatcher.add_handler(REPORT_HANDLER2, REPORT_GROUP)

__mod_name__ = "REPORTING"
__handlers__ = [
    (REPORT_HANDLER, REPORT_GROUP),
    (ADMIN_REPORT_HANDLER, REPORT_GROUP),
    (SETTING_HANDLER),
]
