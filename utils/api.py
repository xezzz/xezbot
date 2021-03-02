import aiohttp
import asyncio
from datetime import datetime


async def get_bearer_token(bot, client_id, client_secret):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://id.twitch.tv/oauth2/token",
            params={
                "client_id": client_id,
                "client_secret": client_secret,
                "grant_type": "client_credentials"
            },
        ) as req:
            try:
                data = await req.json()
            except aiohttp.ContentTypeError:
                data = {}
                
            if req.status == 200:
                pass
            elif req.status == 400 and data.get("message") == "invalid client":
                print("Ungültige Client ID")
            elif req.status == 403 and data.get("message") == "invalid client secret":
                print("Invalid Client Secret")
            elif "message" in data:
                print("Anfrage fehlgeschlagen mit Fehlercode {} und Nachricht {}".format(str(req.status), data["message"]))
            else:
                print(f"Anfrage fehlgeschlagen mit Fehlercode {req.status}")
                
            if req.status != 200:
                return
            
        api_cache = data
        api_cache["expires_at"] = datetime.utcnow().timestamp() + data.get("expires_in")
        return data


async def maybe_new_token(bot, client_id, client_secret) -> None:
    await asyncio.sleep(10)
    if bot.api_cache:
        if bot.api_cache["expires_at"] - datetime.utcnow().timestamp() >= 60:
            await get_bearer_token(bot, client_id, client_secret)
