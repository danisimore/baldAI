import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message

from config import bot_config
from agent.agent import Agent
from repositories.user import get_or_create_user
from repositories.messages import get_history, save_messages


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
    user = get_or_create_user(user_data=message.from_user)

    history = get_history(user["id"])
    result = agent.chat(
        history=history, user_message=message.text, user_id=message.from_user.id
    )

    save_messages(
        client_id=user["id"],
        messages=result.messages,
    )

    await message.answer(result.answer)


async def close_bot():
    """Closes the telegram session."""
    await bot.session.close()


dp.include_router(router)
