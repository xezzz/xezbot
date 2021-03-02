import re
import datetime

from database import connector



db = connector.Database()



def process(bot, user, channel, message, msg_id):
    handle_spam(bot, user, channel, message, msg_id)
    handle_words(bot, user, channel, message, msg_id)
    handle_dupes(bot, user, channel, message, msg_id)



def handle_words(bot, user, channel, message, msg_id):
    black_list = [x.lower().strip() for x in db.get(db.configs, "channel", channel, "black_list")]
    msg = message.replace("//", "")
    try:
        CENSOR_RE = re.compile(r"|".join(black_list))
        found = CENSOR_RE.search(msg)
        if found:
            bot.send_message(channel, f"/delete {msg_id}")
    except Exception:
        return



def handle_dupes(bot, user, channel, message, msg_id):
    parts = message.split(" ")
    allowed = 5
    if len(parts) >= (len(set(parts)) + allowed):
        bot.send_message(channel, f"/timeout {user['name']} 30s ResidentSleeper Nachricht enthält mehrfach den selben Inhalt")
    else:
        pass



def handle_spam(bot, user, channel, message, msg_id):
    #TODO change this fucking function, tf is this dict storing with 1000 if statements?
    cache = bot.spam_bucket
    uid = str(user["id"])
    if uid in cache:
        if cache[uid]["count"] == 3:
            dif = cache[uid]["messages"]["msg3"]["time"] - cache[uid]["messages"]["msg1"]["time"]
            max_dif = datetime.timedelta(seconds=5) - datetime.timedelta(seconds=1)
            if dif < max_dif:
                del cache[uid]
                bot.send_message(channel, f"/timeout {user['name']} 2m ResidentSleeper Spam (3+/2s)")
            else:
                del cache[uid]
        elif cache[uid]["count"] == 2:
            cache[uid]["count"] = 3
            cache[uid]["messages"]["msg3"] = {}
            cache[uid]["messages"]["msg3"]["time"] = datetime.datetime.utcnow()
        elif cache[uid]["count"] == 1:
            cache[uid]["count"] = 2
    else:
        cache[uid] = {}
        cache[uid]["count"] = 1
        cache[uid]["messages"] = {}
        cache[uid]["messages"]["msg1"] = {}
        cache[uid]["messages"]["msg1"]["time"] = datetime.datetime.utcnow()