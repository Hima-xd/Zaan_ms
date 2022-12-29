import random
import threading
from typing import Union

from KRISTY.modules.helper_funcs.msg_types import Types
from KRISTY.modules.sql import BASE, SESSION
from sqlalchemy import Boolean, Column, String, UnicodeText, Integer
from sqlalchemy.sql.sqltypes import BigInteger

DEFAULT_WELCOME_MESSAGES = [
    "{first} ɪꜱ ʜᴇʀᴇ ʙᴀʙʏ🥀!",
    "ʀᴇᴀᴅʏ ᴘʟᴀʏᴇʀ {first} ʙᴀʙʏ🥀",
    "ɢᴇɴᴏꜱ, {first} ɪꜱ ʜᴇʀᴇ ʙᴀʙʏ🥀.",
    "ᴀ ᴡɪʟᴅ {first} ᴀᴘᴘᴇᴀʀᴇᴅ ʙᴀʙʏ🥀.",
    "{first} ᴄᴀᴍᴇ ɪɴ ʟɪᴋᴇ ᴀ ʟɪᴏɴ ʙᴀʙʏ🥀!",
    "{first} ʜᴀꜱ ᴊᴏɪɴᴇᴅ ʏᴏᴜʀ ᴘᴀʀᴛʏ ʙᴀʙʏ🥀.",
    "{first} ᴊᴜꜱᴛ ᴊᴏɪɴᴇᴅ. ᴄᴀɴ ɪ ɢᴇᴛ ᴀ ʜᴇᴀʟ? ʙᴀʙʏ🥀",
    "{first} ᴊᴜꜱᴛ ᴊᴏɪɴᴇᴅ ᴛʜᴇ ᴄʜᴀᴛ - ᴀꜱᴅɢꜰʜᴀᴋ ʙᴀʙʏ🥀!",
    "{first} ᴊᴜꜱᴛ ᴊᴏɪɴᴇᴅ. ᴇᴠᴇʀʏᴏɴᴇ, ʟᴏᴏᴋ ʙᴜꜱʏ ʙᴀʙʏ🥀!",
    "ᴡᴇʟᴄᴏᴍᴇ, {first}. ꜱᴛᴀʏ ᴀᴡʜɪʟᴇ ᴀɴᴅ ʟɪꜱᴛᴇɴ ʙᴀʙʏ🥀.",
    "ᴡᴇʟᴄᴏᴍᴇ, {first}. ᴡᴇ ᴡᴇʀᴇ ᴇxᴘᴇᴄᴛɪɴɢ ʏᴏᴜ ( ͡° ͜ʖ ͡°) ʙᴀʙʏ🥀",
    "ᴡᴇʟᴄᴏᴍᴇ, {first}. ᴡᴇ ʜᴏᴘᴇ ʏᴏᴜ ʙʀᴏᴜɢʜᴛ ᴘɪᴢᴢᴀ ʙᴀʙʏ🥀.",
    "ᴡᴇʟᴄᴏᴍᴇ, {first}. ʟᴇᴀᴠᴇ ʏᴏᴜʀ ᴡᴇᴀᴘᴏɴꜱ ʙʏ ᴛʜᴇ ᴅᴏᴏʀ ʙᴀʙʏ🥀.",
    "ꜱᴡᴏᴏᴏᴏꜱʜ. {first} ᴊᴜꜱᴛ ʟᴀɴᴅᴇᴅ ʙᴀʙʏ🥀.",
    "ʙʀᴀᴄᴇ ʏᴏᴜʀꜱᴇʟᴠᴇꜱ. {first} ᴊᴜꜱᴛ ᴊᴏɪɴᴇᴅ ᴛʜᴇ ᴄʜᴀᴛ ʙᴀʙʏ🥀.",
    "{first} ᴊᴜꜱᴛ ᴊᴏɪɴᴇᴅ. ʜɪᴅᴇ ʏᴏᴜʀ ʙᴀɴᴀɴᴀꜱ ʙᴀʙʏ🥀.",
    "{first} ᴊᴜꜱᴛ ᴀʀʀɪᴠᴇᴅ. ꜱᴇᴇᴍꜱ ᴏᴘ - ᴘʟᴇᴀꜱᴇ ɴᴇʀꜰ ʙᴀʙʏ🥀.",
    "{first} ᴊᴜꜱᴛ ꜱʟɪᴅ ɪɴᴛᴏ ᴛʜᴇ ᴄʜᴀᴛ ʙᴀʙʏ🥀.",
    "ᴀ {first} ʜᴀꜱ ꜱᴘᴀᴡɴᴇᴅ ɪɴ ᴛʜᴇ ᴄʜᴀᴛ ʙᴀʙʏ🥀.",
    "ʙɪɢ {first} ꜱʜᴏᴡᴇᴅ ᴜᴘ ʙᴀʙʏ🥀!",
    "ᴡʜᴇʀᴇ’ꜱ {first}? ɪɴ ᴛʜᴇ ᴄʜᴀᴛ ʙᴀʙʏ🥀!",
    "{first} ʜᴏᴘᴘᴇᴅ ɪɴᴛᴏ ᴛʜᴇ ᴄʜᴀᴛ. ᴋᴀɴɢᴀʀᴏᴏ ʙᴀʙʏ🥀!!",
    "{first} ᴊᴜꜱᴛ ꜱʜᴏᴡᴇᴅ ᴜᴘ. ʜᴏʟᴅ ᴍʏ ʙᴇᴇʀ ʙᴀʙʏ🥀.",
    "ᴄʜᴀʟʟᴇɴɢᴇʀ ᴀᴘᴘʀᴏᴀᴄʜɪɴɢ! {first} ʜᴀꜱ ᴀᴘᴘᴇᴀʀᴇᴅ ʙᴀʙʏ🥀!",
    "ɪᴛ'ꜱ ᴀ ʙɪʀᴅ! ɪᴛ'ꜱ ᴀ ᴘʟᴀɴᴇ! ɴᴇᴠᴇʀᴍɪɴᴅ, ɪᴛ'ꜱ ᴊᴜꜱᴛ {first} ʙᴀʙʏ🥀.",
    "ɪᴛ'ꜱ {first}! ᴘʀᴀɪꜱᴇ ᴛʜᴇ ꜱᴜɴ ʙᴀʙʏ🥀! \ᴏ/",
    "ɴᴇᴠᴇʀ ɢᴏɴɴᴀ ɢɪᴠᴇ {first} ᴜᴘ. ɴᴇᴠᴇʀ ɢᴏɴɴᴀ ʟᴇᴛ {first} ᴅᴏᴡɴ ʙᴀʙʏ🥀.",
    "ʜᴀ! {first} ʜᴀꜱ ᴊᴏɪɴᴇᴅ! ʏᴏᴜ ᴀᴄᴛɪᴠᴀᴛᴇᴅ ᴍʏ ᴛʀᴀᴘ ᴄᴀʀᴅ ʙᴀʙʏ🥀!",
    "ʜᴇʏ! ʟɪꜱᴛᴇɴ! {first} ʜᴀꜱ ᴊᴏɪɴᴇᴅ ʙᴀʙʏ🥀!",
    "ᴡᴇ'ᴠᴇ ʙᴇᴇɴ ᴇxᴘᴇᴄᴛɪɴɢ ʏᴏᴜ {first} ʙᴀʙʏ🥀",
    "ɪᴛ'ꜱ ᴅᴀɴɢᴇʀᴏᴜꜱ ᴛᴏ ɢᴏ ᴀʟᴏɴᴇ, ᴛᴀᴋᴇ {first} ʙᴀʙʏ🥀!",
    "{first} ʜᴀꜱ ᴊᴏɪɴᴇᴅ ᴛʜᴇ ᴄʜᴀᴛ! ɪᴛ'ꜱ ꜱᴜᴘᴇʀ ᴇꜰꜰᴇᴄᴛɪᴠᴇ ʙᴀʙʏ🥀!",
    "ᴄʜᴇᴇʀꜱ, ʟᴏᴠᴇ! {first} ɪꜱ ʜᴇʀᴇ ʙᴀʙʏ🥀!",
    "{first} ɪꜱ ʜᴇʀᴇ, ᴀꜱ ᴛʜᴇ ᴘʀᴏᴘʜᴇᴄʏ ꜰᴏʀᴇᴛᴏʟᴅ ʙᴀʙʏ🥀.",
    "{first} ʜᴀꜱ ᴀʀʀɪᴠᴇᴅ. ᴘᴀʀᴛʏ'ꜱ ᴏᴠᴇʀ ʙᴀʙʏ🥀.",
    "{first} ɪꜱ ʜᴇʀᴇ ᴛᴏ ᴋɪᴄᴋ ʙᴜᴛᴛ ᴀɴᴅ ᴄʜᴇᴡ ʙᴜʙʙʟᴇɢᴜᴍ. ᴀɴᴅ {first} ɪꜱ ᴀʟʟ ᴏᴜᴛ ᴏꜰ ɢᴜᴍ ʙᴀʙʏ🥀.",
    "ʜᴇʟʟᴏ. ɪꜱ ɪᴛ {first} ʏᴏᴜ'ʀᴇ ʟᴏᴏᴋɪɴɢ ꜰᴏʀ? ʙᴀʙʏ🥀",
    "{first} ʜᴀꜱ ᴊᴏɪɴᴇᴅ. ꜱᴛᴀʏ ᴀᴡʜɪʟᴇ ᴀɴᴅ ʟɪꜱᴛᴇɴ ʙᴀʙʏ🥀!",
    "ʀᴏꜱᴇꜱ ᴀʀᴇ ʀᴇᴅ, ᴠɪᴏʟᴇᴛꜱ ᴀʀᴇ ʙʟᴜᴇ, {first} ᴊᴏɪɴᴇᴅ ᴛʜɪꜱ ᴄʜᴀᴛ ᴡɪᴛʜ ʏᴏᴜ ʙᴀʙʏ🥀",
    "ᴡᴇʟᴄᴏᴍᴇ {first}, ᴀᴠᴏɪᴅ ᴘᴜɴᴄʜᴇꜱ ɪꜰ ʏᴏᴜ ᴄᴀɴ ʙᴀʙʏ🥀!",
    "ɪᴛ'ꜱ ᴀ ʙɪʀᴅ! ɪᴛ'ꜱ ᴀ ᴘʟᴀɴᴇ! - ɴᴏᴘᴇ, ɪᴛꜱ {first} ʙᴀʙʏ🥀!",
    "{first} ᴊᴏɪɴᴇᴅ! - ᴏᴋ ʙᴀʙʏ🥀.",
    "ᴀʟʟ ʜᴀɪʟ {first} ʙᴀʙʏ🥀!",
    "ʜɪ, {first}. ᴅᴏɴ'ᴛ ʟᴜʀᴋ, ᴏɴʟʏ ᴠɪʟʟᴀɴꜱ ᴅᴏ ᴛʜᴀᴛ ʙᴀʙʏ🥀.",
    "{first} ʜᴀꜱ ᴊᴏɪɴᴇᴅ ᴛʜᴇ ʙᴀᴛᴛʟᴇ ʙᴜꜱ ʙᴀʙʏ🥀.",
    "ᴀ ɴᴇᴡ ᴄʜᴀʟʟᴇɴɢᴇʀ ᴇɴᴛᴇʀꜱ ʙᴀʙʏ🥀!",
    "ᴏᴋ ʙᴀʙʏ🥀!",
    "{first} ᴊᴜꜱᴛ ꜰᴇʟʟ ɪɴᴛᴏ ᴛʜᴇ ᴄʜᴀᴛ ʙᴀʙʏ🥀!",
    "ꜱᴏᴍᴇᴛʜɪɴɢ ᴊᴜꜱᴛ ꜰᴇʟʟ ꜰʀᴏᴍ ᴛʜᴇ ꜱᴋʏ! - ᴏʜ, ɪᴛꜱ {first} ʙᴀʙʏ🥀.",
    "{first} ᴊᴜꜱᴛ ᴛᴇʟᴇᴘᴏʀᴛᴇᴅ ɪɴᴛᴏ ᴛʜᴇ ᴄʜᴀᴛ ʙᴀʙʏ🥀!",
    "ʜɪ, {first}, ꜱʜᴏᴡ ᴍᴇ ʏᴏᴜʀ ʜᴜɴᴛᴇʀ ʟɪᴄᴇɴꜱᴇ ʙᴀʙʏ🥀!",
    "ɪ'ᴍ ʟᴏᴏᴋɪɴɢ ꜰᴏʀ ɢᴀʀᴏ, ᴏʜ ᴡᴀɪᴛ ɴᴠᴍ ɪᴛ'ꜱ {first} ʙᴀʙʏ🥀.",
    "ᴡᴇʟᴄᴏᴍᴇ {first}, ʟᴇᴀᴠɪɴɢ ɪꜱ ɴᴏᴛ ᴀɴ ᴏᴘᴛɪᴏɴ ʙᴀʙʏ🥀!",
    "ʀᴜɴ ꜰᴏʀᴇꜱᴛ! ..ɪ ᴍᴇᴀɴ...{first} ʙᴀʙʏ🥀.",
    "{first} ᴅᴏ 100 ᴘᴜꜱʜ-ᴜᴘꜱ, 100 ꜱɪᴛ-ᴜᴘꜱ, 100 ꜱQᴜᴀᴛꜱ, ᴀɴᴅ 10ᴋᴍ ʀᴜɴɴɪɴɢ ᴇᴠᴇʀʏ ꜱɪɴɢʟᴇ ᴅᴀʏ ʙᴀʙʏ🥀!!!",  
      "ʜᴜʜ?/nᴅɪᴅ ꜱᴏᴍᴇᴏɴᴇ ᴡɪᴛʜ ᴀ ᴅɪꜱᴀꜱᴛᴇʀ ʟᴇᴠᴇʟ ᴊᴜꜱᴛ ᴊᴏɪɴ?/nᴏʜ ᴡᴀɪᴛ, ɪᴛ'ꜱ ᴊᴜꜱᴛ {first} ʙᴀʙʏ🥀.",
      "ʜᴇʏ, {first}, ᴇᴠᴇʀ ʜᴇᴀʀᴅ ᴛʜᴇ ᴋɪɴɢ ᴇɴɢɪɴᴇ? ʙᴀʙʏ🥀",
      "ʜᴇʏ, {first}, ᴇᴍᴘᴛʏ ʏᴏᴜʀ ᴘᴏᴄᴋᴇᴛꜱ ʙᴀʙʏ🥀.",
      "ʜᴇʏ, {first}!, ᴀʀᴇ ʏᴏᴜ ꜱᴛʀᴏɴɢ? ʙᴀʙʏ🥀",
      "ᴄᴀʟʟ ᴛʜᴇ ᴀᴠᴇɴɢᴇʀꜱ! - {first} ᴊᴜꜱᴛ ᴊᴏɪɴᴇᴅ ᴛʜᴇ ᴄʜᴀᴛ ʙᴀʙʏ🥀.",
      "{first} ᴊᴏɪɴᴇᴅ. ʏᴏᴜ ᴍᴜꜱᴛ ᴄᴏɴꜱᴛʀᴜᴄᴛ ᴀᴅᴅɪᴛɪᴏɴᴀʟ ᴘʏʟᴏɴꜱ ʙᴀʙʏ🥀.",
      "ᴇʀᴍᴀɢʜᴇʀᴅ. {first} ɪꜱ ʜᴇʀᴇ ʙᴀʙʏ🥀.",
      "ᴄᴏᴍᴇ ꜰᴏʀ ᴛʜᴇ ꜱɴᴀɪʟ ʀᴀᴄɪɴɢ, ꜱᴛᴀʏ ꜰᴏʀ ᴛʜᴇ ᴄʜɪᴍɪᴄʜᴀɴɢᴀꜱ ʙᴀʙʏ🥀!",
      "ᴡʜᴏ ɴᴇᴇᴅꜱ ɢᴏᴏɢʟᴇ? ʏᴏᴜ'ʀᴇ ᴇᴠᴇʀʏᴛʜɪɴɢ ᴡᴇ ᴡᴇʀᴇ ꜱᴇᴀʀᴄʜɪɴɢ ꜰᴏʀ ʙᴀʙʏ🥀.",
      "ᴛʜɪꜱ ᴘʟᴀᴄᴇ ᴍᴜꜱᴛ ʜᴀᴠᴇ ꜰʀᴇᴇ ᴡɪꜰɪ, ᴄᴀᴜꜱᴇ ɪ'ᴍ ꜰᴇᴇʟɪɴɢ ᴀ ᴄᴏɴɴᴇᴄᴛɪᴏɴ ʙᴀʙʏ🥀.",
      "ꜱᴘᴇᴀᴋ ꜰʀɪᴇɴᴅ ᴀɴᴅ ᴇɴᴛᴇʀ ʙᴀʙʏ🥀.",
      "ᴡᴇʟᴄᴏᴍᴇ ʏᴏᴜ ᴀʀᴇ ʙᴀʙʏ🥀",
      "ᴡᴇʟᴄᴏᴍᴇ {first}, ʏᴏᴜʀ ᴘʀɪɴᴄᴇꜱꜱ ɪꜱ ɪɴ ᴀɴᴏᴛʜᴇʀ ᴄᴀꜱᴛʟᴇ ʙᴀʙʏ🥀.",
      "ʜɪ {first}, ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ᴅᴀʀᴋ ꜱɪᴅᴇ ʙᴀʙʏ🥀.",
      "ʜᴏʟᴀ {first}, ʙᴇᴡᴀʀᴇ ᴏꜰ ᴘᴇᴏᴘʟᴇ ᴡɪᴛʜ ᴅɪꜱᴀꜱᴛᴇʀ ʟᴇᴠᴇʟꜱ ʙᴀʙʏ🥀",
]
DEFAULT_GOODBYE_MESSAGES = [

"{first} ᴡɪʟʟ ʙᴇ ᴍɪꜱꜱᴇᴅ ʙᴀʙʏ🥀.",
"{first} ᴊᴜꜱᴛ ᴡᴇɴᴛ ᴏꜰꜰʟɪɴᴇ ʙᴀʙʏ🥀.",
"{first} ʜᴀꜱ ʟᴇꜰᴛ ᴛʜᴇ ʟᴏʙʙʏ ʙᴀʙʏ🥀.",
"{first} ʜᴀꜱ ʟᴇꜰᴛ ᴛʜᴇ ᴄʟᴀɴ ʙᴀʙʏ🥀.",
"{first} ʜᴀꜱ ʟᴇꜰᴛ ᴛʜᴇ ɢᴀᴍᴇ ʙᴀʙʏ🥀.",
"{first} ʜᴀꜱ ꜰʟᴇᴅ ᴛʜᴇ ᴀʀᴇᴀ ʙᴀʙʏ🥀.",
"{first} ɪꜱ ᴏᴜᴛ ᴏꜰ ᴛʜᴇ ʀᴜɴɴɪɴɢ ʙᴀʙʏ🥀.",
"ɴɪᴄᴇ ᴋɴᴏᴡɪɴɢ ʏᴀ, {first} ʙᴀʙʏ🥀!",
"ɪᴛ ᴡᴀꜱ ᴀ ꜰᴜɴ ᴛɪᴍᴇ {first} ʙᴀʙʏ🥀.",
"ᴡᴇ ʜᴏᴘᴇ ᴛᴏ ꜱᴇᴇ ʏᴏᴜ ᴀɢᴀɪɴ ꜱᴏᴏɴ, {first} ʙᴀʙʏ🥀.",
"ɪ ᴅᴏɴᴜᴛ ᴡᴀɴᴛ ᴛᴏ ꜱᴀʏ ɢᴏᴏᴅʙʏᴇ, {first} ʙᴀʙʏ🥀.",
"ɢᴏᴏᴅʙʏᴇ {first}! ɢᴜᴇꜱꜱ ᴡʜᴏ'ꜱ ɢᴏɴɴᴀ ᴍɪꜱꜱ ʏᴏᴜ :') ʙᴀʙʏ🥀",
"ɢᴏᴏᴅʙʏᴇ {first}! ɪᴛ'ꜱ ɢᴏɴɴᴀ ʙᴇ ʟᴏɴᴇʟʏ ᴡɪᴛʜᴏᴜᴛ ʏᴀ ʙᴀʙʏ🥀.",
"ᴘʟᴇᴀꜱᴇ ᴅᴏɴ'ᴛ ʟᴇᴀᴠᴇ ᴍᴇ ᴀʟᴏɴᴇ ɪɴ ᴛʜɪꜱ ᴘʟᴀᴄᴇ, {first} ʙᴀʙʏ🥀!",
"ɢᴏᴏᴅ ʟᴜᴄᴋ ꜰɪɴᴅɪɴɢ ʙᴇᴛᴛᴇʀ ꜱʜɪᴛ-ᴘᴏꜱᴛᴇʀꜱ ᴛʜᴀɴ ᴜꜱ, {first} ʙᴀʙʏ🥀!",
"ʏᴏᴜ ᴋɴᴏᴡ ᴡᴇ'ʀᴇ ɢᴏɴɴᴀ ᴍɪꜱꜱ ʏᴏᴜ {first}. ʀɪɢʜᴛ? ʀɪɢʜᴛ? ʀɪɢʜᴛ? ʙᴀʙʏ🥀",
"ᴄᴏɴɢʀᴀᴛᴜʟᴀᴛɪᴏɴꜱ, {first}! ʏᴏᴜ'ʀᴇ ᴏꜰꜰɪᴄɪᴀʟʟʏ ꜰʀᴇᴇ ᴏꜰ ᴛʜɪꜱ ᴍᴇꜱꜱ ʙᴀʙʏ🥀.",
"{first}. ʏᴏᴜ ᴡᴇʀᴇ ᴀɴ ᴏᴘᴘᴏɴᴇɴᴛ ᴡᴏʀᴛʜ ꜰɪɢʜᴛɪɴɢ ʙᴀʙʏ🥀.",
"ʏᴏᴜ'ʀᴇ ʟᴇᴀᴠɪɴɢ, {first}? ʏᴀʀᴇ ʏᴀʀᴇ ᴅᴀᴢᴇ ʙᴀʙʏ🥀.",
"ʙʀɪɴɢ ʜɪᴍ ᴛʜᴇ ᴘʜᴏᴛᴏ ʙᴀʙʏ🥀",
"ɢᴏ ᴏᴜᴛꜱɪᴅᴇ ʙᴀʙʏ🥀!",
"ᴀꜱᴋ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ ʙᴀʙʏ🥀",
"ᴛʜɪɴᴋ ꜰᴏʀ ʏᴏᴜʀꜱᴇʟꜰ ʙᴀʙʏ🥀",
"Qᴜᴇꜱᴛɪᴏɴ ᴀᴜᴛʜᴏʀɪᴛʏ ʙᴀʙʏ🥀",
"ʏᴏᴜ ᴀʀᴇ ᴡᴏʀꜱʜɪᴘɪɴɢ ᴀ ꜱᴜɴ ɢᴏᴅ ʙᴀʙʏ🥀",
"ᴅᴏɴ'ᴛ ʟᴇᴀᴠᴇ ᴛʜᴇ ʜᴏᴜꜱᴇ ᴛᴏᴅᴀʏ ʙᴀʙʏ🥀",
"ɢɪᴠᴇ ᴜᴘ ʙᴀʙʏ🥀!",
"ᴍᴀʀʀʏ ᴀɴᴅ ʀᴇᴘʀᴏᴅᴜᴄᴇ ʙᴀʙʏ🥀",
"ꜱᴛᴀʏ ᴀꜱʟᴇᴇᴘ ʙᴀʙʏ🥀",
"ᴡᴀᴋᴇ ᴜᴘ ʙᴀʙʏ🥀",
"ʟᴏᴏᴋ ᴛᴏ ʟᴀ ʟᴜɴᴀ ʙᴀʙʏ🥀",
"ꜱᴛᴇᴠᴇɴ ʟɪᴠᴇꜱ ʙᴀʙʏ🥀",
"ᴍᴇᴇᴛ ꜱᴛʀᴀɴɢᴇʀꜱ ᴡɪᴛʜᴏᴜᴛ ᴘʀᴇᴊᴜᴅɪᴄᴇ ʙᴀʙʏ🥀",
"ᴀ ʜᴀɴɢᴇᴅ ᴍᴀɴ ᴡɪʟʟ ʙʀɪɴɢ ʏᴏᴜ ɴᴏ ʟᴜᴄᴋ ᴛᴏᴅᴀʏ ʙᴀʙʏ🥀",
"ᴡʜᴀᴛ ᴅᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴏ ᴛᴏᴅᴀʏ? ʙᴀʙʏ🥀",
"ʏᴏᴜ ᴀʀᴇ ᴅᴀʀᴋ ɪɴꜱɪᴅᴇ ʙᴀʙʏ🥀",
"ʜᴀᴠᴇ ʏᴏᴜ ꜱᴇᴇɴ ᴛʜᴇ ᴇxɪᴛ?",
"ɢᴇᴛ ᴀ ʙᴀʙʏ ᴘᴇᴛ ɪᴛ ᴡɪʟʟ ᴄʜᴇᴇʀ ʏᴏᴜ ᴜᴘ ʙᴀʙʏ🥀.",
"ʏᴏᴜʀ ᴘʀɪɴᴄᴇꜱꜱ ɪꜱ ɪɴ ᴀɴᴏᴛʜᴇʀ ᴄᴀꜱᴛʟᴇ ʙᴀʙʏ🥀.",
"ʏᴏᴜ ᴀʀᴇ ᴘʟᴀʏɪɴɢ ɪᴛ ᴡʀᴏɴɢ ɢɪᴠᴇ ᴍᴇ ᴛʜᴇ ᴄᴏɴᴛʀᴏʟʟᴇʀ ʙᴀʙʏ🥀",
"ᴛʀᴜꜱᴛ ɢᴏᴏᴅ ᴘᴇᴏᴘʟᴇ ʙᴀʙʏ🥀",
"ʟɪᴠᴇ ᴛᴏ ᴅɪᴇ ʙᴀʙʏ🥀.",
"ᴡʜᴇɴ ʟɪꜰᴇ ɢɪᴠᴇꜱ ʏᴏᴜ ʟᴇᴍᴏɴꜱ ʀᴇʀᴏʟʟ ʙᴀʙʏ🥀!",
"ᴡᴇʟʟ, ᴛʜᴀᴛ ᴡᴀꜱ ᴡᴏʀᴛʜʟᴇꜱꜱ ʙᴀʙʏ🥀  ",
"ɪ ꜰᴇʟʟ ᴀꜱʟᴇᴇᴘ ʙᴀʙʏ🥀!",
"ᴍᴀʏ ʏᴏᴜʀ ᴛʀᴏᴜʙʟᴇꜱ ʙᴇ ᴍᴀɴʏ ʙᴀʙʏ🥀",
"ʏᴏᴜʀ ᴏʟᴅ ʟɪꜰᴇ ʟɪᴇꜱ ɪɴ ʀᴜɪɴ ʙᴀʙʏ🥀",
"ᴀʟᴡᴀʏꜱ ʟᴏᴏᴋ ᴏɴ ᴛʜᴇ ʙʀɪɢʜᴛ ꜱɪᴅᴇ ʙᴀʙʏ🥀",
"ɪᴛ ɪꜱ ᴅᴀɴɢᴇʀᴏᴜꜱ ᴛᴏ ɢᴏ ᴀʟᴏɴᴇ ʙᴀʙʏ🥀",
"ʏᴏᴜ ᴡɪʟʟ ɴᴇᴠᴇʀ ʙᴇ ꜰᴏʀɢɪᴠᴇɴ ʙᴀʙʏ🥀",
"ʏᴏᴜ ʜᴀᴠᴇ ɴᴏʙᴏᴅʏ ᴛᴏ ʙʟᴀᴍᴇ ʙᴜᴛ ʏᴏᴜʀꜱᴇʟꜰ ʙᴀʙʏ🥀",
"ᴏɴʟʏ ᴀ ꜱɪɴɴᴇʀ ʙᴀʙʏ🥀",
"ᴜꜱᴇ ʙᴏᴍʙꜱ ᴡɪꜱᴇʟʏ ʙᴀʙʏ🥀",
"ɴᴏʙᴏᴅʏ ᴋɴᴏᴡꜱ ᴛʜᴇ ᴛʀᴏᴜʙʟᴇꜱ ʏᴏᴜ ʜᴀᴠᴇ ꜱᴇᴇɴ ʙᴀʙʏ🥀",
"ʏᴏᴜ ʟᴏᴏᴋ ꜰᴀᴛ ʏᴏᴜ ꜱʜᴏᴜʟᴅ ᴇxᴇʀᴄɪꜱᴇ ᴍᴏʀᴇ ʙᴀʙʏ🥀",
"ꜰᴏʟʟᴏᴡ ᴛʜᴇ ᴢᴇʙʀᴀ ʙᴀʙʏ🥀",
"ᴡʜʏ ꜱᴏ ʙʟᴜᴇ? ʙᴀʙʏ🥀",
"ᴛʜᴇ ᴅᴇᴠɪʟ ɪɴ ᴅɪꜱɢᴜɪꜱᴇ ʙᴀʙʏ🥀",
"ɢᴏ ᴏᴜᴛꜱɪᴅᴇ ʙᴀʙʏ🥀",
"ᴀʟᴡᴀʏꜱ ʏᴏᴜʀ ʜᴇᴀᴅ ɪɴ ᴛʜᴇ ᴄʟᴏᴜᴅꜱ ʙᴀʙʏ🥀",
]


