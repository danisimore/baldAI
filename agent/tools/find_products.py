import logging
from db import get_cursor

_logger = logging.getLogger("tools.logger")


TOOL = {
    "type": "function",
    "function": {
        "name": "find_products",
        "description": "Search products by natural language query.",
        "parameters": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
    },
}
"""AI Agent tool for find products."""


def find_products(query: str, limit: int = 5) -> list[dict]:
    """
    Find products matching a natural language search query.

    The query may contain:
    - a full product name;
    - part of a product name;
    - a brand name;
    - a model;
    - a power or other characteristic (e.g. "5.5");
    - several keywords in arbitrary order.

    The search is case-insensitive and returns the most relevant products.

    Examples:
        "АкваФлоу 5.5"
        "водонагреватель АкваФлоу"
        "бойлер thermex 80"
        "проточный 5.5 квт"

    Args:
        query: User search query.
        limit: Maximum number of products to return.

    Returns:
        List of product dictionaries sorted by relevance.
    """

    with get_cursor() as cur:
        sql = """
            SELECT
                id,
                article,
                name,
                category_id,
                brand_id,
                type,
                size,
                sections,
                diameter,
                pack,
                price,
                stock_kursk,
                stock_lipetsk,
                stock_bryansk,

                word_similarity(
                    lower(%(query)s),
                    lower(name)
                ) AS score

            FROM products

            WHERE
                word_similarity(
                    lower(%(query)s),
                    lower(name)
                ) > 0

            ORDER BY score DESC

            LIMIT %(limit)s;
        """

        cur.execute(
            sql,
            {
                "query": query,
                "limit": limit,
            },
        )
        rows = cur.fetchall()

        rows = [row for row in rows if row["score"] > 0.8]

        return rows


if __name__ == "__main__":
    while True:
        query = input("Поиск: ")

        if not query:
            break

        products = find_products(query)

        print("-" * 50)

        for product in products:
            print(f"Score: {product['score']:.3f}")
            print(product["name"])
            print(product["price"])
            print()
