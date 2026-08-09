import logging
import asyncio

from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message

from config import bot_config
from agent.agent import Agent
from repositories.user import get_or_create_user
from repositories.messages import get_history, save_messages

from tg_bot.services import transcriber


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
    if message.voice:
        try:
            path = await transcriber.download_voice(message)

            try:
                text = await asyncio.to_thread(
                    transcriber.transcribe,
                    str(path),
                )
                _logger.info("Сообщение успешно транскрибировано:\n\n%s", text)
            finally:
                path.unlink(missing_ok=True)

        except Exception:
            _logger.exception("Failed to transcribe voice message.")

            await message.answer(
                "К сожалению, мне не удалось распознать ваше голосовое сообщение. "
                "Попробуйте отправить его еще раз или напишите текстом."
            )
            return
    else:
        text = message.text

    user = get_or_create_user(user_data=message.from_user)

    history = get_history(user["id"])
    result = agent.chat(
        history=history, user_message=text, user_id=message.from_user.id
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
