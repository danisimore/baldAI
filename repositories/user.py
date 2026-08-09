from typing import Any
from db import get_cursor
from aiogram.types import User


def get_user_by_telegram_id(telegram_id: str) -> dict[str, Any] | None:
    """Retrieves a client by Telegram ID.

    Args:
        telegram_id (int): User telegram ID.

    Returns:
        dict[str, Any] | None: Client record if found, otherwise None.
    """
    with get_cursor() as cur:
        cur.execute(
            """
            SELECT *
            FROM clients
            WHERE telegram_id = %s
            """,
            (telegram_id,),
        )
        return cur.fetchone()


def get_user_by_id(id: int) -> dict[str, Any] | None:
    """Retrieves a client by ID.

    Args:
        id (int): User ID in Postgres.

    Returns:
        dict[str, Any] | None: Client record if found, otherwise None.
    """
    with get_cursor() as cur:
        cur.execute(
            """
            SELECT *
            FROM clients
            WHERE id = %s
            """,
            (id,),
        )
        return cur.fetchone()


def create_user(user_data: User) -> dict[str, Any]:
    """Creates a new client.

    Stores the Telegram user in the database and returns the created
    client record.

    Args:
        user_data (User): Telegram user data.

    Returns:
        dict[str, Any]: Newly created client record.
    """
    with get_cursor() as cur:
        cur.execute(
            """
            INSERT INTO clients (
                telegram_id,
                username
            )
            VALUES (%s, %s)
            ON CONFLICT (telegram_id)
            DO UPDATE
            SET username = EXCLUDED.username
            RETURNING *;
            """,
            (user_data.id, user_data.username),
        )
        return cur.fetchone()


def get_or_create_user(user_data: User) -> dict[str, Any]:
    """Retrieves an existing client or creates a new one.

    Searches for a client by Telegram ID. If the client does not exist,
    creates a new database record.

    Args:
        user_data (User): Telegram user data.

    Returns:
        dict[str, Any]: Existing or newly created client record.
    """
    user = get_user_by_telegram_id(telegram_id=user_data.id)
    if user:
        return user

    return create_user(user_data)
