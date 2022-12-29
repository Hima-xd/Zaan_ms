import html
from KRISTY.modules.disable import DisableAbleCommandHandler
from KRISTY import dispatcher, DRAGONS
from KRISTY.modules.helper_funcs.extraction import extract_user
from telegram.ext import CallbackContext, CallbackQueryHandler
import KRISTY.modules.sql.approve_sql as sql
from KRISTY.modules.helper_funcs.chat_status import user_admin
from KRISTY.modules.log_channel import loggable
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.utils.helpers import mention_html
from telegram.error import BadRequest


@loggable
@user_admin
def approve(update, context):
    message = update.effective_message
    chat_title = message.chat.title
    chat = update.effective_chat
    args = context.args
    user = update.effective_user
    user_id = extract_user(message, args)
    if not user_id:
        message.reply_text(
            "ɪ ᴅᴏɴ'ᴛ ᴋɴᴏᴡ ᴡʜᴏ ʏᴏᴜ'ʀᴇ ᴛᴀʟᴋɪɴɢ ᴀʙᴏᴜᴛ, ʏᴏᴜ'ʀᴇ ɢᴏɪɴɢ ᴛᴏ ɴᴇᴇᴅ ᴛᴏ ꜱᴘᴇᴄɪꜰʏ ᴀ ᴜꜱᴇʀ ʙᴀʙʏ🥀!",
        )
        return ""
    try:
        member = chat.get_member(user_id)
    except BadRequest:
        return ""
    if member.status in ("administrator", "creator"):
        message.reply_text(
            "ᴜꜱᴇʀ ɪꜱ ᴀʟʀᴇᴀᴅʏ ᴀᴅᴍɪɴ - ʟᴏᴄᴋꜱ, ʙʟᴏᴄᴋʟɪꜱᴛꜱ, ᴀɴᴅ ᴀɴᴛɪꜰʟᴏᴏᴅ ᴀʟʀᴇᴀᴅʏ ᴅᴏɴ'ᴛ ᴀᴘᴘʟʏ ᴛᴏ ᴛʜᴇᴍ ʙᴀʙʏ🥀.",
        )
        return ""
    if sql.is_approved(message.chat_id, user_id):
        message.reply_text(
            f"[{member.user['first_name']}](tg://user?id={member.user['id']}) ɪꜱ ᴀʟʀᴇᴀᴅʏ ᴀᴘᴘʀᴏᴠᴇᴅ ɪɴ {chat_title} ʙᴀʙʏ🥀",
            parse_mode=ParseMode.MARKDOWN,
        )
        return ""
    sql.approve(message.chat_id, user_id)
    message.reply_text(
        f"[{member.user['first_name']}](tg://user?id={member.user['id']}) ʜᴀꜱ ʙᴇᴇɴ ᴀᴘᴘʀᴏᴠᴇᴅ ɪɴ {chat_title} ʙᴀʙʏ🥀! ᴛʜᴇʏ ᴡɪʟʟ ɴᴏᴡ ʙᴇ ɪɢɴᴏʀᴇᴅ ʙʏ ᴀᴜᴛᴏᴍᴀᴛᴇᴅ ᴀᴅᴍɪɴ ᴀᴄᴛɪᴏɴꜱ ʟɪᴋᴇ ʟᴏᴄᴋꜱ, ʙʟᴏᴄᴋʟɪꜱᴛꜱ, ᴀɴᴅ ᴀɴᴛɪꜰʟᴏᴏᴅ ʙᴀʙʏ🥀.",
        parse_mode=ParseMode.MARKDOWN,
    )
    log_message = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#ᴀᴘᴘʀᴏᴠᴇᴅ\n"
        f"<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>ᴜꜱᴇʀ:</b> {mention_html(member.user.id, member.user.first_name)}"
    )

    return log_message


