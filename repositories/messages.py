from psycopg2.extras import Json
from db import get_cursor
from agent.prompts import SYSTEM_PROMPT


def get_history(client_id: int) -> list[dict]:
    """Loads the conversation history for a client.

    Args:
        client_id (int): user telegram id.

    Returns:
        list[dict]: conversation history.
    """

    history = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]

    with get_cursor() as cur:
        cur.execute(
            """
            SELECT message
            FROM messages
            WHERE client_id = %s
            ORDER BY id
            """,
            (client_id,),
        )

        history.extend(row["message"] for row in cur.fetchall())

    return history


def save_messages(client_id: int, messages: list[dict]) -> None:
    """Saved message into db.

    Args:
        client_id (int): postgres client_id.
        messages (list[dict]): message history.
    """
    with get_cursor() as cur:
        cur.executemany(
            """
            INSERT INTO messages (
                client_id,
                message
            )
            VALUES (%s, %s)
            """,
            [(client_id, Json(message)) for message in messages],
        )
