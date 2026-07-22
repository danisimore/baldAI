import logging

from aiogram import Bot, Dispatcher

from config import bot_config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

_logger = logging.getLogger("bot.logger")

bot = Bot(token=bot_config.token)
dp = Dispatcher()


async def close_bot():
    """Closes the telegram session."""
    await bot.session.close()
