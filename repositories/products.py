from typing import Any
from db import get_cursor
from dto.product_search_filter import ProductSearchFilter


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


def search_products(filters: ProductSearchFilter) -> list[dict[str, Any]]:
    """
    Executes SQL queries for product search.

    Builds a dynamic SQL query based on the provided search criteria and
    returns matching products from the database.

    Args:
        filters (ProductSearchFilter): Product search filters.

    Returns:
        list[dict[str, Any]]: List of products matching the specified filters.
    """
    with get_cursor() as cur:
        where = []
        params = {}

        if filters.query:
            where.append("""
                word_similarity(lower(%(query)s), lower(p.name)) > 0.8
            """)
            params["query"] = filters.query

        if filters.brand:
            where.append("""
                word_similarity(lower(%(brand)s), lower(b.name)) > 0.5
            """)
            params["brand"] = filters.brand

        if filters.category:
            where.append("""
                word_similarity(lower(%(category)s), lower(c.name)) > 0.5
            """)
            params["category"] = filters.category

        if filters.article:
            where.append("""
                p.article ILIKE %(article)s
            """)
            params["article"] = f"%{filters.article}%"

        if filters.type:
            where.append("""
                word_similarity(lower(%(type)s), lower(p.type)) > 0.7
            """)
            params["type"] = filters.type

        if filters.sections is not None:
            where.append("""
                p.sections = %(sections)s
            """)
            params["sections"] = filters.sections

        if filters.size:
            where.append("""
                p.size = %(size)s
            """)
            params["size"] = filters.size

        if filters.diameter:
            where.append("""
                p.diameter = %(diameter)s
            """)
            params["diameter"] = filters.diameter

        if filters.min_price is not None:
            where.append("""
                p.price >= %(min_price)s
            """)
            params["min_price"] = filters.min_price

        if filters.max_price is not None:
            where.append("""
                p.price <= %(max_price)s
            """)
            params["max_price"] = filters.max_price

        if filters.in_stock:
            where.append("""
                (
                    COALESCE(p.stock_kursk, 0) +
                    COALESCE(p.stock_lipetsk, 0) +
                    COALESCE(p.stock_bryansk, 0)
                ) > 0
            """)

        sql = """
            SELECT
                p.id,
                p.article,
                p.name,
                b.name AS brand,
                c.name AS category,
                p.type,
                p.size,
                p.sections,
                p.diameter,
                p.pack,
                p.price,
                p.stock_kursk,
                p.stock_lipetsk,
                p.stock_bryansk
            FROM products p
            LEFT JOIN product_brand b
                ON p.brand_id = b.brand_id
            LEFT JOIN product_category c
                ON p.category_id = c.category_id
        """

        if where:
            sql += "\nWHERE " + "\nAND ".join(where)

        sql += "\nLIMIT %(limit)s"
        params["limit"] = min(filters.limit, 50)

        cur.execute(sql, params)
        return cur.fetchall()
