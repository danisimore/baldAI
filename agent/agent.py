import logging
import json
from agent.llm import DeepSeekClient
from agent.tools_registry import TOOLS
from dto.agent_data import AgentResult
from dto.tool_context import ToolContext
from agent.tool_executor import ToolExecutor
from repositories.user import get_user


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
        self.llm = DeepSeekClient(model="deepseek-chat")

    def chat(
        self,
        history: list[dict],
        user_message: str,
        user_id: str,
    ) -> AgentResult:
        """Generates a response to a user's message.

        Starts a conversation with the system prompt and the user's message,
        sends it to the language model, executes any requested tool calls,
        appends tool results to the conversation, and continues until the
        model returns a final response without requesting additional tools.

        Args:
            history (list[dict]): Chat history.
            user_message (str): User's input message.
            user_id (str): telegram user id.

        Returns:
            AgentResult: Final assistant response together with all newly
                generated conversation messages that should be persisted.

        Raises:
            RuntimeError: If the language model exceeds the maximum allowed
                number of tool calls.
        """

        user = get_user(telegram_id=user_id)
        executor = ToolExecutor(
            context=ToolContext(telegram_id=user_id, user_id=user["id"])
        )
        messages = list(history)
        new_messages = []

        user = {
            "role": "user",
            "content": user_message,
        }

        messages.append(user)
        new_messages.append(user)

        for _ in range(self.MAX_TOOL_CALLS):
            response = self.llm.chat(
                messages=messages,
                tools=TOOLS,
            )

            assistant = response.message

            assistant_message = {
                "role": "assistant",
                "content": assistant.content,
                "tool_calls": [
                    tool_call.model_dump() for tool_call in assistant.tool_calls
                ]
                if assistant.tool_calls
                else None,
            }

            messages.append(assistant_message)
            new_messages.append(assistant_message)

            if not assistant.tool_calls:
                return AgentResult(
                    answer=assistant.content or "",
                    messages=new_messages,
                )

            for tool_call in assistant.tool_calls:
                tool_name = tool_call.function.name
                arguments = tool_call.function.arguments

                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        _logger.error(
                            "Failed to parse tool arguments: %s",
                            arguments,
                        )
                        arguments = {}

                _logger.info(
                    "Calling tool %s(%s)",
                    tool_name,
                    arguments,
                )

                result = executor.execute(tool_name=tool_name, arguments=arguments)

                _logger.info(
                    "Tool %s returned %d objects",
                    tool_name,
                    len(result) if isinstance(result, list) else 1,
                )

                tool_message = {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result, ensure_ascii=False, default=str),
                }

                messages.append(tool_message)
                new_messages.append(tool_message)

        raise RuntimeError("LLM exceeded maximum number of tool calls.")
