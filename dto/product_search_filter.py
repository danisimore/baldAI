from dataclasses import dataclass


@dataclass(slots=True)
class ProductSearchFilter:
    """
    Represents product search criteria.

    Each field is optional and, when provided, is used to build the SQL
    query for searching products in the catalog.
    """

    query: str | None = None
    category: str | None = None
    brand: str | None = None
    article: str | None = None
    type: str | None = None
    diameter: int | None = None
    sections: int | None = None
    size: str | None = None
    min_price: int | None = None
    max_price: int | None = None
    in_stock: bool | None = None
    limit: int = 5
