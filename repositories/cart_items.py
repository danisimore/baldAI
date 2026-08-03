from db import get_cursor


def add_item(
    cart_id: int,
    product_id: int,
    quantity: int,
    total_price: int,
):
    """Creates carts item.

    Args:
        cart (dict[str, Any]): dict with user's shopping cart data.
        product (dict[str, Any]): the product being added to the cart.
        product_id (int): the id of product being added to the cart.
        quantity (int): the number of items added to the cart.
    """
    with get_cursor() as cur:
        sql = """
            INSERT INTO cart_items (
                cart_id,
                product_id,
                quantity,
                price
            ) VALUES (
                %(cart_id)s,
                %(product_id)s,
                %(quantity)s,
                %(price)s
            )
        """

        cur.execute(
            sql,
            {
                "cart_id": cart_id,
                "product_id": product_id,
                "quantity": quantity,
                "price": total_price,
            },
        )
