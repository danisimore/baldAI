from ollama import Client


class OllamaClient:
    """Client for interacting with a locally hosted Ollama model.

    Wraps the official Ollama Python client and provides a simplified
    interface for sending chat completion requests with optional tool
    definitions.
    """

    def __init__(self, host: str = "http://localhost:11434", model: str = "qwen3:8b"):
        self.client = Client(host=host)
        self.model = model

    def chat(
        self,
        messages: list[dict[str, any]],
        tools: list[dict[str, any]] | None = None,
    ):
        """Sends a chat completion request to the Ollama server.

        Args:
            messages (list[dict]): Conversation history formatted according
                to the Ollama chat API.
            tools (list[dict] | None): Optional tool definitions available
                to the language model.

        Returns:
            ChatResponse: Response returned by the Ollama client containing
                the assistant message and any requested tool calls.
        """
        return self.client.chat(model=self.model, messages=messages, tools=tools)