class Welcome(BASE):
    __tablename__ = "welcome_pref"
    chat_id = Column(String(14), primary_key=True)
    should_welcome = Column(Boolean, default=True)
    should_goodbye = Column(Boolean, default=True)
    custom_content = Column(UnicodeText, default=None)

    custom_welcome = Column(
        UnicodeText,
        default=random.choice(DEFAULT_WELCOME_MESSAGES),
    )
    welcome_type = Column(Integer, default=Types.TEXT.value)

    custom_leave = Column(UnicodeText, default=random.choice(DEFAULT_GOODBYE_MESSAGES))
    leave_type = Column(Integer, default=Types.TEXT.value)

    clean_welcome = Column(Integer)

    def __init__(self, chat_id, should_welcome=True, should_goodbye=True):
        self.chat_id = chat_id
        self.should_welcome = should_welcome
        self.should_goodbye = should_goodbye

    def __repr__(self):
        return "<Chat {} should Welcome new users: {}>".format(
            self.chat_id,
            self.should_welcome,
        )


class WelcomeButtons(BASE):
    __tablename__ = "welcome_urls"
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(String(14), primary_key=True)
    name = Column(UnicodeText, nullable=False)
    url = Column(UnicodeText, nullable=False)
    same_line = Column(Boolean, default=False)

    def __init__(self, chat_id, name, url, same_line=False):
        self.chat_id = str(chat_id)
        self.name = name
        self.url = url
        self.same_line = same_line


