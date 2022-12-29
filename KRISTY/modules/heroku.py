import asyncio
import math
import os

import heroku3
import requests

from KRISTY import telethn as borg, HEROKU_APP_NAME, HEROKU_API_KEY, OWNER_ID
from KRISTY.events import register

heroku_api = "https://api.heroku.com"
Heroku = heroku3.from_key(HEROKU_API_KEY)


@register(pattern="^/(set|see|del) var(?: |$)(.*)(?: |$)([\s\S]*)")
async def variable(var):
    if var.fwd_from:
        return
    if var.sender_id == OWNER_ID:
        pass
    else:
        return
    """
    Manage most of ConfigVars setting, set new var, get current var,
    or delete var...
    """
    if HEROKU_APP_NAME is not None:
        app = Heroku.app(HEROKU_APP_NAME)
    else:
        return await var.reply("`[HEROKU]:" "\nᴘʟᴇᴀꜱᴇ ꜱᴇᴛᴜᴘ ʏᴏᴜʀ` **HEROKU_APP_NAME** ʙᴀʙʏ🥀")
    exe = var.pattern_match.group(1)
    heroku_var = app.config()
    if exe == "see":
        k = await var.reply("`ɢᴇᴛᴛɪɴɢ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ ʙᴀʙʏ🥀...`")
        await asyncio.sleep(1.5)
        try:
            variable = var.pattern_match.group(2).split()[0]
            if variable in heroku_var:
                return await k.edit(
                    "**ᴄᴏɴꜰɪɢᴠᴀʀꜱ**:" f"\n\n`{variable} = {heroku_var[variable]}`\n"
                )
            else:
                return await k.edit(
                    "**ᴄᴏɴꜰɪɢᴠᴀʀꜱ**:" f"\n\n`ᴇʀʀᴏʀ:\n-> {variable} ᴅᴏɴ'ᴛ ᴇxɪꜱᴛꜱ ʙᴀʙʏ🥀`"
                )
        except IndexError:
            configs = prettyjson(heroku_var.to_dict(), indent=2)
            with open("configs.json", "w") as fp:
                fp.write(configs)
            with open("configs.json", "r") as fp:
                result = fp.read()
                if len(result) >= 4096:
                    await var.client.send_file(
                        var.chat_id,
                        "configs.json",
                        reply_to=var.id,
                        caption="`ᴏᴜᴛᴘᴜᴛ ᴛᴏᴏ ʟᴀʀɢᴇ, ꜱᴇɴᴅɪɴɢ ɪᴛ ᴀꜱ ᴀ ꜰɪʟᴇ ʙᴀʙʏ🥀`",
                    )
                else:
                    await k.edit(
                        "`[HEROKU]` ᴄᴏɴꜰɪɢᴠᴀʀꜱ:\n\n"
                        "================================"
                        f"\n```{result}```\n"
                        "================================"
                    )
            os.remove("configs.json")
            return
    elif exe == "set":
        s = await var.reply("`ꜱᴇᴛᴛɪɴɢ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ...ᴡᴀɪᴛ ʙᴀʙʏ🥀`")
        variable = var.pattern_match.group(2)
        if not variable:
            return await s.edit(">`.ꜱᴇᴛ ᴠᴀʀ <ᴄᴏɴꜰɪɢᴠᴀʀꜱ-ɴᴀᴍᴇ> <ᴠᴀʟᴜᴇ> ʙᴀʙʏ🥀`")
        value = var.pattern_match.group(3)
        if not value:
            variable = variable.split()[0]
            try:
                value = var.pattern_match.group(2).split()[1]
            except IndexError:
                return await s.edit(">`/set var <ᴄᴏɴꜰɪɢᴠᴀʀꜱ-ɴᴀᴍᴇ> <ᴠᴀʟᴜᴇ> ʙᴀʙʏ🥀`")
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await s.edit(
                f"**{variable}**  `ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴄʜᴀɴɢᴇᴅ ᴛᴏ`  ->  **{value}** ʙᴀʙʏ🥀"
            )
        else:
            await s.edit(
                f"**{variable}**  `ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴀᴅᴅᴇᴅ ᴡɪᴛʜ ᴠᴀʟᴜᴇ`  ->  **{value}** ʙᴀʙʏ🥀"
            )
        heroku_var[variable] = value
    elif exe == "del":
        m = await var.edit("`ɢᴇᴛᴛɪɴɢ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ ᴛᴏ ᴅᴇʟᴇᴛɪɴɢ ᴠᴀʀɪᴀʙʟᴇ ʙᴀʙʏ🥀...`")
        try:
            variable = var.pattern_match.group(2).split()[0]
        except IndexError:
            return await m.edit("`ᴘʟᴇᴀꜱᴇ ꜱᴘᴇᴄɪꜰʏ ᴄᴏɴꜰɪɢᴠᴀʀꜱ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴇʟᴇᴛᴇ ʙᴀʙʏ🥀`")
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await m.edit(f"**{variable}**  `ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ ʙᴀʙʏ🥀`")
            del heroku_var[variable]
        else:
            return await m.edit(f"**{variable}**  `ɪꜱ ɴᴏᴛ ᴇxɪꜱᴛꜱ ʙᴀʙʏ🥀`")


