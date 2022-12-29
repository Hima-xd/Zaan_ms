from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, Filters
from telegram.utils.helpers import mention_markdown, escape_markdown

from KRISTY import dispatcher
from KRISTY.modules.disable import DisableAbleCommandHandler
from KRISTY.modules.helper_funcs.chat_status import user_admin, user_admin_no_reply


@user_admin
def start_attendance(update, context):
    if ('flag' in context.chat_data) and (context.chat_data['flag'] == 1):
        update.message.reply_text(
            "ᴘʟᴇᴀꜱᴇ ᴄʟᴏꜱᴇ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴀᴛᴛᴇɴᴅᴀɴᴄᴇ ꜰɪʀꜱᴛ ʙᴀʙʏ🥀",
        )
    elif ('flag' not in context.chat_data) or (context.chat_data['flag'] == 0):
        context.chat_data['flag'] = 1
        context.chat_data['attendees'] = {}
        context.chat_data['id'] = update.effective_chat.id
        keyboard = [
            [
                InlineKeyboardButton(
                    "Present",
                    callback_data='present',
                ),
            ],
            [
                InlineKeyboardButton(
                    "End Attendance (Admin only)",
                    callback_data='end_attendance',
                ),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.chat_data['message'] = update.message.reply_text(
            "ᴘʟᴇᴀꜱᴇ ᴍᴀʀᴋ ʏᴏᴜʀ ᴀᴛᴛᴇɴᴅᴀɴᴄᴇ ʙᴀʙʏ🥀", reply_markup=reply_markup,
        )


def mark_attendance(update, context):
    query = update.callback_query
    if (
        str(update.effective_user.id) not in
        context.chat_data['attendees'].keys()
    ):
        context.chat_data['attendees'][
                update.effective_user.id
        ] = f'{escape_markdown(update.effective_user.full_name)}'
        context.bot.answer_callback_query(
            callback_query_id=query.id,
            text="ʏᴏᴜʀ ᴀᴛᴛᴇɴᴅᴀɴᴄᴇ ʜᴀꜱ ʙᴇᴇɴ ᴍᴀʀᴋᴇᴅ ʙᴀʙʏ🥀",
            show_alert=True,
        )
    else:
        context.bot.answer_callback_query(
            callback_query_id=query.id,
            text="ʏᴏᴜʀ ᴀᴛᴛᴇɴᴅᴀɴᴄᴇ ɪꜱ ᴀʟʀᴇᴀᴅʏ ᴍᴀʀᴋᴇᴅ ʙᴀʙʏ🥀",
            show_alert=True,
        )
    query.answer()


@user_admin_no_reply
def end_attendance(update, context):
    query = update.callback_query
    query.answer()
    if (context.chat_data['id'] != update.effective_chat.id):
        return
    if len(context.chat_data['attendees'].items()) > 0:
        attendee_list = "\n- ".join([
            mention_markdown(id, name)
                for id, name in context.chat_data['attendees'].items()
        ])
        context.bot.edit_message_text(
            text="ᴀᴛᴛᴇɴᴅᴀɴᴄᴇ ɪꜱ ᴏᴠᴇʀ ʙᴀʙʏ🥀. " +
            str(len(context.chat_data['attendees'])) +
            " ᴍᴇᴍʙᴇʀ(s) ᴍᴀʀᴋᴇᴅ ᴀᴛᴛᴇɴᴅᴀɴᴄᴇ.\n" +
            "ʜᴇʀᴇ ɪꜱ ᴛʜᴇ ʟɪꜱᴛ ʙᴀʙʏ🥀:\n- " + attendee_list,
            chat_id=context.chat_data['message'].chat_id,
            message_id=context.chat_data['message'].message_id,
            parse_mode=ParseMode.MARKDOWN,
        )
    else:
        context.bot.edit_message_text(
            text="ᴀᴛᴛᴇɴᴅᴀɴᴄᴇ ɪꜱ ᴏᴠᴇʀ. ɴᴏ ᴏɴᴇ ᴡᴀꜱ ᴘʀᴇꜱᴇɴᴛ ʙᴀʙʏ🥀.",
            chat_id=context.chat_data['message'].chat_id,
            message_id=context.chat_data['message'].message_id,
        )
    context.chat_data['flag'] = 0
    context.chat_data['attendees'].clear()

@user_admin
def end_attendance_cmd(update, context):
    if ('flag' not in context.chat_data) and (context.chat_data['flag'] != 1):
        update.message.reply_text(
            "ɴᴏ ᴀᴛᴛᴇɴᴅᴀɴᴄᴇ ɪꜱ ɢᴏɪɴɢ ᴏɴ ʙᴀʙʏ🥀.",
        )
    else:
        if (context.chat_data['id'] != update.effective_chat.id):
            return
        if len(context.chat_data['attendees'].items()) > 0:
            attendee_list = "\n- ".join([
                mention_markdown(id, name)
                for id, name in context.chat_data['attendees'].items()
            ])
            context.bot.edit_message_text(
                text="ᴀᴛᴛᴇɴᴅᴀɴᴄᴇ ɪꜱ ᴏᴠᴇʀ ʙᴀʙʏ🥀. " +
                str(len(context.chat_data['attendees'])) +
            " ᴍᴇᴍʙᴇʀ(s) ᴍᴀʀᴋᴇᴅ ᴀᴛᴛᴇɴᴅᴀɴᴄᴇ.\n" +
            "ʜᴇʀᴇ ɪꜱ ᴛʜᴇ ʟɪꜱᴛ ʙᴀʙʏ🥀:\n- " + attendee_list,
                chat_id=context.chat_data['message'].chat_id,
                message_id=context.chat_data['message'].message_id,
                parse_mode=ParseMode.MARKDOWN,
            )
        else:
            context.bot.edit_message_text(
                text="ᴀᴛᴛᴇɴᴅᴀɴᴄᴇ ɪꜱ ᴏᴠᴇʀ. ɴᴏ ᴏɴᴇ ᴡᴀꜱ ᴘʀᴇꜱᴇɴᴛ ʙᴀʙʏ🥀.",
                chat_id=context.chat_data['message'].chat_id,
                message_id=context.chat_data['message'].message_id,
            )
        context.chat_data['flag'] = 0
        context.chat_data['attendees'].clear()

__help__ = """
- `/attendance`*:* ꜱᴛᴀʀᴛ ᴛʜᴇ ᴀᴛᴛᴇɴᴅᴀɴᴄᴇ
- `/end_attendance`*:* ᴇɴᴅ ᴛʜᴇ ᴀᴛᴛᴇɴᴅᴀɴᴄᴇ
"""

START_ATTENDANCE = DisableAbleCommandHandler("attendance", start_attendance)
MARK_ATTENDANCE = CallbackQueryHandler(mark_attendance, pattern="present")
END_ATTENDANCE = CallbackQueryHandler(end_attendance, pattern="end_attendance")
END_ATTENDANCE_CMD = DisableAbleCommandHandler("end_attendance", end_attendance_cmd)

dispatcher.add_handler(START_ATTENDANCE)
dispatcher.add_handler(MARK_ATTENDANCE)
dispatcher.add_handler(END_ATTENDANCE)
dispatcher.add_handler(END_ATTENDANCE_CMD)

__mod_name__ = "ATTENDANCE"
__command_list__ = ["attendance", "end_attendance"]
__handlers__ = [START_ATTENDANCE, END_ATTENDANCE, END_ATTENDANCE_CMD]
