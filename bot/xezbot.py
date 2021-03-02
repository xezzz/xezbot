from core import config
import asyncio

from irc.bot import SingleServerIRCBot
import requests as r

from core import commands, automod
from utils import api, black_list
from database import connector, models



class xezbot(SingleServerIRCBot):
    def __init__(self):
        self.HOST = "irc.chat.twitch.tv"
        self.PORT = 6667
        self.USERNAME = "xezbot"
        self.CLIENT_ID = config.CLIENT_ID
        self.CLIENT_SECRET = config.CLIENT_SECRET
        self.TOKEN = config.TOKEN
        self.database = connector.Database()
        self.twitch_channels = [f"#{x}" for x in self.database.channels.find()[0]["channels"]]
        self.api_cache = asyncio.run(api.get_bearer_token(self, self.CLIENT_ID, self.CLIENT_SECRET))
        self.spam_bucket = dict()


        for t in self.twitch_channels:
            if not self.database.get(self.database.configs, "channel", f"{t}", "black_list"):
                self.database.insert(self.database.configs, models.channel_model(t, black_list.default_black_list))
            else:
                pass

        self.database.update(self.database.channels, "ac", "123", "bearer", f"{self.api_cache['access_token']}")


        url = "https://api.twitch.tv/kraken/users?login={}".format(self.USERNAME)
        headers = {
            "Client-ID": self.CLIENT_ID,
            "Accept": "application/vnd.twitchtv.v5+json"
        }
        res = r.get(url=url, headers=headers).json()
        self.channel_id = res["users"][0]["_id"]


        super().__init__([(self.HOST, self.PORT, f"oauth:{self.TOKEN}")], self.USERNAME, self.USERNAME)


    def on_welcome(self, cxn, event):
        for req in ("membership", "tags", "commands"):
            cxn.cap("REQ", ":twitch.tv/{}".format(req))
        
        for channel in self.twitch_channels:
            cxn.join(channel)
            print("Ich bin dem Kanal {} beigetreten!".format(channel))




    def on_pubmsg(self, cxn, event):
        tags = {
            k["key"]: k["value"] for k in event.tags
        }
        user = {
            "name": tags["display-name"].lower(),
            "id": tags["user-id"],
            "mod": tags["mod"],
            "sub": tags["subscriber"]
        }
        channel = event.target
        message = event.arguments[0]
        msg_id = tags["id"]

        if user["name"] != self.USERNAME and user["mod"] == "0" and user["name"] != channel.split("#")[1].lower():
            automod.process(self, user, channel, message, msg_id)
            commands.process_normal(self, user, channel, message)
        
        if user["name"] != self.USERNAME and user["mod"] > "0" or user["name"] == channel.split("#")[1].lower():
            commands.process_mod(self, user, channel, message)


    def send_message(self, channel, message):
        self.connection.privmsg(channel, message)