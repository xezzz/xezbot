from datetime import datetime

from database import connector, models



db = connector.Database()



def add(bot, user, channel, *args):
    args = list(args)
    if 2 > len(args) < 120:
        return bot.send_message(channel, "Jebaited Hey, ich brauche einen Namen & einen Text den ich als Antwort (max 120 wörter) schicke, um einen Custom Command zu registrieren.")
    
    trigger = args[0].lower()
    reply = " ".join(args[1:])

    cmd_id = f"{trigger}-{channel}"
    if db.get(db.commands, "command_id", cmd_id, "reply") is not None:
        return bot.send_message(channel, "Jebaited Ein Command mit diesem Namen existiert bereits.")

    db.insert(db.commands, models.command_model(cmd_id, reply, user["name"], datetime.utcnow()))
    bot.send_message(channel, "SeemsGood Command {} wurde hinzugefügt. Du kannst ihn mit !{} ausprobieren.".format(trigger, trigger))



def remove(bot, user, channel, *args):
    args = list(args)
    if len(args) != 1:
        return bot.send_message(channel, "Jebaited Dieser Command braucht 1 Parameter (den Namen vom Custom Cmd, der gelöscht werden soll)")
    
    cmd_id = f"{args[0].lower()}-{channel}"
    if db.get(db.commands, "command_id", cmd_id, "reply") is None:
        return bot.send_message(channel, "Jebaited Ich kann keinen Command mit diesem Namen finden.")

    db.delete(db.commands, "command_id", cmd_id)
    bot.send_message(channel, "SeemsGood Command {} wurde entfernt!".format(args[0].lower()))



def commands(bot, user, channel, *args):
    cmds = [f"!{x['command_id'].split('-')[0]}" for x in db.commands.find() if x['command_id'].split("-")[1] == channel]
    if len(cmds) < 1:
        return bot.send_message(channel, "Jebaited Dieser Kanal hat noch keine Custom Commands. Füge einen mit !add <name> <antwort> hinzu.")
    
    bot.send_message(channel, "Custom Commands für {}: {}".format(channel.split("#")[1], ", ".join(cmds)))