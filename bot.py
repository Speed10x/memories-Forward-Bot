import asyncio
import logging
import logging.config
from database import db
from config import Config
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from pyrogram.enums import ParseMode
from pyrogram.errors import FloodWait
from pyrogram.types import Update

# bot developer @mr_jisshu
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)

class Bot(Client):
    def __init__(self):
        super().__init__(
            Config.BOT_SESSION,
            api_hash=Config.API_HASH,
            api_id=Config.API_ID,
            plugins={"root": "plugins"},
            workers=50,
            bot_token=Config.BOT_TOKEN
        )
        self.log = logging

    async def start(self):
        await super().start()
        me = await self.get_me()
        logging.info(f"{me.first_name} with for pyrogram v{__version__} (Layer {layer}) started on @{me.username}.")
        self.id = me.id
        self.username = me.username
        self.first_name = me.first_name
        self.set_parse_mode(ParseMode.DEFAULT)

        # Notify all forward users
        text = "**๏[-ิ_•ิ]๏ bot restarted !**"
        success = failed = 0
        users = await db.get_all_frwd()
        async for user in users:
            chat_id = user['user_id']
            try:
                await self.send_message(chat_id, text)
                success += 1
            except FloodWait as e:
                await asyncio.sleep(e.value + 1)
                await self.send_message(chat_id, text)
                success += 1
            except Exception:
                failed += 1

        if (success + failed) != 0:
            await db.rmve_frwd(all=True)
            logging.info(f"Restart message status: success={success}, failed={failed}")

    async def stop(self, *args):
        msg = f"@{self.username} stopped. Bye."
        await super().stop()
        logging.info(msg)

    def set_webhook(self, url: str):
        # Correct webhook setup — without using raw functions
        self.loop.run_until_complete(self.set_webhook(url))
        self.log.info(f"Webhook set to {url}")

    def process_update(self, update: dict):
        # Feed Telegram updates to Pyrogram manually
        try:
            parsed_update = Update.de_json(update, self)
            self.loop.create_task(self.dispatcher.feed_update(parsed_update))
        except Exception as e:
            self.log.error(f"Failed to process update: {e}")
