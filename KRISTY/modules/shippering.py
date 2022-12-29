import random
from datetime import datetime

from pyrogram import filters

from KRISTY import pbot
from KRISTY.utils.dbfun import get_couple, save_couple


# Date and time
def dt():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M")
    dt_list = dt_string.split(" ")
    return dt_list


def dt_tom():
    a = (
        str(int(dt()[0].split("/")[0]) + 1)
        + "/"
        + dt()[0].split("/")[1]
        + "/"
        + dt()[0].split("/")[2]
    )
    return a


today = str(dt()[0])
tomorrow = str(dt_tom())


@pbot.on_message(filters.command(["couple", "couples"]))
async def couple(_, message):
    if message.chat.type == "private":
        return await message.reply_text("ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ᴡᴏʀᴋꜱ ɪɴ ɢʀᴏᴜᴘꜱ ʙᴀʙʏ🥀.")
    try:
        chat_id = message.chat.id
        is_selected = await get_couple(chat_id, today)
        if not is_selected:
            list_of_users = []
            async for i in pbot.get_chat_members(message.chat.id):
                if not i.user.is_bot:
                    list_of_users.append(i.user.id)
            if len(list_of_users) < 2:
                return await message.reply_text("ɴᴏᴛ ᴇɴᴏᴜɢʜ ᴜꜱᴇʀꜱ ʙᴀʙʏ🥀")
            c1_id = random.choice(list_of_users)
            c2_id = random.choice(list_of_users)
            while c1_id == c2_id:
                c1_id = random.choice(list_of_users)
            c1_mention = (await pbot.get_users(c1_id)).mention
            c2_mention = (await pbot.get_users(c2_id)).mention

            couple_selection_message = f"""**ᴄᴏᴜᴘʟᴇ ᴏꜰ ᴛʜᴇ ᴅᴀʏ:**
{c1_mention} + {c2_mention} = 😘
__ɴᴇᴡ ᴄᴏᴜᴘʟᴇ ᴏꜰ ᴛʜᴇ ᴅᴀʏ ᴍᴀʏ ʙᴇ ᴄʜᴏꜱᴇɴ ᴀᴛ 12ᴀᴍ ʙᴀʙʏ🥀 {tomorrow}__"""
            await pbot.send_message(message.chat.id, text=couple_selection_message)
            couple = {"c1_id": c1_id, "c2_id": c2_id}
            await save_couple(chat_id, today, couple)

        elif is_selected:
            c1_id = int(is_selected["c1_id"])
            c2_id = int(is_selected["c2_id"])
            c1_name = (await pbot.get_users(c1_id)).first_name
            c2_name = (await pbot.get_users(c2_id)).first_name
            couple_selection_message = f"""ᴄᴏᴜᴘʟᴇ ᴏꜰ ᴛʜᴇ ᴅᴀʏ:
[{c1_name}](tg://openmessage?user_id={c1_id}) + [{c2_name}](tg://openmessage?user_id={c2_id}) = 😘
__ɴᴇᴡ ᴄᴏᴜᴘʟᴇ ᴏꜰ ᴛʜᴇ ᴅᴀʏ ᴍᴀʏ ʙᴇ ᴄʜᴏꜱᴇɴ ᴀᴛ 12ᴀᴍ ʙᴀʙʏ🥀 {tomorrow}__"""
            await pbot.send_message(message.chat.id, text=couple_selection_message)
    except Exception as e:
        print(e)
        await message.reply_text(e)


__help__ = """
 » `/couple` *:* ᴄʜᴏᴏꜱᴇ 2 ᴜꜱᴇʀꜱ ᴀɴᴅ ꜱᴇɴᴅ ᴛʜᴇɪʀ ɴᴀᴍᴇ ᴀꜱ ᴄᴏᴜᴘʟᴇꜱ ɪɴ ʏᴏᴜʀ ᴄʜᴀᴛ.
"""

__mod_name__ = "COUPLE"
