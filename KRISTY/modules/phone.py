import json
import requests

from telethon import types
from telethon.tl import functions

from KRISTY.services.emrror import register,telethn


async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):

        return isinstance(
            (
                await telethn(functions.channels.GetParticipantRequest(chat, user))
            ).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(chat, types.InputPeerChat):

        ui = await telethn.get_peer_id(user)
        ps = (
            await telethn(functions.messages.GetFullChatRequest(chat.chat_id))
        ).full_chat.participants.participants
        return isinstance(
            next((p for p in ps if p.user_id == ui), None),
            (types.ChatParticipantAdmin, types.ChatParticipantCreator),
        )
    return None


@register(pattern=r"^/phone (.*)")
async def phone(event):
    if (
        event.is_group
        and not await is_register_admin(event.input_chat, event.message.sender_id)
    ):
        await event.reply("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ʙᴀʙʏ🥀")
        return
    information = event.pattern_match.group(1)
    number = information
    key = "fe65b94e78fc2e3234c1c6ed1b771abd"
    api = (
        "http://apilayer.net/api/validate?access_key="
        + key
        + "&number="
        + number
        + "&country_code=&format=1"
    )
    output = requests.get(api)
    content = output.text
    obj = json.loads(content)
    country_code = obj["country_code"]
    country_name = obj["country_name"]
    location = obj["location"]
    carrier = obj["carrier"]
    line_type = obj["line_type"]
    validornot = obj["valid"]
    aa = "ᴠᴀʟɪᴅ: " + str(validornot)
    a = "ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ: " + str(number)
    b = "ᴄᴏᴜɴᴛʀʏ: " + str(country_code)
    c = "ᴄᴏᴜɴᴛʀʏ ɴᴀᴍᴇ: " + str(country_name)
    d = "ʟᴏᴄᴀᴛɪᴏɴ: " + str(location)
    e = "ᴄᴀʀʀɪᴇʀ: " + str(carrier)
    f = "ᴅᴇᴠɪᴄᴇ: " + str(line_type)
    g = f"{aa}\n{a}\n{b}\n{c}\n{d}\n{e}\n{f}"
    await event.reply(g)
    
    __help__ = """
 » `/phone` <any fake num> :  ɢᴇɴʀᴀᴛᴇꜱ ꜰᴀᴋᴇ ᴘʜᴏɴᴇ ɪɴꜰᴏ.
 """
__mod_name__ = "PHONE"
