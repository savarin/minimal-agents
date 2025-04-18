from dataclasses import dataclass


@dataclass
class Usage:
    requests: int = 0
    """Total requests made to the LLM API."""

    input_tokens: int = 0
    """Total input tokens sent, across all requests."""

    output_tokens: int = 0
    """Total output tokens received, across all requests."""

    total_tokens: int = 0
    """Total tokens sent and received, across all requests."""