@loggable
@user_admin
def disapprove(update, context):
    message = update.effective_message
    chat_title = message.chat.title
    chat = update.effective_chat
    args = context.args
    user = update.effective_user
    user_id = extract_user(message, args)
    if not user_id:
        message.reply_text(
            "ɪ ᴅᴏɴ'ᴛ ᴋɴᴏᴡ ᴡʜᴏ ʏᴏᴜ'ʀᴇ ᴛᴀʟᴋɪɴɢ ᴀʙᴏᴜᴛ, ʏᴏᴜ'ʀᴇ ɢᴏɪɴɢ ᴛᴏ ɴᴇᴇᴅ ᴛᴏ ꜱᴘᴇᴄɪꜰʏ ᴀ ᴜꜱᴇʀ ʙᴀʙʏ🥀!",
        )
        return ""
    try:
        member = chat.get_member(user_id)
    except BadRequest:
        return ""
    if member.status in ("administrator", "creator"):
        message.reply_text("ᴛʜɪꜱ ᴜꜱᴇʀ ɪꜱ ᴀɴ ᴀᴅᴍɪɴ, ᴛʜᴇʏ ᴄᴀɴ'ᴛ ʙᴇ ᴜɴᴀᴘᴘʀᴏᴠᴇᴅ ʙᴀʙʏ🥀.")
        return ""
    if not sql.is_approved(message.chat_id, user_id):
        message.reply_text(f"{member.user['first_name']} ɪꜱɴ'ᴛ ᴀᴘᴘʀᴏᴠᴇᴅ ʏᴇᴛ ʙᴀʙʏ🥀!")
        return ""
    sql.disapprove(message.chat_id, user_id)
    message.reply_text(
        f"{member.user['first_name']} ɪꜱ ɴᴏ ʟᴏɴɢᴇʀ ᴀᴘᴘʀᴏᴠᴇᴅ ɪɴ {chat_title} ʙᴀʙʏ🥀.",
    )
    log_message = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#ᴜɴᴀᴘᴘʀᴏᴠᴇᴅ\n"
        f"<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>ᴜꜱᴇʀ:</b> {mention_html(member.user.id, member.user.first_name)}"
    )

    return log_message


@user_admin
def approved(update, context):
    message = update.effective_message
    chat_title = message.chat.title
    chat = update.effective_chat
    msg = "ᴛʜᴇ ꜰᴏʟʟᴏᴡɪɴɢ ᴜꜱᴇʀꜱ ᴀʀᴇ ᴀᴘᴘʀᴏᴠᴇᴅ ʙᴀʙʏ🥀.\n"
    approved_users = sql.list_approved(message.chat_id)
    for i in approved_users:
        member = chat.get_member(int(i.user_id))
        msg += f"- `{i.user_id}`: {member.user['first_name']}\n"
    if msg.endswith("approved.\n"):
        message.reply_text(f"ɴᴏ ᴜꜱᴇʀꜱ ᴀʀᴇ ᴀᴘᴘʀᴏᴠᴇᴅ ɪɴ {chat_title} ʙᴀʙʏ🥀.")
        return ""
    message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)


@user_admin
def approval(update, context):
    message = update.effective_message
    chat = update.effective_chat
    args = context.args
    user_id = extract_user(message, args)
    member = chat.get_member(int(user_id))
    if not user_id:
        message.reply_text(
            "ɪ ᴅᴏɴ'ᴛ ᴋɴᴏᴡ ᴡʜᴏ ʏᴏᴜ'ʀᴇ ᴛᴀʟᴋɪɴɢ ᴀʙᴏᴜᴛ, ʏᴏᴜ'ʀᴇ ɢᴏɪɴɢ ᴛᴏ ɴᴇᴇᴅ ᴛᴏ ꜱᴘᴇᴄɪꜰʏ ᴀ ᴜꜱᴇʀ ʙᴀʙʏ🥀!",
        )
        return ""
    if sql.is_approved(message.chat_id, user_id):
        message.reply_text(
            f"{member.user['first_name']} ɪꜱ ᴀɴ ᴀᴘᴘʀᴏᴠᴇᴅ ᴜꜱᴇʀ. ʟᴏᴄᴋꜱ, ᴀɴᴛɪꜰʟᴏᴏᴅ, ᴀɴᴅ ʙʟᴏᴄᴋʟɪꜱᴛꜱ ᴡᴏɴ'ᴛ ᴀᴘᴘʟʏ ᴛᴏ ᴛʜᴇᴍ ʙᴀʙʏ🥀.",
        )
    else:
        message.reply_text(
            f"{member.user['first_name']} ɪꜱ ɴᴏᴛ ᴀɴ ᴀᴘᴘʀᴏᴠᴇᴅ ᴜꜱᴇʀ. ᴛʜᴇʏ ᴀʀᴇ ᴀꜰꜰᴇᴄᴛᴇᴅ ʙʏ ɴᴏʀᴍᴀʟ ᴄᴏᴍᴍᴀɴᴅꜱ ʙᴀʙʏ🥀.",
        )


