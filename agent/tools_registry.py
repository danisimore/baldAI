from agent.tools.find_products import TOOL as find_products_tool, find_products
from agent.tools.get_cart import TOOL as get_cart_tool, get_cart
from agent.tools.add_to_cart import TOOL as add_cart_tool, add_to_cart

TOOLS = [find_products_tool, get_cart_tool, add_cart_tool]
"""AI Agent tools."""

FUNCTIONS = {
    "find_products": find_products,
    "get_cart": get_cart,
    "add_to_cart": add_to_cart,
}
"""Tools functions."""
