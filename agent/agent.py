import logging
import json
from agent.llm import OllamaClient
from agent.prompts import SYSTEM_PROMPT
from agent.tools_registry import TOOLS, FUNCTIONS

_logger = logging.getLogger("bot.logger")


class Agent:
    """LLM-powered shopping assistant.

    Coordinates interaction with the language model and external tools.
    Executes tool calls requested by the model, appends tool results to
    the conversation, and continues the dialogue until a final response
    is produced.
    """

    MAX_TOOL_CALLS = 10

    def __init__(self):
        self.llm = OllamaClient()

    def chat(self, user_message: str) -> str:
        """Generates a response to a user's message.

        Starts a conversation with the system prompt and the user's message,
        sends it to the language model, executes any requested tool calls,
        appends tool results to the conversation, and continues until the
        model returns a final response without requesting additional tools.

        Args:
            user_message (str): User's input message.

        Returns:
            str: Final assistant response.

        Raises:
            RuntimeError: If the language model exceeds the maximum allowed
                number of tool calls.
        """
        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": user_message,
            },
        ]

        for _ in range(self.MAX_TOOL_CALLS):
            response = self.llm.chat(
                messages=messages,
                tools=TOOLS,
            )

            assistant = response.message

            messages.append(
                {
                    "role": "assistant",
                    "content": assistant.content,
                    "tool_calls": assistant.tool_calls,
                }
            )

            if not assistant.tool_calls:
                return assistant.content or ""

            for tool_call in assistant.tool_calls:
                tool_name = tool_call.function.name
                arguments = tool_call.function.arguments

                _logger.info(
                    "Calling tool %s(%s)",
                    tool_name,
                    arguments,
                )

                func = FUNCTIONS[tool_name]
                result = func(**arguments)

                _logger.info(
                    "Tool %s returned %d objects",
                    tool_name,
                    len(result) if isinstance(result, list) else 1,
                )

                messages.append(
                    {
                        "role": "tool",
                        "name": tool_name,
                        "content": json.dumps(
                            result,
                            ensure_ascii=False,
                        ),
                    }
                )

        raise RuntimeError("LLM exceeded maximum number of tool calls.")
