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

    # Get optional settings (defaults handled by settings module)
    temperature = settings.get("temperature")
    max_tokens = settings.get("max_tokens")

    # TODO: Implement LLM call
    pass
