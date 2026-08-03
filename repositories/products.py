from typing import Any
from db import get_cursor


def get_product_by_id(product_id: str) -> dict[str, Any] | None:
    """
    Returns the product by its ID.

    Args:
        product_id: The product ID.

    Returns:
        Dictionary with product data, if an entry is found,
        else ``None``.
    """
    with get_cursor() as cur:
        sql = """
            SELECT * FROM products WHERE id = %(id)s
        """
        cur.execute(sql, {"id": product_id})
        return cur.fetchone()