class GoodbyeButtons(BASE):
    __tablename__ = "leave_urls"
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(String(14), primary_key=True)
    name = Column(UnicodeText, nullable=False)
    url = Column(UnicodeText, nullable=False)
    same_line = Column(Boolean, default=False)

    def __init__(self, chat_id, name, url, same_line=False):
        self.chat_id = str(chat_id)
        self.name = name
        self.url = url
        self.same_line = same_line


class WelcomeMute(BASE):
    __tablename__ = "welcome_mutes"
    chat_id = Column(String(14), primary_key=True)
    welcomemutes = Column(UnicodeText, default=False)

    def __init__(self, chat_id, welcomemutes):
        self.chat_id = str(chat_id)  # ensure string
        self.welcomemutes = welcomemutes


class WelcomeMuteUsers(BASE):
    __tablename__ = "human_checks"
    user_id = Column(BigInteger, primary_key=True)
    chat_id = Column(String(14), primary_key=True)
    human_check = Column(Boolean)

    def __init__(self, user_id, chat_id, human_check):
        self.user_id = user_id  # ensure string
        self.chat_id = str(chat_id)
        self.human_check = human_check


class CleanServiceSetting(BASE):
    __tablename__ = "clean_service"
    chat_id = Column(String(14), primary_key=True)
    clean_service = Column(Boolean, default=True)

    def __init__(self, chat_id):
        self.chat_id = str(chat_id)

    def __repr__(self):
        return "<Chat used clean service ({})>".format(self.chat_id)


