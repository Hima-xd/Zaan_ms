from pymongo import MongoClient
from telethon import *
from telethon.tl import *

from KRISTY import BOT_ID, MONGO_DB_URI
from KRISTY import telethn as tbot
from KRISTY.events import register

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["Fingapara2"]
approved_users = db.approve
dbb = client["Fingapara2"]
poll_id = dbb.pollid


async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):
        return isinstance(
            (
                await tbot(functions.channels.GetParticipantRequest(chat, user))
            ).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(chat, types.InputPeerChat):
        ui = await tbot.get_peer_id(user)
        ps = (
            await tbot(functions.messages.GetFullChatRequest(chat.chat_id))
        ).full_chat.participants.participants
        return isinstance(
            next((p for p in ps if p.user_id == ui), None),
            (types.ChatParticipantAdmin, types.ChatParticipantCreator),
        )
    return None


@register(pattern="^/poll (.*)")
async def _(event):
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch["id"]
        userss = ch["user"]
    if event.is_group:
        if await is_register_admin(event.input_chat, event.message.sender_id):
            pass
        elif event.chat_id == iid and event.sender_id == userss:
            pass
        else:
            return
    try:
        quew = event.pattern_match.group(1)
    except Exception:
        await event.reply("ᴡʜᴇʀᴇ ɪꜱ ᴛʜᴇ Qᴜᴇꜱᴛɪᴏɴ ʙᴀʙʏ🥀?")
        return
    if "|" in quew:
        secrets, quess, options = quew.split("|")
    secret = secrets.strip()

    if not secret:
        await event.reply("ɪ ɴᴇᴇᴅ ᴀ ᴘᴏʟʟ ɪᴅ ᴏꜰ 5 ᴅɪɢɪᴛꜱ ᴛᴏ ᴍᴀᴋᴇ ᴀ ᴘᴏʟʟ ʙᴀʙʏ🥀")
        return

    try:
        secret = str(secret)
    except ValueError:
        await event.reply("ᴘᴏʟʟ ɪᴅ ꜱʜᴏᴜʟᴅ ᴄᴏɴᴛᴀɪɴ ᴏɴʟʏ ɴᴜᴍʙᴇʀꜱ ʙᴀʙʏ🥀")
        return

    # print(secret)

    if len(secret) != 5:
        await event.reply("ᴘᴏʟʟ ɪᴅ ꜱʜᴏᴜʟᴅ ʙᴇ ᴀɴ ɪɴᴛᴇɢᴇʀ ᴏꜰ 5 ᴅɪɢɪᴛꜱ ʙᴀʙʏ🥀")
        return

    allpoll = poll_id.find({})
    # print(secret)
    for c in allpoll:
        if event.sender_id == c["user"]:
            await event.reply(
                "ᴘʟᴇᴀꜱᴇ ꜱᴛᴏᴘ ᴛʜᴇ ᴘʀᴇᴠɪᴏᴜꜱ ᴘᴏʟʟ ʙᴇꜰᴏʀᴇ ᴄʀᴇᴀᴛɪɴɢ ᴀ ɴᴇᴡ ᴏɴᴇ ʙᴀʙʏ🥀!"
            )
            return
    poll_id.insert_one({"user": event.sender_id, "pollid": secret})

    ques = quess.strip()
    option = options.strip()
    quiz = option.split(" ")[1 - 1]
    if "True" in quiz:
        quizy = True
        if "@" in quiz:
            one, two = quiz.split("@")
            rightone = two.strip()
        else:
            await event.reply(
                "ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ꜱᴇʟᴇᴄᴛ ᴛʜᴇ ʀɪɢʜᴛ ᴀɴꜱᴡᴇʀ ᴡɪᴛʜ Qᴜᴇꜱᴛɪᴏɴ ɴᴜᴍʙᴇʀ ʟɪᴋᴇ ᴛʀᴜᴇ@1, True@3 ᴇᴛᴄ ʙᴀʙʏ🥀..."
            )
            return

        quizoptionss = []
        try:
            ab = option.split(" ")[4 - 1]
            cd = option.split(" ")[5 - 1]
            quizoptionss.append(types.PollAnswer(ab, b"1"))
            quizoptionss.append(types.PollAnswer(cd, b"2"))
        except Exception:
            await event.reply("ᴀᴛ ʟᴇᴀꜱᴛ ɴᴇᴇᴅ ᴛᴡᴏ ᴏᴘᴛɪᴏɴꜱ ᴛᴏ ᴄʀᴇᴀᴛᴇ ᴀ ᴘᴏʟʟ ʙᴀʙʏ🥀")
            return
        try:
            ef = option.split(" ")[6 - 1]
            quizoptionss.append(types.PollAnswer(ef, b"3"))
        except Exception:
            ef = None
        try:
            gh = option.split(" ")[7 - 1]
            quizoptionss.append(types.PollAnswer(gh, b"4"))
        except Exception:
            gh = None
        try:
            ij = option.split(" ")[8 - 1]
            quizoptionss.append(types.PollAnswer(ij, b"5"))
        except Exception:
            ij = None
        try:
            kl = option.split(" ")[9 - 1]
            quizoptionss.append(types.PollAnswer(kl, b"6"))
        except Exception:
            kl = None
        try:
            mn = option.split(" ")[10 - 1]
            quizoptionss.append(types.PollAnswer(mn, b"7"))
        except Exception:
            mn = None
        try:
            op = option.split(" ")[11 - 1]
            quizoptionss.append(types.PollAnswer(op, b"8"))
        except Exception:
            op = None
        try:
            qr = option.split(" ")[12 - 1]
            quizoptionss.append(types.PollAnswer(qr, b"9"))
        except Exception:
            qr = None
        try:
            st = option.split(" ")[13 - 1]
            quizoptionss.append(types.PollAnswer(st, b"10"))
        except Exception:
            st = None

    elif "False" in quiz:
        quizy = False
    else:
        await event.reply("ᴡʀᴏɴɢ ᴀʀɢᴜᴍᴇɴᴛꜱ ᴘʀᴏᴠɪᴅᴇᴅ ʙᴀʙʏ🥀!")
        return

    pvote = option.split(" ")[2 - 1]
    if "True" in pvote:
        pvoty = True
    elif "False" in pvote:
        pvoty = False
    else:
        await event.reply("ᴡʀᴏɴɢ ᴀʀɢᴜᴍᴇɴᴛꜱ ᴘʀᴏᴠɪᴅᴇᴅ ʙᴀʙʏ🥀!")
        return
    mchoice = option.split(" ")[3 - 1]
    if "True" in mchoice:
        mchoicee = True
    elif "False" in mchoice:
        mchoicee = False
    else:
        await event.reply("ᴡʀᴏɴɢ ᴀʀɢᴜᴍᴇɴᴛꜱ ᴘʀᴏᴠɪᴅᴇᴅ ʙᴀʙʏ🥀!")
        return
    optionss = []
    try:
        ab = option.split(" ")[4 - 1]
        cd = option.split(" ")[5 - 1]
        optionss.append(types.PollAnswer(ab, b"1"))
        optionss.append(types.PollAnswer(cd, b"2"))
    except Exception:
        await event.reply("ᴀᴛ ʟᴇᴀꜱᴛ ɴᴇᴇᴅ ᴛᴡᴏ ᴏᴘᴛɪᴏɴꜱ ᴛᴏ ᴄʀᴇᴀᴛᴇ ᴀ ᴘᴏʟʟ ʙᴀʙʏ🥀")
        return
    try:
        ef = option.split(" ")[6 - 1]
        optionss.append(types.PollAnswer(ef, b"3"))
    except Exception:
        ef = None
    try:
        gh = option.split(" ")[7 - 1]
        optionss.append(types.PollAnswer(gh, b"4"))
    except Exception:
        gh = None
    try:
        ij = option.split(" ")[8 - 1]
        optionss.append(types.PollAnswer(ij, b"5"))
    except Exception:
        ij = None
    try:
        kl = option.split(" ")[9 - 1]
        optionss.append(types.PollAnswer(kl, b"6"))
    except Exception:
        kl = None
    try:
        mn = option.split(" ")[10 - 1]
        optionss.append(types.PollAnswer(mn, b"7"))
    except Exception:
        mn = None
    try:
        op = option.split(" ")[11 - 1]
        optionss.append(types.PollAnswer(op, b"8"))
    except Exception:
        op = None
    try:
        qr = option.split(" ")[12 - 1]
        optionss.append(types.PollAnswer(qr, b"9"))
    except Exception:
        qr = None
    try:
        st = option.split(" ")[13 - 1]
        optionss.append(types.PollAnswer(st, b"10"))
    except Exception:
        st = None

    if pvoty is False and quizy is False and mchoicee is False:
        await tbot.send_file(
            event.chat_id,
            types.InputMediaPoll(
                poll=types.Poll(id=12345, question=ques, answers=optionss, quiz=False)
            ),
        )

    if pvoty is True and quizy is False and mchoicee is True:
        await tbot.send_file(
            event.chat_id,
            types.InputMediaPoll(
                poll=types.Poll(
                    id=12345,
                    question=ques,
                    answers=optionss,
                    quiz=False,
                    multiple_choice=True,
                    public_voters=True,
                )
            ),
        )

    if pvoty is False and quizy is False and mchoicee is True:
        await tbot.send_file(
            event.chat_id,
            types.InputMediaPoll(
                poll=types.Poll(
                    id=12345,
                    question=ques,
                    answers=optionss,
                    quiz=False,
                    multiple_choice=True,
                    public_voters=False,
                )
            ),
        )

    if pvoty is True and quizy is False and mchoicee is False:
        await tbot.send_file(
            event.chat_id,
            types.InputMediaPoll(
                poll=types.Poll(
                    id=12345,
                    question=ques,
                    answers=optionss,
                    quiz=False,
                    multiple_choice=False,
                    public_voters=True,
                )
            ),
        )

    if pvoty is False and quizy is True and mchoicee is False:
        await tbot.send_file(
            event.chat_id,
            types.InputMediaPoll(
                poll=types.Poll(
                    id=12345, question=ques, answers=quizoptionss, quiz=True
                ),
                correct_answers=[f"{rightone}"],
            ),
        )

    if pvoty is True and quizy is True and mchoicee is False:
        await tbot.send_file(
            event.chat_id,
            types.InputMediaPoll(
                poll=types.Poll(
                    id=12345,
                    question=ques,
                    answers=quizoptionss,
                    quiz=True,
                    public_voters=True,
                ),
                correct_answers=[f"{rightone}"],
            ),
        )

    if pvoty is True and quizy is True and mchoicee is True:
        await event.reply("ʏᴏᴜ ᴄᴀɴ'ᴛ ᴜꜱᴇ ᴍᴜʟᴛɪᴘʟᴇ ᴠᴏᴛɪɴɢ ᴡɪᴛʜ Qᴜɪᴢ ᴍᴏᴅᴇ ʙᴀʙʏ🥀")
        return
    if pvoty is False and quizy is True and mchoicee is True:
        await event.reply("ʏᴏᴜ ᴄᴀɴ'ᴛ ᴜꜱᴇ ᴍᴜʟᴛɪᴘʟᴇ ᴠᴏᴛɪɴɢ ᴡɪᴛʜ Qᴜɪᴢ ᴍᴏᴅᴇ ʙᴀʙʏ🥀")
        return


@register(pattern="^/stoppoll(?: |$)(.*)")
async def stop(event):
    secret = event.pattern_match.group(1)
    # print(secret)
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch["id"]
        userss = ch["user"]
    if event.is_group:
        if await is_register_admin(event.input_chat, event.message.sender_id):
            pass
        elif event.chat_id == iid and event.sender_id == userss:
            pass
        else:
            return

    if not event.reply_to_msg_id:
        await event.reply("ᴘʟᴇᴀꜱᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴘᴏʟʟ ᴛᴏ ꜱᴛᴏᴘ ɪᴛ ʙᴀʙʏ🥀")
        return

    if input is None:
        await event.reply("ᴡʜᴇʀᴇ ɪꜱ ᴛʜᴇ ᴘᴏʟʟ ɪᴅ ʙᴀʙʏ🥀?")
        return

    try:
        secret = str(secret)
    except ValueError:
        await event.reply("ᴘᴏʟʟ ɪᴅ ꜱʜᴏᴜʟᴅ ᴄᴏɴᴛᴀɪɴ ᴏɴʟʏ ɴᴜᴍʙᴇʀꜱ ʙᴀʙʏ🥀")
        return

    if len(secret) != 5:
        await event.reply("ᴘᴏʟʟ ɪᴅ ꜱʜᴏᴜʟᴅ ʙᴇ ᴀɴ ɪɴᴛᴇɢᴇʀ ᴏꜰ 5 ᴅɪɢɪᴛꜱ ʙᴀʙʏ🥀")
        return

    msg = await event.get_reply_message()

    if str(msg.sender_id) != str(BOT_ID):
        await event.reply(
            "ɪ ᴄᴀɴ'ᴛ ᴅᴏ ᴛʜɪꜱ ᴏᴘᴇʀᴀᴛɪᴏɴ ᴏɴ ᴛʜɪꜱ ᴘᴏʟʟ.\nᴘʀᴏʙᴀʙʟʏ ɪᴛ'ꜱ ɴᴏᴛ ᴄʀᴇᴀᴛᴇᴅ ʙʏ ᴍᴇ ʙᴀʙʏ🥀"
        )
        return
    print(secret)
    if msg.poll:
        allpoll = poll_id.find({})
        for c in allpoll:
            if not event.sender_id == c["user"] and not secret == c["pollid"]:
                await event.reply(
                    "ᴏᴏᴘꜱ, ᴇɪᴛʜᴇʀ ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ ᴄʀᴇᴀᴛᴇᴅ ᴛʜɪꜱ ᴘᴏʟʟ ᴏʀ ʏᴏᴜ ʜᴀᴠᴇ ɢɪᴠᴇɴ ᴡʀᴏɴɢ ᴘᴏʟʟ ɪᴅ ʙᴀʙʏ🥀"
                )
                return
        if msg.poll.poll.closed:
            await event.reply("ᴏᴏᴘꜱ, ᴛʜᴇ ᴘᴏʟʟ ɪꜱ ᴀʟʀᴇᴀᴅʏ ᴄʟᴏꜱᴇᴅ ʙᴀʙʏ🥀.")
            return
        poll_id.delete_one({"user": event.sender_id})
        pollid = msg.poll.poll.id
        await msg.edit(
            file=types.InputMediaPoll(
                poll=types.Poll(id=pollid, question="", answers=[], closed=True)
            )
        )
        await event.reply("ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ꜱᴛᴏᴘᴘᴇᴅ ᴛʜᴇ ᴘᴏʟʟ ʙᴀʙʏ🥀")
    else:
        await event.reply("ᴛʜɪꜱ ɪꜱɴ'ᴛ ᴀ ᴘᴏʟʟ ʙᴀʙʏ🥀")


@register(pattern="^/forgotpollid$")
async def stop(event):
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch["id"]
        userss = ch["user"]
    if event.is_group:
        if await is_register_admin(event.input_chat, event.message.sender_id):
            pass
        elif event.chat_id == iid and event.sender_id == userss:
            pass
        else:
            return
    allpoll = poll_id.find({})
    for c in allpoll:
        if event.sender_id == c["user"]:
            try:
                poll_id.delete_one({"user": event.sender_id})
                await event.reply("ᴅᴏɴᴇ ʏᴏᴜ ᴄᴀɴ ɴᴏᴡ ᴄʀᴇᴀᴛᴇ ᴀ ɴᴇᴡ ᴘᴏʟʟ ʙᴀʙʏ🥀.")
            except Exception:
                await event.reply("ꜱᴇᴇᴍꜱ ʟɪᴋᴇ ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ ᴄʀᴇᴀᴛᴇᴅ ᴀɴʏ ᴘᴏʟʟ ʏᴇᴛ ʙᴀʙʏ🥀!")


__help__ = """
» ᴘᴏʟʟ-ɪᴅ - ᴀ ᴘᴏʟʟ ɪᴅ ᴄᴏɴꜱɪꜱᴛꜱ ᴏꜰ ᴀɴ 5 ᴅɪɢɪᴛ ʀᴀɴᴅᴏᴍ ɪɴᴛᴇɢᴇʀ, ᴛʜɪꜱ ɪᴅ ɪꜱ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ʀᴇᴍᴏᴠᴇᴅ ꜰʀᴏᴍ ᴛʜᴇ ꜱʏꜱᴛᴇᴍ ᴡʜᴇɴ ʏᴏᴜ ꜱᴛᴏᴘ ʏᴏᴜʀ ᴘʀᴇᴠɪᴏᴜꜱ ᴘᴏʟʟ 
» Qᴜᴇꜱᴛɪᴏɴ - ᴛʜᴇ Qᴜᴇꜱᴛɪᴏɴ ʏᴏᴜ ᴡᴀɴɴᴀ ᴀꜱᴋ 
» <ᴛʀᴜᴇ@ᴏᴘᴛɪᴏɴɴᴜᴍʙᴇʀ/ꜰᴀʟꜱᴇ>(1) - Qᴜɪᴢ ᴍᴏᴅᴇ, ʏᴏᴜ ᴍᴜꜱᴛ ꜱᴛᴀᴛᴇ ᴛʜᴇ ᴄᴏʀʀᴇᴄᴛ ᴀɴꜱᴡᴇʀ ᴡɪᴛʜ `@` ᴇɢ: `ᴛʀᴜᴇ@1` ᴏʀ `ᴛʀᴜᴇ@2` 
» <ᴛʀᴜᴇ/ꜰᴀʟꜱᴇ>(2) - ᴘᴜʙʟɪᴄ ᴠᴏᴛᴇꜱ » <ᴛʀᴜᴇ/ꜰᴀʟꜱᴇ>(3) - ᴍᴜʟᴛɪᴘʟᴇ ᴄʜᴏɪᴄᴇ
**ꜱʏɴᴛᴀx** -
» `/poll <ᴘᴏʟʟ-ɪᴅ> <Qᴜᴇꜱᴛɪᴏɴ> | <ᴛʀᴜᴇ@ᴏᴘᴛɪᴏɴɴᴜᴍʙᴇʀ/ꜰᴀʟꜱᴇ> <ᴛʀᴜᴇ/ꜰᴀʟꜱᴇ> <ᴛʀᴜᴇ/ꜰᴀʟꜱᴇ> <ᴏᴘᴛɪᴏɴ1> <ᴏᴘᴛɪᴏɴ2> ... ᴜᴘᴛᴏ <ᴏᴘᴛɪᴏɴ10>`
**ᴇxᴀᴍᴘʟᴇꜱ** -
» `/poll 12345 | ᴀᴍ ɪ ᴄᴏᴏʟ? | ꜰᴀʟꜱᴇ ꜰᴀʟꜱᴇ ꜰᴀʟꜱᴇ ʏᴇꜱ ɴᴏ`
» `/poll 12345 | ᴀᴍ ɪ ᴄᴏᴏʟ? | ᴛʀᴜᴇ@1 ꜰᴀʟꜱᴇ ꜰᴀʟꜱᴇ ʏᴇꜱ ɴᴏ`
**ᴛᴏ ꜱᴛᴏᴘ ᴀ ᴘᴏʟʟ**
ʀᴇᴘʟʏ ᴛᴏ ᴛʜᴇ ᴘᴏʟʟ ᴡɪᴛʜ `/stoppoll <ᴘᴏʟʟ-ɪᴅ>` ᴛᴏ ꜱᴛᴏᴘ ᴛʜᴇ ᴘᴏʟʟ**ɴᴏᴛᴇ**
ɪꜰ ʏᴏᴜ ʜᴀᴠᴇ ꜰᴏʀɢᴏᴛᴛᴇɴ ʏᴏᴜʀ ᴘᴏʟʟ ɪᴅ ᴏʀ ᴅᴇʟᴇᴛᴇᴅ ᴛʜᴇ ᴘᴏʟʟ ꜱᴏ ᴛʜᴀᴛ ʏᴏᴜ ᴄᴀɴ'ᴛ ꜱᴛᴏᴘ ᴛʜᴇ ᴘʀᴇᴠɪᴏᴜꜱ ᴘᴏʟʟ ᴛʏᴘᴇ `/forgotpollid`, ᴛʜɪꜱ ᴡɪʟʟ ʀᴇꜱᴇᴛ ᴛʜᴇ ᴘᴏʟʟ ɪᴅ, ʏᴏᴜ ᴡɪʟʟ ʜᴀᴠᴇ ɴᴏ ᴀᴄᴄᴇꜱꜱ ᴛᴏ ᴛʜᴇ ᴘʀᴇᴠɪᴏᴜꜱ ᴘᴏʟʟ!
"""


__mod_name__ = "POLLING"