def unapproveall(update: Update, context: CallbackContext):
    chat = update.effective_chat
    user = update.effective_user
    member = chat.get_member(user.id)
    if member.status != "creator" and user.id not in DRAGONS:
        update.effective_message.reply_text(
            "ᴏɴʟʏ ᴛʜᴇ ᴄʜᴀᴛ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜɴᴀᴘᴘʀᴏᴠᴇ ᴀʟʟ ᴜꜱᴇʀꜱ ᴀᴛ ᴏɴᴄᴇ ʙᴀʙʏ🥀.",
        )
    else:
        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Unapprove all users",
                        callback_data="unapproveall_user",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="Cancel",
                        callback_data="unapproveall_cancel",
                    ),
                ],
            ],
        )
        update.effective_message.reply_text(
            f"ᴀʀᴇ ʏᴏᴜ ꜱᴜʀᴇ ʏᴏᴜ ᴡᴏᴜʟᴅ ʟɪᴋᴇ ᴛᴏ ᴜɴᴀᴘᴘʀᴏᴠᴇ ᴀʟʟ ᴜꜱᴇʀꜱ ɪɴ {chat.title}? ᴛʜɪꜱ ᴀᴄᴛɪᴏɴ ᴄᴀɴɴᴏᴛ ʙᴇ ᴜɴᴅᴏɴᴇ ʙᴀʙʏ🥀.",
            reply_markup=buttons,
            parse_mode=ParseMode.MARKDOWN,
        )


def unapproveall_btn(update: Update, context: CallbackContext):
    query = update.callback_query
    chat = update.effective_chat
    message = update.effective_message
    member = chat.get_member(query.from_user.id)
    if query.data == "unapproveall_user":
        if member.status == "creator" or query.from_user.id in DRAGONS:
            approved_users = sql.list_approved(chat.id)
            users = [int(i.user_id) for i in approved_users]
            for user_id in users:
                sql.disapprove(chat.id, user_id)
            message.edit_text("ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴜɴᴀᴘᴘʀᴏᴠᴇᴅ ᴀʟʟ ᴜꜱᴇʀ ɪɴ ᴛʜɪꜱ ᴄʜᴀᴛ ʙᴀʙʏ🥀.")
            return

        if member.status == "administrator":
            query.answer("ᴏɴʟʏ ᴏᴡɴᴇʀ ᴏꜰ ᴛʜᴇ ᴄʜᴀᴛ ᴄᴀɴ ᴅᴏ ᴛʜɪꜱ ʙᴀʙʏ🥀.")

        if member.status == "member":
            query.answer("ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʙᴇ ᴀᴅᴍɪɴ ᴛᴏ ᴅᴏ ᴛʜɪꜱ ʙᴀʙʏ🥀.")
    elif query.data == "unapproveall_cancel":
        if member.status == "creator" or query.from_user.id in DRAGONS:
            message.edit_text("ʀᴇᴍᴏᴠɪɴɢ ᴏꜰ ᴀʟʟ ᴀᴘᴘʀᴏᴠᴇᴅ ᴜꜱᴇʀꜱ ʜᴀꜱ ʙᴇᴇɴ ᴄᴀɴᴄᴇʟʟᴇᴅ ʙᴀʙʏ🥀.")
            return ""
        if member.status == "administrator":
            query.answer("ᴏɴʟʏ ᴏᴡɴᴇʀ ᴏꜰ ᴛʜᴇ ᴄʜᴀᴛ ᴄᴀɴ ᴅᴏ ᴛʜɪꜱ ʙᴀʙʏ🥀.")
        if member.status == "member":
            query.answer("ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʙᴇ ᴀᴅᴍɪɴ ᴛᴏ ᴅᴏ ᴛʜɪꜱ ʙᴀʙʏ🥀.")


