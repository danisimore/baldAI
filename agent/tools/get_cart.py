import logging
from typing import Any
from agent.tools.services.cart_service import CartService

_logger = logging.getLogger("tools.logger")

TOOL = {
    "type": "function",
    "function": {
        "name": "get_cart",
        "description": "Returns the user's active cart. Creates one if it doesn't exist.",
        "parameters": {"type": "object", "properties": {}},
    },
}
"""AI Agent tool for create cart."""


def get_cart(user_id: int) -> dict[str, Any]:
    """Gets user's shopping cart.

    If there is no cart, it will be created.

    Args:
        user_id (int): id of the user whose shopping cart you want to receive.

    Returns:
        dict[str, Any]: dictionary with data about the user's cart.
    """
    return CartService().get_or_create_cart(user_id=user_id)
