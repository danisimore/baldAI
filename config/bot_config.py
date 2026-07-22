from config.base_config import BaseConfig


class BotConfig(BaseConfig):
    """Telegram Bot settings."""

    token: str
    webhook_path: str
