from dataclasses import dataclass


@dataclass
class ToolContext:
    """Tool context dataclass."""

    telegram_id: str | None
    user_id: int
