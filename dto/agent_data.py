from dataclasses import dataclass


@dataclass
class AgentResult:
    """Agent answer dataclass."""

    answer: str
    messages: list[dict]
