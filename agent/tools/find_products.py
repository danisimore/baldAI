import logging
from agent.tools.services.product_service import ProductSearchService
from dto.product_search_filter import ProductSearchFilter

_logger = logging.getLogger("tools.logger")


TOOL = {
    "type": "function",
    "function": {
        "name": "find_products",
        "description": (
            "Search products in the catalog.\n\n"
            "Extract as many structured filters as possible from the user's request.\n"
            "Use:\n"
            "- brand for manufacturer names;\n"
            "- category for product categories;\n"
            "- article for product codes;\n"
            "- type for product characteristics (e.g. биметаллический, алюминиевый);\n"
            "- sections for radiator sections;\n"
            "- diameter for pipe or fitting connection size;\n"
            "- size for radiator dimensions;\n"
            "- min_price/max_price for price limits.\n\n"
            "Use query only for the product name or keywords that cannot be represented "
            "by structured filters.\n"
            "Do not duplicate structured filters inside query.\n"
            "If the user specifies multiple filters, extract all of them."
        ),
        "parameters": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "query": {
                    "type": "string",
                    "description": (
                        "Free-text product name or keywords. "
                        "Use only when the request cannot be fully represented "
                        "by structured filters.\n"
                        "Examples: "
                        "'Радиатор биметаллический ГКС ECO Bi 500/100 8 секций', "
                        "'Муфта серая', "
                        "'Угольник VALFEX'."
                    ),
                },
                "category": {
                    "type": "string",
                    "description": (
                        "Product category.\n"
                        "Examples: "
                        "'Радиаторы отопления', "
                        "'Трубопроводная арматура', "
                        "'Фитинги', "
                        "'Трубы'."
                    ),
                },
                "brand": {
                    "type": "string",
                    "description": (
                        "Manufacturer or brand.\n"
                        "Examples: "
                        "'Royal Thermo', "
                        "'VALFEX', "
                        "'LAMIN', "
                        "'ГКС', "
                        "'BAXI'."
                    ),
                },
                "article": {
                    "type": "string",
                    "description": ("Exact or partial product article number."),
                },
                "type": {
                    "type": "string",
                    "description": (
                        "Product type or material inside a category.\n"
                        "Examples: "
                        "'биметаллический', "
                        "'алюминиевый', "
                        "'шаровый'."
                    ),
                },
                "diameter": {
                    "type": "string",
                    "description": (
                        "Pipe or fitting connection size exactly as specified "
                        "by the user.\n"
                        "Examples: "
                        "'20', "
                        "'25', "
                        "'20x1/2', "
                        "'32x3/4', "
                        "'1/2', "
                        "'DN20'."
                    ),
                },
                "sections": {
                    "type": "integer",
                    "description": ("Number of radiator sections."),
                },
                "size": {
                    "type": "string",
                    "description": (
                        "Radiator dimensions exactly as specified by the user "
                        "or stored in the catalog.\n"
                        "Examples: "
                        "'500/100', "
                        "'350/80'."
                    ),
                },
                "min_price": {
                    "type": "integer",
                    "description": ("Minimum product price."),
                },
                "max_price": {
                    "type": "integer",
                    "description": ("Maximum product price."),
                },
                "limit": {
                    "type": "integer",
                    "description": (
                        "Maximum number of returned products. "
                        "Usually omit this parameter."
                    ),
                },
                "in_stock": {
                    "type": "boolean",
                    "description": (
                        "Return only products that are currently in stock. "
                        "Use when the user asks for products that are available, "
                        "in stock, or can be purchased immediately."
                    ),
                },
            },
        },
    },
}
"""AI Agent tool for find products."""


def find_products(
    query: str | None = None,
    category: str | None = None,
    brand: str | None = None,
    article: str | None = None,
    type: str | None = None,
    diameter: str | None = None,
    sections: int | None = None,
    size: str | None = None,
    min_price: int | None = None,
    max_price: int | None = None,
    in_stock: bool | None = None,
    limit: int = 5,
) -> list[dict]:
    """
    Searches the product catalog using parameters extracted from an LLM request.

    Creates a ProductSearchFilter instance from the provided arguments and
    delegates the search to the product search service.

    Args:
        query (str | None, optional):
            Free-text product name or search keywords.
        category (str | None, optional):
            Product category.
        brand (str | None, optional):
            Manufacturer or brand.
        article (str | None, optional):
            Product article number.
        type (str | None, optional):
            Product type or characteristic.
        diameter (str | None, optional):
            Pipe or fitting connection size.
        sections (int | None, optional):
            Number of radiator sections.
        size (str | None, optional):
            Product size or dimensions.
        min_price (int | None, optional):
            Minimum product price.
        max_price (int | None, optional):
            Maximum product price.
        in_stock (bool | None, optional):
            Whether to return only products currently in stock.
        limit (int, optional):
            Maximum number of returned products. Defaults to 5.

    Returns:
        list[dict]: Matching products.
    """
    filters = ProductSearchFilter(
        query=query,
        category=category,
        brand=brand,
        article=article,
        type=type,
        diameter=diameter,
        sections=sections,
        size=size,
        min_price=min_price,
        max_price=max_price,
        limit=limit,
        in_stock=in_stock,
    )
    return ProductSearchService().find_products(filters=filters)
