from . import settings
import litellm
import beartype


@beartype.beartype
def send(msg: str, history: list[object]) -> tuple[str, list[object]]:
    """
    Send a message to the LLM and get the response.

    Args:
        msg: The message to send to the LLM
        history: Optional chat history for context

    Returns:
        The LLM's response as a string and new history.

    Raises:
        ValueError: If required settings are missing
        RuntimeError: If LLM call fails
    """
    # Get required model setting
    model = settings.get("llm")  # e.g. "gpt-4"

    # Get optional settings with defaults.
    temperature = (
        0.7 if settings.get("temperature") is None else settings.get("temperature")
    )
    max_tokens = (
        1000 if settings.get("max_tokens") is None else settings.get("max_tokens")
    )

    try:
        # Format messages for chat completion
        messages = []

        # Add history if provided
        if history:
            messages.extend(history)

        # Add current message
        messages.append({"role": "user", "content": msg})

        # Make LLM call
        response = litellm.completion(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        # Extract and return the response text
        # Return updated history as well AI!
        return response.choices[0].message.content

    except Exception as e:
        # Wrap any LiteLLM errors
        raise RuntimeError(f"LLM call failed: {str(e)}") from e