Welcome.__table__.create(checkfirst=True)
WelcomeButtons.__table__.create(checkfirst=True)
GoodbyeButtons.__table__.create(checkfirst=True)
WelcomeMute.__table__.create(checkfirst=True)
WelcomeMuteUsers.__table__.create(checkfirst=True)
CleanServiceSetting.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()
WELC_BTN_LOCK = threading.RLock()
LEAVE_BTN_LOCK = threading.RLock()
WM_LOCK = threading.RLock()
CS_LOCK = threading.RLock()


def welcome_mutes(chat_id):
    try:
        welcomemutes = SESSION.query(WelcomeMute).get(str(chat_id))
        if welcomemutes:
            return welcomemutes.welcomemutes
        return False
    finally:
        SESSION.close()


def set_welcome_mutes(chat_id, welcomemutes):
    with WM_LOCK:
        prev = SESSION.query(WelcomeMute).get((str(chat_id)))
        if prev:
            SESSION.delete(prev)
        welcome_m = WelcomeMute(str(chat_id), welcomemutes)
        SESSION.add(welcome_m)
        SESSION.commit()


def set_human_checks(user_id, chat_id):
    with INSERTION_LOCK:
        human_check = SESSION.query(WelcomeMuteUsers).get((user_id, str(chat_id)))
        if not human_check:
            human_check = WelcomeMuteUsers(user_id, str(chat_id), True)

        else:
            human_check.human_check = True

        SESSION.add(human_check)
        SESSION.commit()

        return human_check


