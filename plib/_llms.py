from . import settings
import litellm
import beartype


@beartype.beartype
def send(msg: str, history: list[object]) -> str:
    """
    Send a message to the LLM and get the response.

    Args:
        msg: The message to send to the LLM
        history: Optional chat history for context

    Returns:
        The LLM's response as a string

    Raises:
        ValueError: If required settings are missing
        RuntimeError: If LLM call fails
    """
    # Get required model setting
    model = settings.get("llm")  # e.g. "gpt-4"

    # Get optional settings with defaults.
    # Make a clean separation of defaults for each setting, rather than this repeated code. AI!
    temperature = (
        0.7 if settings.get("temperature") is None else settings.get("temperature")
    )
    max_tokens = (
        1000 if settings.get("max_tokens") is None else settings.get("max_tokens")
    )

    # TODO: Implement LLM call
    pass
