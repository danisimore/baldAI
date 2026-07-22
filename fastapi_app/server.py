import uvicorn

from fastapi_app.main import app


async def start_api():
    """Starts the fastapi application."""
    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )

    server = uvicorn.Server(config)

    await server.serve()
