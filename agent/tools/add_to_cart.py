import logging
from agent.tools.services.cart_service import CartService
from typing import Any

_logger = logging.getLogger("tools.logger")

TOOL = {
    "type": "function",
    "function": {
        "name": "add_to_cart",
        "description": (
            "Adds a product to the user's shopping cart. "
            "Use the product id returned by find_products."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "product_id": {
                    "type": "integer",
                    "description": "ID of the product to add",
                },
                "quantity": {
                    "type": "integer",
                    "description": "Quantity of products",
                    "default": 1,
                },
            },
            "required": ["product_id"],
        },
    },
}
"""AI Agent tool for create cart."""


def add_to_cart(
    user_id: int,
    product_id: int,
    quantity: int = 1,
) -> dict[str, Any]:
    """
    Add product to user's shopping cart.

    Args:
        user_id: User id from Postgres.
        product_id: Product identifier.
        quantity: Number of products to add.

    Returns:
        dict[str, Any]: Added products data to the cart
    """

    return CartService().add_product(
        user_id=user_id,
        product_id=product_id,
        quantity=quantity,
    )