def get_human_checks(user_id, chat_id):
    try:
        human_check = SESSION.query(WelcomeMuteUsers).get((user_id, str(chat_id)))
        if not human_check:
            return None
        human_check = human_check.human_check
        return human_check
    finally:
        SESSION.close()


def get_welc_mutes_pref(chat_id):
    welcomemutes = SESSION.query(WelcomeMute).get(str(chat_id))
    SESSION.close()

    if welcomemutes:
        return welcomemutes.welcomemutes

    return False


def get_welc_pref(chat_id):
    welc = SESSION.query(Welcome).get(str(chat_id))
    SESSION.close()
    if welc:
        return (
            welc.should_welcome,
            welc.custom_welcome,
            welc.custom_content,
            welc.welcome_type,
        )
    # Welcome by default.
    return True, random.choice(DEFAULT_WELCOME_MESSAGES), None, Types.TEXT


def get_gdbye_pref(chat_id):
    welc = SESSION.query(Welcome).get(str(chat_id))
    SESSION.close()
    if welc:
        return welc.should_goodbye, welc.custom_leave, welc.leave_type
    # Welcome by default.
    return True, random.choice(DEFAULT_GOODBYE_MESSAGES), Types.TEXT


def set_clean_welcome(chat_id, clean_welcome):
    with INSERTION_LOCK:
        curr = SESSION.query(Welcome).get(str(chat_id))
        if not curr:
            curr = Welcome(str(chat_id))

        curr.clean_welcome = int(clean_welcome)

        SESSION.add(curr)
        SESSION.commit()


