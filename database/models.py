def command_model(cmd_id, reply, author, timestamp):
    model = {
        "command_id": f"{cmd_id}",
        "reply": f"{reply}",
        "author": f"{author}",
        "timestamp": timestamp
    }
    return model



def channel_model(channel, black_list):
    model = {
        "channel": f"{channel}",
        "black_list": black_list
    }
    return model