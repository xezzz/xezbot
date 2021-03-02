import datetime
import requests as r
from utils import api
import asyncio

def help(bot, prefix, channel, cmds):
    bot.send_message(channel, "GlitchCat Command List: " + f", ".join([f"{prefix}{cmd}" for cmd in sorted(cmds.keys())]))



def accountage(bot, user, channel, *args):
    raw = r.get(
        url="https://api.twitch.tv/helix/users?id={}".format(user["id"]),
        headers={
            "Authorization": "Bearer {}".format(bot.api_cache["access_token"]),
            "Client-Id": bot.CLIENT_ID
        }
    ).json()["data"][0]["created_at"].split("T")[0]

    fmt = "%Y-%m-%d"
    created = datetime.datetime.strptime(raw, fmt)
    now = datetime.datetime.strptime(datetime.datetime.utcnow().strftime(fmt), fmt)
    ago = (now - created).days

    bot.send_message(channel, "GlitchCat Account erstellt am {} ({} Tage her)".format(created.strftime("%d/%m/%Y"), ago))


def followage(bot, user, channel, *args):
    headers = {
        "Authorization": "Bearer {}".format(bot.api_cache["access_token"]),
        "Client-Id": bot.CLIENT_ID
    }
    channel_id = r.get("https://api.twitch.tv/helix/users?login={}".format(channel.split('#')[1]), headers=headers).json()["data"][0]["id"]
    raw = r.get(
        url="https://api.twitch.tv/helix/users/follows?from_id={}&to_id={}".format(user["id"], channel_id), 
        headers=headers
    ).json()["data"]

    if not channel.split("#")[1].lower() in [str(x["to_name"]).lower() for x in raw]:
        return bot.send_message(channel, "Jebaited Du folgst {} nicht.".format(channel.split("#")[1]))

    else:
        raw_followed = raw[raw.index([x for x in raw if x["to_login"] == channel.split("#")[1]][0])]["followed_at"].split("T")[0]

        fmt = "%Y-%m-%d"
        followed = datetime.datetime.strptime(raw_followed, fmt)
        now = datetime.datetime.strptime(datetime.datetime.utcnow().strftime(fmt), fmt)
        ago = (now - followed).days
        bot.send_message(channel, "GlitchCat Du bist ein Follower seit dem {} ({} Tage her)".format(followed.strftime("%d/%m/%Y"), ago))