def get_clean_pref(chat_id):
    welc = SESSION.query(Welcome).get(str(chat_id))
    SESSION.close()

    if welc:
        return welc.clean_welcome

    return False


def set_welc_preference(chat_id, should_welcome):
    with INSERTION_LOCK:
        curr = SESSION.query(Welcome).get(str(chat_id))
        if not curr:
            curr = Welcome(str(chat_id), should_welcome=should_welcome)
        else:
            curr.should_welcome = should_welcome

        SESSION.add(curr)
        SESSION.commit()


def set_gdbye_preference(chat_id, should_goodbye):
    with INSERTION_LOCK:
        curr = SESSION.query(Welcome).get(str(chat_id))
        if not curr:
            curr = Welcome(str(chat_id), should_goodbye=should_goodbye)
        else:
            curr.should_goodbye = should_goodbye

        SESSION.add(curr)
        SESSION.commit()


def set_custom_welcome(
    chat_id,
    custom_content,
    custom_welcome,
    welcome_type,
    buttons=None,
):
    if buttons is None:
        buttons = []

    with INSERTION_LOCK:
        welcome_settings = SESSION.query(Welcome).get(str(chat_id))
        if not welcome_settings:
            welcome_settings = Welcome(str(chat_id), True)

        if custom_welcome or custom_content:
            welcome_settings.custom_content = custom_content
            welcome_settings.custom_welcome = custom_welcome
            welcome_settings.welcome_type = welcome_type.value

        else:
            welcome_settings.custom_welcome = random.choice(DEFAULT_WELCOME_MESSAGES)
            welcome_settings.welcome_type = Types.TEXT.value

        SESSION.add(welcome_settings)

        with WELC_BTN_LOCK:
            prev_buttons = (
                SESSION.query(WelcomeButtons)
                .filter(WelcomeButtons.chat_id == str(chat_id))
                .all()
            )
            for btn in prev_buttons:
                SESSION.delete(btn)

            for b_name, url, same_line in buttons:
                button = WelcomeButtons(chat_id, b_name, url, same_line)
                SESSION.add(button)

        SESSION.commit()


