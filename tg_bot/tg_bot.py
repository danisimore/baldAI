import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message

from config import bot_config
from agent.agent import Agent


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

_logger = logging.getLogger("bot.logger")

bot = Bot(token=bot_config.token)
dp = Dispatcher()
router = Router()
agent = Agent()


@router.message()
async def chat(message: Message):
    """Handles incoming Telegram messages.

    Receives a message from Telegram, loads the conversation context,
    passes the user's request to the AI agent, and sends the generated
    response back to the user.

    Args:
        message (Message): Incoming Telegram message.
    """
    pass
    # answer = agent.chat(message.text)

    # await message.answer(answer)


async def close_bot():
    """Closes the telegram session."""
    await bot.session.close()


dp.include_router(router)