__help__ = """
ꜱᴏᴍᴇᴛɪᴍᴇꜱ, ʏᴏᴜ ᴍɪɢʜᴛ ᴛʀᴜꜱᴛ ᴀ ᴜꜱᴇʀ ɴᴏᴛ ᴛᴏ ꜱᴇɴᴅ ᴜɴᴡᴀɴᴛᴇᴅ ᴄᴏɴᴛᴇɴᴛ.
ᴍᴀʏʙᴇ ɴᴏᴛ ᴇɴᴏᴜɢʜ ᴛᴏ ᴍᴀᴋᴇ ᴛʜᴇᴍ ᴀᴅᴍɪɴ, ʙᴜᴛ ʏᴏᴜ ᴍɪɢʜᴛ ʙᴇ ᴏᴋ ᴡɪᴛʜ ʟᴏᴄᴋꜱ, ʙʟᴀᴄᴋʟɪꜱᴛꜱ, ᴀɴᴅ ᴀɴᴛɪꜰʟᴏᴏᴅ ɴᴏᴛ ᴀᴘᴘʟʏɪɴɢ ᴛᴏ ᴛʜᴇᴍ.

ᴛʜᴀᴛ'ꜱ ᴡʜᴀᴛ ᴀᴘᴘʀᴏᴠᴀʟꜱ ᴀʀᴇ ꜰᴏʀ - ᴀᴘᴘʀᴏᴠᴇ ᴏꜰ ᴛʀᴜꜱᴛᴡᴏʀᴛʜʏ ᴜꜱᴇʀꜱ ᴛᴏ ᴀʟʟᴏᴡ ᴛʜᴇᴍ ᴛᴏ ꜱᴇɴᴅ
*Admin commands:*
» `/approval`*:* ᴄʜᴇᴄᴋ ᴀ ᴜꜱᴇʀ'ꜱ ᴀᴘᴘʀᴏᴠᴀʟ ꜱᴛᴀᴛᴜꜱ ɪɴ ᴛʜɪꜱ ᴄʜᴀᴛ.
» `/approve`*:* ᴀᴘᴘʀᴏᴠᴇ ᴏꜰ ᴀ ᴜꜱᴇʀ. ʟᴏᴄᴋꜱ, ʙʟᴀᴄᴋʟɪꜱᴛꜱ, ᴀɴᴅ ᴀɴᴛɪꜰʟᴏᴏᴅ ᴡᴏɴ'ᴛ ᴀᴘᴘʟʏ ᴛᴏ ᴛʜᴇᴍ ᴀɴʏᴍᴏʀᴇ.
» `/unapprove`*:* ᴜɴᴀᴘᴘʀᴏᴠᴇ ᴏꜰ ᴀ ᴜꜱᴇʀ. ᴛʜᴇʏ ᴡɪʟʟ ɴᴏᴡ ʙᴇ ꜱᴜʙᴊᴇᴄᴛ ᴛᴏ ʟᴏᴄᴋꜱ, ʙʟᴀᴄᴋʟɪꜱᴛꜱ, ᴀɴᴅ ᴀɴᴛɪꜰʟᴏᴏᴅ ᴀɢᴀɪɴ.
» `/approved`*:* ʟɪꜱᴛ ᴀʟʟ ᴀᴘᴘʀᴏᴠᴇᴅ ᴜꜱᴇʀꜱ.
» `/unapproveall`*:* ᴜɴᴀᴘᴘʀᴏᴠᴇ *ᴀʟʟ* ᴜꜱᴇʀꜱ ɪɴ ᴀ ᴄʜᴀᴛ. ᴛʜɪꜱ ᴄᴀɴɴᴏᴛ ʙᴇ ᴜɴᴅᴏɴᴇ.
"""

APPROVE = DisableAbleCommandHandler("approve", approve, run_async=True)
DISAPPROVE = DisableAbleCommandHandler("unapprove", disapprove, run_async=True)
APPROVED = DisableAbleCommandHandler("approved", approved, run_async=True)
APPROVAL = DisableAbleCommandHandler("approval", approval, run_async=True)
UNAPPROVEALL = DisableAbleCommandHandler("unapproveall", unapproveall, run_async=True)
UNAPPROVEALL_BTN = CallbackQueryHandler(
    unapproveall_btn, pattern=r"unapproveall_.*", run_async=True
)

dispatcher.add_handler(APPROVE)
dispatcher.add_handler(DISAPPROVE)
dispatcher.add_handler(APPROVED)
dispatcher.add_handler(APPROVAL)
dispatcher.add_handler(UNAPPROVEALL)
dispatcher.add_handler(UNAPPROVEALL_BTN)

__mod_name__ = "APPROVALS"
__command_list__ = ["approve", "unapprove", "approved", "approval"]
__handlers__ = [APPROVE, DISAPPROVE, APPROVED, APPROVAL]
