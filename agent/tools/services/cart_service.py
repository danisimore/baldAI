import logging
from typing import Any
from repositories.products import get_product_by_id
from repositories import carts, cart_items

_logger = logging.getLogger("tools.logger")


class CartService:
    """A service for interacting with the user's shopping cart."""

    def get_available_product_quantity(self, product: dict[str, Any]) -> int:
        """Calculates the available number of goods from all warehouses.

        Args:
            product (dict[str, Any]): Dict with product data.

        Returns:
            int: Available number of goods from all warehouses.
        """
        return (
            product.get("stock_kursk", 0)
            + product.get("stock_lipetsk", 0)
            + product.get("stock_bryansk", 0)
        )

    def add_product(
        self,
        user_id: int,
        product_id: int,
        quantity: int = 1,
    ) -> dict[str, Any]:
        """
        Add product to user's shopping cart.

        Args:
            user_id: User ID from Postgres.
            product_id: Product identifier.
            quantity: Number of products to add.

        Returns:
            dict[str, Any]: Added products data to the cart
        """
        cart = self.get_or_create_cart(user_id=user_id)
        product = get_product_by_id(product_id=product_id)

        if product is None:
            return {"success": False, "message": "Product not found."}

        available = self.get_available_product_quantity(product)
        if available < quantity:
            return {
                "success": False,
                "message": "Not enough stock.",
                "available": self.get_available_product_quantity(product=product),
            }

        try:
            cart_items.add_item(
                cart_id=cart["id"],
                product_id=product_id,
                quantity=quantity,
                total_price=product["price"] * quantity,
            )

            return {
                "success": True,
                "product_name": product["name"],
                "quantity": quantity,
                "total_price": product.get("price", 0) * quantity,
            }
        except Exception:
            _logger.exception("Error when adding an item to the cart.")
            raise

    def get_or_create_cart(self, user_id: int) -> dict:
        """Gets the user's shopping cart.

        If the bucket does not exist, it creates.

        Args:
            user_id (int): User ID from Postgres.

        Returns:
            dict: dict with data about the user's shopping cart.
        """
        cart = carts.get_active_cart(user_id=user_id)

        if cart is None:
            cart = carts.create_cart(user_id=user_id)

        return cart
