from time import time

from . import misc, custom, censor
from database import connector


db = connector.Database()


PREFIX = "!"

normal_cmds = {
    "accountage": misc.accountage,
    "followage": misc.followage,
    "commands": custom.commands,
}

mod_cmds = {
    "add": custom.add,
    "remove": custom.remove,

    "add_word": censor.add_word,
    "remove_word": censor.remove_word,
    "black_list": censor.black_list
}

all_commands = {**normal_cmds, **mod_cmds}


def process_normal(bot, user, channel, message):
    if message.startswith(PREFIX):
        cmd = message.split(" ")[0][len(PREFIX):]
        args = message.split(" ")[1:]
        perform_normal(bot, user, channel, cmd, *args)


def process_mod(bot, user, channel, message):
    if message.startswith(PREFIX):
        cmd = message.split(" ")[0][len(PREFIX):]
        args = message.split(" ")[1:]
        perform_mod(bot, user, channel, cmd, *args)



def perform_normal(bot, user, channel, cmd, *args):
    if cmd in [x for x, y in mod_cmds.items()]:
        bot.send_message(channel, "NotLikeThis Sorry, aber das ist ein Mod-Only Command.")

    for name, func in normal_cmds.items():
        if cmd == name:
            func(bot, user, channel, *args)
        else:
            pass

    if cmd == "help":
        misc.help(bot, PREFIX, channel, all_commands)

    custom_id = f"{cmd}-{channel}"
    reply = db.get(db.commands, "command_id", custom_id, "reply")
    if reply is not None:
        bot.send_message(channel, f"{reply}")
    else:
        return


def perform_mod(bot, user, channel, cmd, *args):

    for name, func in all_commands.items():
        if cmd == name:
            if cmd != "add" or cmd != "remove":
                func(bot, user, channel, *args)
            else:
                pass
        
    if cmd == "help":
        misc.help(bot, PREFIX, channel, all_commands)

    custom_id = f"{cmd}-{channel}"
    reply = db.get(db.commands, "command_id", custom_id, "reply")
    if reply is not None:
        bot.send_message(channel, f"{reply}")
    else:
        return