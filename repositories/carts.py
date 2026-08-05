import logging
from typing import Any
from db import get_cursor
from repositories.user import get_user_by_id


_logger = logging.getLogger("repos.logger")


def get_active_cart(user_id: int) -> dict[str, Any] | None:
    """Gets user's shopping cart.

    Args:
        user_id (int): id of the user whose shopping cart you want to receive.

    Returns:
        dict[str, Any]: dictionary with data about the user's cart.
    """

    with get_cursor() as cur:
        sql = """
            SELECT *
            FROM carts
            WHERE client_id = %(user_id)s
            AND status = %(status)s;
        """
        cur.execute(
            sql,
            {
                "user_id": user_id,
                "status": "active",
            },
        )
        return cur.fetchone()


def create_cart(user_id: int) -> dict[str, Any]:
    """Creates a cart for the user.

    To avoid the race condition, you need an index for carts by client_id.
    Example:
        CREATE UNIQUE INDEX ux_active_cart
        ON carts(client_id)
        WHERE status = 'active';

    Args:
        user_id (int): id of the user to create a shopping cart for.

    Returns:
        dict[str, Any]: dictionary with data about the created cart.
    """
    user = get_user_by_id(id=user_id)

    with get_cursor() as cur:
        try:
            sql = """
            INSERT INTO carts (
                client_id,
                status
            )
            VALUES (
                %(client_id)s,
                %(status)s
            )
            RETURNING *;
            """

            cur.execute(
                sql,
                {
                    "client_id": user["id"],
                    "status": "active",
                },
            )
            return cur.fetchone()
        except Exception:
            _logger.exception(
                "Failed to create cart for user %s",
                user["id"],
            )
            raise
