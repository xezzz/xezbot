from database import connector, models


db = connector.Database()



def add_word(bot, user, channel, *args):
    args = list(args)
    if 1 > len(args):
        return bot.send_message(channel, "Jebaited Was für ein Wort/einen Satz soll ich denn jetzt hinzufügen?")
    if 20 < len(args):
        return bot.send_message(channel, "Jebaited Der Satz ist ein wenig zu lang (Max 20 Wörter)")
    
    phrase = " ".join(args)
    current = [x.strip().lower() for x in db.get(db.configs, "channel", f"{channel}", "black_list")]
    if phrase.lower() in current:
        return bot.send_message(channel, "Jebaited Das Wort/der Satz ist bereits auf der Black List.")
    
    current.append(phrase.lower())
    db.update(db.configs, "channel", f"{channel}", "black_list", current)
    bot.send_message(channel, "SeemsGood Alles klar, ich habe das Wort/den Satz zur Black List hinzugefügt!")


def remove_word(bot, user, channel, *args):
    args = list(args)
    if 1 > len(args):
        return bot.send_message(channel, "Jebaited Was für ein Wort/einen Satz soll ich denn jetzt entfernen?")
    if 20 < len(args):
        return bot.send_message(channel, "Jebaited Der Satz ist ein wenig zu lang (Max 20 Wörter)")
    
    phrase = " ".join(args)
    current = [x.strip().lower() for x in db.get(db.configs, "channel", f"{channel}", "black_list")]
    if len(current) < 1:
        return bot.send(channel, "Jebaited Dieser Channel hat bereits eine leere Black List.")
    if not phrase.lower() in current:
        return bot.send_message(channel, "Jebaited Das Wort/der Satz ist nicht auf der Black List.")
    
    current.remove(phrase.lower())
    db.update(db.configs, "channel", f"{channel}", "black_list", current)
    bot.send_message(channel, "SeemsGood Alles klar, ich habe das Wort/den Satz von der Black List entfernt!")


def black_list(bot, user, channel, *args):
    current = [x.strip().lower() for x in db.get(db.configs, "channel", f"{channel}", "black_list")]
    if len(current) < 1:
        return bot.send(channel, "Jebaited Dieser Channel hat eine leere Black List.")
    bot.send_message(channel, f"BOP https://xezbot.ezzz1337.repl.co/{channel.split('#')[1]} (mod-only)")