import beartype
import litellm

from . import settings


@beartype.beartype
async def send(msg: str, history: list[object] = None) -> tuple[str, list[object]]:
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

    try:
        # Format messages for chat completion
        messages = []

        # Add history if provided
        if history:
            messages.extend(history)

        # Add current message
        messages.append({"role": "user", "content": msg})

        # Make LLM call
        response = await litellm.acompletion(
            model=model,
            messages=messages,
            temperature=temperature,
        )

        # Extract response and update history
        response_text = response.choices[0].message.content

        # Add response to history
        messages.append({"role": "assistant", "content": response_text})

        return response_text, messages

    except Exception as err:
        # Wrap any LiteLLM errors
        raise RuntimeError(f"LLM call failed: {str(err)}") from err
