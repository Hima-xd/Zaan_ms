from KRISTY.events import register
from KRISTY import telethn

TMP_DOWNLOAD_DIRECTORY = ". /"
from telethon import events
import os
from PIL import Image
from datetime import datetime
from telegraph import Telegraph, upload_file, exceptions

wibu = "KRISTY"
telegraph = Telegraph()
r = telegraph.create_account(short_name=wibu)
auth_url = r["auth_url"]


@register(pattern="^/t(gm|gt) ?(.*)")
async def _(event):
    if event.fwd_from:
        return
    optional_title = event.pattern_match.group(2)
    if event.reply_to_msg_id:
        start = datetime.now()
        r_message = await event.get_reply_message()
        input_str = event.pattern_match.group(1)
        if input_str == "gm":
            downloaded_file_name = await telethn.download_media(
                r_message,
                TMP_DOWNLOAD_DIRECTORY
            )
            end = datetime.now()
            ms = (end - start).seconds
            h = await event.reply("ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ᴛᴏ {} ɪɴ {} ꜱᴇᴄᴏɴᴅꜱ ʙᴀʙʏ🥀.".format(downloaded_file_name, ms))
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.now()
                media_urls = upload_file(downloaded_file_name)
            except exceptions.TelegraphException as exc:
                await h.edit("ᴇʀʀᴏʀ: " + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                ms_two = (end - start).seconds
                os.remove(downloaded_file_name)
                await h.edit("ᴜᴘʟᴏᴀᴅᴇᴅ ᴛᴏ `https://telegra.ph{}` ʙᴀʙʏ🥀".format(media_urls[0], (ms + ms_two)), link_preview=True)
        elif input_str == "gt":
            user_object = await telethn.get_entity(r_message.sender_id)
            title_of_page = user_object.first_name # + " " + user_object.last_name
            # apparently, all Users do not have last_name field
            if optional_title:
                title_of_page = optional_title
            page_content = r_message.message
            if r_message.media:
                if page_content != "":
                    title_of_page = page_content
                downloaded_file_name = await telethn.download_media(
                    r_message,
                    TMP_DOWNLOAD_DIRECTORY
                )
                m_list = None
                with open(downloaded_file_name, "rb") as fd:
                    m_list = fd.readlines()
                for m in m_list:
                    page_content += m.decode("UTF-8") + "\n"
                os.remove(downloaded_file_name)
            page_content = page_content.replace("\n", "<br>")
            response = telegraph.create_page(
                title_of_page,
                html_content=page_content
            )
            end = datetime.now()
            ms = (end - start).seconds
            await event.reply("ᴘᴀꜱᴛᴇᴅ ᴛᴏ `https://telegra.ph/{}` ʙᴀʙʏ🥀".format(response["path"], ms), link_preview=True)
    else:
        await event.reply("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ɢᴇᴛ ᴀ ᴘᴇʀᴍᴀɴᴇɴᴛ telegra.ph ʟɪɴᴋ ʙᴀʙʏ🥀.")


def resize_image(image):
    im = Image.open(image)
    im.save(image, "PNG")

file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
 » `/tgm` :  ɢᴇᴛ ᴛᴇʟᴇɢʀᴀᴘʜ ʟɪɴᴋ ᴏꜰ ʀᴇᴘʟɪᴇᴅ ᴍᴇᴅɪᴀ
 » `/tgt` :  ɢᴇᴛ ᴛᴇʟᴇɢʀᴀᴘʜ ʟɪɴᴋ ᴏꜰ ʀᴇᴘʟɪᴇᴅ ᴛᴇxᴛ
 » `/transfersh` : ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴛᴇʟᴇɢʀᴀᴍ ꜰɪʟᴇ ᴛᴏ ᴜᴘʟᴏᴀᴅ ɪᴛ ᴏɴ ᴛʀᴀɴꜱꜰᴇʀꜱʜ ᴀɴᴅ ɢᴇᴛ ᴅɪʀᴇᴄᴛ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ
 » `/tmpninja` :  ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴛᴇʟᴇɢʀᴀᴍ ꜰɪʟᴇ ᴛᴏ ᴜᴘʟᴏᴀᴅ ɪᴛ ᴏɴ ᴛᴍᴘɴɪɴᴊᴀ ᴀɴᴅ ɢᴇᴛ ᴅɪʀᴇᴄᴛ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ
 """
__mod_name__ = "TELEGRAPH"