@register(pattern="^/usage(?: |$)")
async def dyno_usage(dyno):
    if dyno.fwd_from:
        return
    if dyno.sender_id == OWNER_ID:
        pass
    else:
        return
    """
    Get your account Dyno Usage
    """
    die = await dyno.reply("**ᴘʀᴏᴄᴇꜱꜱɪɴɢ...**")
    useragent = (
        "Mozilla/5.0 (Linux; Android 10; SM-G975F) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/80.0.3987.149 Mobile Safari/537.36"
    )
    user_id = Heroku.account().id
    headers = {
        "User-Agent": useragent,
        "Authorization": f"Bearer {HEROKU_API_KEY}",
        "Accept": "application/vnd.heroku+json; version=3.account-quotas",
    }
    path = "/accounts/" + user_id + "/actions/get-quota"
    r = requests.get(heroku_api + path, headers=headers)
    if r.status_code != 200:
        return await die.edit(
            "`ᴇʀʀᴏʀ: ꜱᴏᴍᴇᴛʜɪɴɢ ʙᴀᴅ ʜᴀᴘᴘᴇɴᴇᴅ`\n\n" f">.`{r.reason}`\n"
        )
    result = r.json()
    quota = result["account_quota"]
    quota_used = result["quota_used"]

    """ - Used - """
    remaining_quota = quota - quota_used
    percentage = math.floor(remaining_quota / quota * 100)
    minutes_remaining = remaining_quota / 60
    hours = math.floor(minutes_remaining / 60)
    minutes = math.floor(minutes_remaining % 60)

    """ - Current - """
    App = result["apps"]
    try:
        App[0]["quota_used"]
    except IndexError:
        AppQuotaUsed = 0
        AppPercentage = 0
    else:
        AppQuotaUsed = App[0]["quota_used"] / 60
        AppPercentage = math.floor(App[0]["quota_used"] * 100 / quota)
    AppHours = math.floor(AppQuotaUsed / 60)
    AppMinutes = math.floor(AppQuotaUsed % 60)

    await asyncio.sleep(1.5)

    return await die.edit(
        "**ᴅʏɴᴏ ᴜꜱᴀɢᴇ**:\n\n"
        f" -> `ᴅʏɴᴏ ᴜꜱᴀɢᴇ ꜰᴏʀ`  **{HEROKU_APP_NAME}**:\n"
        f"     •  `{AppHours}`**h**  `{AppMinutes}`**m**  "
        f"**|**  [`{AppPercentage}`**%**] ʙᴀʙʏ🥀"
        "\n\n"
        " -> `ᴅʏɴᴏ ʜᴏᴜʀꜱ Qᴜᴏᴛᴀ ʀᴇᴍᴀɪɴɪɴɢ ᴛʜɪꜱ ᴍᴏɴᴛʜ`:\n"
        f"     •  `{hours}`**h**  `{minutes}`**m**  "
        f"**|**  [`{percentage}`**%**] ʙᴀʙʏ🥀"
    )


@register(pattern="^/logs$")
async def _(dyno):
    if dyno.fwd_from:
        return
    if dyno.sender_id == OWNER_ID:
        pass
    else:
        return
    try:
        Heroku = heroku3.from_key(HEROKU_API_KEY)
        app = Heroku.app(HEROKU_APP_NAME)
    except:
        return await dyno.reply(
            " ᴘʟᴇᴀꜱᴇ ᴍᴀᴋᴇ ꜱᴜʀᴇ ʏᴏᴜʀ ʜᴇʀᴏᴋᴜ ᴀᴘɪ ᴋᴇʏ, ʏᴏᴜʀ ᴀᴘᴘ ɴᴀᴍᴇ ᴀʀᴇ ᴄᴏɴꜰɪɢᴜʀᴇᴅ ᴄᴏʀʀᴇᴄᴛʟʏ ɪɴ ᴛʜᴇ ʜᴇʀᴏᴋᴜ ʙᴀʙʏ🥀"
        )
    v = await dyno.reply("ɢᴇᴛᴛɪɴɢ ʟᴏɢꜱ ʙᴀʙʏ🥀...")
    with open("logs.txt", "w") as log:
        log.write(app.get_log())
    await v.edit("ɢᴏᴛ ᴛʜᴇ ʟᴏɢꜱ ᴡᴀɪᴛ ᴀ ꜱᴇᴄ ʙᴀʙʏ🥀")
    await dyno.client.send_file(
        dyno.chat_id,
        "logs.txt",
        reply_to=dyno.id,
        caption="KRISTY Logs.",
    )

    await asyncio.sleep(5)
    await v.delete()
    return os.remove("logs.txt")


def prettyjson(obj, indent=2, maxlinelength=80):
    """Renders JSON content with indentation and line splits/concatenations to fit maxlinelength.
    Only dicts, lists and basic types are supported"""

    items, _ = getsubitems(
        obj,
        itemkey="",
        islast=True,
        maxlinelength=maxlinelength - indent,
        indent=indent,
    )
    return indentitems(items, indent, level=0)
