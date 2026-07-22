import asyncio

from pyngrok import ngrok

from tg_bot.tg_bot import bot, close_bot
from fastapi_app.server import start_api
from config import ngrok_config, bot_config
from utils.api_utls import wait_api_ready


async def main():
    """Starts and manages the application lifecycle.

    Configures ngrok authentication, starts the FastAPI server,
    waits until the API is ready to accept requests, creates a public
    ngrok tunnel, and registers the Telegram webhook.

    The application runs until the FastAPI server stops. During
    shutdown, the API task is cancelled, the ngrok tunnel is terminated,
    and the Telegram bot session is closed.
    """
    ngrok.set_auth_token(ngrok_config.ngrok_authtoken)
    api_task = asyncio.create_task(start_api())

    try:
        await wait_api_ready("http://127.0.0.1:8000/readyz")

        tunnel = await asyncio.to_thread(
            ngrok.connect,
            "http://localhost:8000",
        )

        await bot.set_webhook(f"{tunnel.public_url}{bot_config.webhook_path}")

        await api_task
    finally:
        api_task.cancel()

        try:
            await api_task
        except asyncio.CancelledError:
            pass

        ngrok.kill()
        await close_bot()


if __name__ == "__main__":
    asyncio.run(main())
