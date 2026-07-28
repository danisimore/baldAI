from db import get_cursor
from aiogram.types import User


def get_user(telegram_id: int) -> dict[str, any] | None:
    """Retrieves a client by Telegram ID.

    Args:
        telegram_id (int): Telegram user identifier.

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


def create_user(user_data: User) -> dict[str, any]:
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


def get_or_create_user(user_data: User) -> dict[str, any]:
    """Retrieves an existing client or creates a new one.

    Searches for a client by Telegram ID. If the client does not exist,
    creates a new database record.

    Args:
        user_data (User): Telegram user data.

    Returns:
        dict[str, Any]: Existing or newly created client record.
    """
    user = get_user(telegram_id=user_data.id)
    if user:
        return user

    return create_user(user_data)
