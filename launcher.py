import asyncio
import traceback

from bot.xezbot import xezbot
from utils import api



async def register_task(bot):
    asyncio.create_task(api.maybe_new_token(bot, bot.CLIENT_ID, bot.CLIENT_SECRET))



if __name__ == "__main__":
    bot = xezbot()
    asyncio.run(register_task(bot))
    try:
        bot.start()
    except Exception:
        print("Fehler beim Starten: \n{}".format(traceback.format_exc()))
        pass