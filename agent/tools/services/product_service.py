from dto.product_search_filter import ProductSearchFilter
from repositories import products


class ProductSearchService:
    """
    Implements business logic for searching products.
    """

    def find_products(self, filters: ProductSearchFilter) -> list[dict]:
        """
        Searches products using the specified filters.

        Args:
            filters (ProductSearchFilter): Product search filters.

        Returns:
            list[dict]: Products matching the specified filters.
        """
        return products.search_products(filters)
