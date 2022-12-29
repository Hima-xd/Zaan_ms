import os
import wget
import urllib.request
from faker import Faker
import pyaztro
from faker.providers import internet
from KRISTY import dispatcher
from KRISTY.modules.disable import DisableAbleCommandHandler
from telegram import Update, ParseMode
from telegram.ext import CallbackContext, run_async


def fakeid(update: Update, context: CallbackContext):
    message = update.effective_message
    dltmsg = message.reply_text("ɢᴇɴᴇʀᴀᴛɪɴɢ ꜰᴀᴋᴇ ɪᴅᴇɴᴛɪᴛʏ ꜰᴏʀ ʏᴏᴜ ʙᴀʙʏ🥀...")
    fake = Faker()
    print("ꜰᴀᴋᴇ ᴅᴇᴛᴀɪʟꜱ ɢᴇɴᴇʀᴀᴛᴇᴅ\n")
    name = str(fake.name())
    fake.add_provider(internet)
    address = str(fake.address())
    ip = fake.ipv4_private()
    cc = fake.credit_card_full()
    email = fake.ascii_free_email()
    job = fake.job()
    android = fake.android_platform_token()
    pc = fake.chrome()
    message.reply_text(
        f"<b> ꜰᴀᴋᴇ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ ɢᴇɴᴇʀᴀᴛᴇᴅ</b>\n<b>ɴᴀᴍᴇ :-</b><code>{name}</code>\n\n<b>ᴀᴅᴅʀᴇꜱꜱ:-</b><code>{address}</code>\n\n<b>ɪᴘ ᴀᴅᴅʀᴇꜱꜱ:-</b><code>{ip}</code>\n\n<b>ᴄʀᴇᴅɪᴛ ᴄᴀʀᴅ:-</b><code>{cc}</code>\n\n<b>ᴇᴍᴀɪʟ ɪᴅ:-</b><code>{email}</code>\n\n<b>ᴊᴏʙ:-</b><code>{job}</code>\n\n<b>ᴀɴᴅʀᴏɪᴅ ᴜꜱᴇʀ ᴀɢᴇɴᴛ:-</b><code>{android}</code>\n\n<b>ᴘᴄ ᴜꜱᴇʀ ᴀɢᴇɴᴛ:-</b><code>{pc}</code>",
        parse_mode=ParseMode.HTML,
    )

    dltmsg.delete()




def astro(update: Update, context: CallbackContext):
    message = update.effective_message
    args = message.text.split(" ", 1)
    
    if len(args) == 1:
        message.reply_text('ᴘʟᴇᴀꜱᴇ ᴄʜᴏᴏꜱᴇ ʏᴏᴜʀ ʜᴏʀᴏꜱᴄᴏᴘᴇ ꜱɪɢɴ. ʟɪꜱᴛ ᴏꜰ ᴀʟʟ ꜱɪɢɴꜱ - ᴀʀɪᴇꜱ, ᴛᴀᴜʀᴜꜱ, ɢᴇᴍɪɴɪ, ᴄᴀɴᴄᴇʀ, ʟᴇᴏ, ᴠɪʀɢᴏ, ʟɪʙʀᴀ, ꜱᴄᴏʀᴘɪᴏ, ꜱᴀɢɪᴛᴛᴀʀɪᴜꜱ, ᴄᴀᴘʀɪᴄᴏʀɴ, ᴀQᴜᴀʀɪᴜꜱ ᴀɴᴅ ᴘɪꜱᴄᴇꜱ ʙᴀʙʏ🥀.')
        return
    else:
        pass
    msg = message.reply_text("ꜰᴇᴛᴄʜɪɴɢ ᴅᴀᴛᴀ ʙᴀʙʏ🥀...")
    try:
        x = args[1]
        horoscope = pyaztro.Aztro(sign=x)
        mood = horoscope.mood
        lt = horoscope.lucky_time
        desc = horoscope.description
        col = horoscope.color
        com = horoscope.compatibility
        ln = horoscope.lucky_number

        result = (
            f"**ʜᴏʀᴏꜱᴄᴏᴘᴇ ꜰᴏʀ `{x}`**:\n"
            f"**ᴍᴏᴏᴅ :** `{mood}`\n"
            f"**ʟᴜᴄᴋʏ ᴛɪᴍᴇ :** `{lt}`\n"
            f"**ʟᴜᴄᴋʏ ᴄᴏʟᴏʀ :** `{col}`\n"
            f"**ʟᴜᴄᴋʏ ɴᴜᴍʙᴇʀ :** `{ln}`\n"
            f"**ᴄᴏᴍᴘᴀᴛɪʙɪʟɪᴛʏ :** `{com}`\n"
            f"**ᴅᴇꜱᴄʀɪᴘᴛɪᴏɴ :** `{desc}`\n"
        )

        msg.edit_text(result, parse_mode=ParseMode.MARKDOWN)

    except Exception as e:
        msg.edit_text(f"ꜱᴏʀʀʏ ɪ ʜᴀᴠᴇɴ'ᴛ ꜰᴏᴜɴᴅ ᴀɴʏᴛʜɪɴɢ!\nᴍᴀʏʙᴇ ʏᴏᴜ ʜᴀᴠᴇ ɢɪᴠᴇɴ ᴀ ᴡʀᴏɴɢ ꜱɪɢɴ ɴᴀᴍᴇ ᴘʟᴇᴀꜱᴇ ᴄʜᴇᴄᴋ ʜᴇʟᴘ ᴏꜰ ʜᴏʀᴏꜱᴄᴏᴘᴇ.\nᴇʀʀᴏʀ - {e} ʙᴀʙʏ🥀")



__help__ = """
 » `/hs <ᴢᴏᴅɪᴀᴄ-ꜱɪɢɴꜱ>`:
ᴜꜱᴀɢᴇ: ɪᴛ ᴡɪʟʟ ꜱʜᴏᴡ ʜᴏʀᴏꜱᴄᴏᴘᴇ ᴏꜰ ᴅᴀɪʟʏ ᴏꜰ ʏᴏᴜʀ ꜱɪɢɴ.
 ʟɪꜱᴛ ᴏꜰ ᴀʟʟ ꜱɪɢɴꜱ - ᴀʀɪᴇꜱ, ᴛᴀᴜʀᴜꜱ, ɢᴇᴍɪɴɪ, ᴄᴀɴᴄᴇʀ, ʟᴇᴏ, ᴠɪʀɢᴏ, ʟɪʙʀᴀ, ꜱᴄᴏʀᴘɪᴏ, ꜱᴀɢɪᴛᴛᴀʀɪᴜꜱ, ᴄᴀᴘʀɪᴄᴏʀɴ, ᴀQᴜᴀʀɪᴜꜱ ᴀɴᴅ ᴘɪꜱᴄᴇꜱ.
 » `/fakeid`:
ᴜꜱᴀɢᴇ: ɪᴛ ᴡɪʟʟ ꜰᴀᴋᴇ ɪᴅᴇɴᴛɪᴛʏ ꜰᴏʀ ʏᴏᴜ.
"""

__mod_name__ = "IDENTITY"

FAKER_HANDLER = DisableAbleCommandHandler("fakeid", fakeid, run_async=True)
ASTRO_HANDLER = DisableAbleCommandHandler("hs", astro, run_async=True)
dispatcher.add_handler(FAKER_HANDLER)
dispatcher.add_handler(ASTRO_HANDLER)