def get_custom_welcome(chat_id):
    welcome_settings = SESSION.query(Welcome).get(str(chat_id))
    ret = random.choice(DEFAULT_WELCOME_MESSAGES)
    if welcome_settings and welcome_settings.custom_welcome:
        ret = welcome_settings.custom_welcome

    SESSION.close()
    return ret


def set_custom_gdbye(chat_id, custom_goodbye, goodbye_type, buttons=None):
    if buttons is None:
        buttons = []

    with INSERTION_LOCK:
        welcome_settings = SESSION.query(Welcome).get(str(chat_id))
        if not welcome_settings:
            welcome_settings = Welcome(str(chat_id), True)

        if custom_goodbye:
            welcome_settings.custom_leave = custom_goodbye
            welcome_settings.leave_type = goodbye_type.value

        else:
            welcome_settings.custom_leave = random.choice(DEFAULT_GOODBYE_MESSAGES)
            welcome_settings.leave_type = Types.TEXT.value

        SESSION.add(welcome_settings)

        with LEAVE_BTN_LOCK:
            prev_buttons = (
                SESSION.query(GoodbyeButtons)
                .filter(GoodbyeButtons.chat_id == str(chat_id))
                .all()
            )
            for btn in prev_buttons:
                SESSION.delete(btn)

            for b_name, url, same_line in buttons:
                button = GoodbyeButtons(chat_id, b_name, url, same_line)
                SESSION.add(button)

        SESSION.commit()


