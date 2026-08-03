import logging
from openai import OpenAI

from config import llm_config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

_logger = logging.getLogger("llm.logger")


class _DeepSeekResponse:
    """Minimal wrapper to mimic Ollama's ChatResponse structure."""

    def __init__(self, message):
        self.message = message


class DeepSeekClient:
    """Client for interacting with DeepSeek API via OpenAI-compatible interface."""

    def __init__(
        self,
        base_url: str = "https://api.deepseek.com",
        model: str = "deepseek-chat",
    ):
        self.client = OpenAI(
            api_key=llm_config.api_key,
            base_url=base_url,
        )
        self.model = model

    def chat(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
    ) -> _DeepSeekResponse:
        """Send a chat completion request to DeepSeek API.

        Args:
            messages (list[dict]): message history.
            tools (list[dict]): available tools that LLM can use.

        Returns:
            _DeepSeekResponse: DeepSeek answer.
        """

        cleaned_messages = []

        for message in messages:
            msg = dict(message)

            if msg.get("role") == "assistant" and msg.get("tool_calls") is None:
                msg.pop("tool_calls", None)

            cleaned_messages.append(msg)

        kwargs = {
            "model": self.model,
            "messages": cleaned_messages,
        }

        if tools:
            kwargs["tools"] = tools

        _logger.debug(
            "Sending request to DeepSeek: model=%s, messages=%d, tools=%s",
            self.model,
            len(cleaned_messages),
            bool(tools),
        )

        response = self.client.chat.completions.create(**kwargs)
        message = response.choices[0].message

        return _DeepSeekResponse(message)
