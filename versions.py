VERSION = "0.1.2"
"""Application version."""

RELEASE_DATE = "2026-08-05"
"""Release date of the version."""

CHANGELOG = {
    "0.1.2": {
        "date": "2026-08-05",
        "changes": [
            "The product search tool has been modified. "
            "Now it allows you to search through all the necessary fields.",
        ],
    },
    "0.1.1": {
        "date": "2026-08-03",
        "changes": [
            "Added tools: get_cart_tool and add_cart_tool",
            "Added Tool Executor.",
            "Prompt has been updated.",
            "The code has been adapted to the new table structure.",
            "Added repositories for interacting with the carts and cart_items tables",
            "Implemented a CartExecutor for working with shopping carts",
        ],
    },
    "0.1.0": {
        "date": "2026-07-28",
        "changes": [
            "Added AI Agent.",
            "Added DeepSeek connector.",
        ],
    },
    "0.0.2": {
        "date": "2026-07-22",
        "changes": [
            "Added automation of project launch.",
        ],
    },
    "0.0.1": {
        "date": "2026-07-21",
        "changes": [
            "Launch of a telegram bot has been implemented.",
            "Implemented a webhook on fastapi.",
        ],
    },
}
"""Information about changes made in versions."""
