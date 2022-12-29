from geopy.geocoders import Nominatim
from telethon import *
from telethon.tl import *

from KRISTY import *
from KRISTY import telethn as tbot
from KRISTY.events import register

GMAPS_LOC = "https://maps.googleapis.com/maps/api/geocode/json"


@register(pattern="^/gps (.*)")
async def _(event):
    args = event.pattern_match.group(1)

    try:
        geolocator = Nominatim(user_agent="SkittBot")
        location = args
        geoloc = geolocator.geocode(location)
        longitude = geoloc.longitude
        latitude = geoloc.latitude
        gm = "https://www.google.com/maps/search/{},{}".format(latitude, longitude)
        await tbot.send_file(
            event.chat_id,
            file=types.InputMediaGeoPoint(
                types.InputGeoPoint(float(latitude), float(longitude))
            ),
        )
        await event.reply(
            "ʜᴇʀᴇ ɪꜱ ʏᴏᴜʀ ʀᴇQᴜɪʀᴇᴅ ʟᴏᴄᴀᴛɪᴏɴ ʏᴏᴜ ᴄᴀɴ ꜰɪɴᴅ ɪᴛ ʙʏ ᴄʟɪᴄᴋɪɴɢ ʜᴇʀᴇ: [ʜᴇʀᴇ]({}) ʙᴀʙʏ🥀".format(gm),
            link_preview=False,
        )
    except Exception as e:
        print(e)
        await event.reply("ɪ ᴀᴍ ᴜɴᴀʙᴀʟᴇ ᴛᴏ ꜰɪɴᴅ ᴛʜᴀᴛ ꜱᴏʀʀʏ ʙᴀʙʏ🥀")


__help__ = """
 » /gps <location>*:* ɢᴇᴛꜱ ʏᴏᴜ ʏᴏᴜʀ ᴅᴇꜱɪʀᴇᴅ ʟᴏᴄᴀᴛɪᴏɴ.
"""

__mod_name__ = "GPS"
