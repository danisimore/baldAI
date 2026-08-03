import logging
from aiogram.types import Update
from fastapi import FastAPI, Request, Response, APIRouter
from tg_bot import bot, dp

app = FastAPI()
router = APIRouter()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

_logger = logging.getLogger("fastapi.logger")


@router.post("/webhook")
async def telegram_webhook(requiest: Request) -> Response:
    """Telegram webhook.

    Args:
        requiest (Request): HTTP request from telegram with message data.

    Returns:
        Response: HTTP response.
    """
    data = await requiest.json()
    update = Update.model_validate(data)

    await dp.feed_webhook_update(bot, update)

    return Response(status_code=200)


@router.get("/readyz", status_code=200)
async def readyz() -> dict[str, str]:
    """Checks whether the application is ready to return responses.

    Returns:
        dict[str, str]: dictionary with the status.
    """
    return {"status": "readyz"}


app.include_router(router)