def get_custom_gdbye(chat_id):
    welcome_settings = SESSION.query(Welcome).get(str(chat_id))
    ret = random.choice(DEFAULT_GOODBYE_MESSAGES)
    if welcome_settings and welcome_settings.custom_leave:
        ret = welcome_settings.custom_leave

    SESSION.close()
    return ret


def get_welc_buttons(chat_id):
    try:
        return (
            SESSION.query(WelcomeButtons)
            .filter(WelcomeButtons.chat_id == str(chat_id))
            .order_by(WelcomeButtons.id)
            .all()
        )
    finally:
        SESSION.close()


def get_gdbye_buttons(chat_id):
    try:
        return (
            SESSION.query(GoodbyeButtons)
            .filter(GoodbyeButtons.chat_id == str(chat_id))
            .order_by(GoodbyeButtons.id)
            .all()
        )
    finally:
        SESSION.close()


def clean_service(chat_id: Union[str, int]) -> bool:
    try:
        chat_setting = SESSION.query(CleanServiceSetting).get(str(chat_id))
        if chat_setting:
            return chat_setting.clean_service
        return False
    finally:
        SESSION.close()


def set_clean_service(chat_id: Union[int, str], setting: bool):
    with CS_LOCK:
        chat_setting = SESSION.query(CleanServiceSetting).get(str(chat_id))
        if not chat_setting:
            chat_setting = CleanServiceSetting(chat_id)

        chat_setting.clean_service = setting
        SESSION.add(chat_setting)
        SESSION.commit()


def migrate_chat(old_chat_id, new_chat_id):
    with INSERTION_LOCK:
        chat = SESSION.query(Welcome).get(str(old_chat_id))
        if chat:
            chat.chat_id = str(new_chat_id)

        with WELC_BTN_LOCK:
            chat_buttons = (
                SESSION.query(WelcomeButtons)
                .filter(WelcomeButtons.chat_id == str(old_chat_id))
                .all()
            )
            for btn in chat_buttons:
                btn.chat_id = str(new_chat_id)

        with LEAVE_BTN_LOCK:
            chat_buttons = (
                SESSION.query(GoodbyeButtons)
                .filter(GoodbyeButtons.chat_id == str(old_chat_id))
                .all()
            )
            for btn in chat_buttons:
                btn.chat_id = str(new_chat_id)

        SESSION.commit()
