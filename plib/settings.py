"""
Settings management for the plib library.

This module provides a simple key-value store for global settings with context management.
Settings can be configured globally or temporarily modified within a context.

Example usage:

```py
# Configure global settings
import plib
plib.settings.configure(
    llm="ollama_chat/mistral:7b",  # Set the language model
    n_proc=100,                    # Set number of processes
    use_cache=True,                # Enable response caching
    logdir="custom_logs"           # Set custom log directory
)

# Get individual settings
temperature = plib.settings.get("temperature")

# Temporarily override settings in a context
with plib.settings.context(temperature=0.9, trace=True):
    # Settings are modified only within this block
    ...
# Settings revert to previous values
```
"""

import contextlib
import os
import typing

_settings = {
    "trace": False,
    "logdir": "logs",
    "use_cache": True,
    "temperature": None,
    "template": "xml",
}

os.makedirs(_settings["logdir"], exist_ok=True)

_known_errors = {
    "llm": "Need to call plib.settings.configure(llm='ollama_chat/llama3.1:8b')",
    "n_proc": "Need to call plib.settings.configure(n_proc=100)",
    "template": "Need to call plib.settings.configure(template='xml|markdown')",
}


def get(key) -> typing.Any:
    if key in _settings:
        return _settings[key]

    if key in _known_errors:
        raise ValueError(_known_errors[key])

    raise ValueError(f"Missing setting: {key}")


def configure(**kwargs):
    for key, value in kwargs.items():
        _settings[key] = value


@contextlib.contextmanager
def context(**kwargs):
    old = {}
    for key, value in kwargs.items():
        if key in _settings:
            old[key] = _settings.pop(key)

        _settings[key] = value

    yield

    for key, value in kwargs.items():
        _settings.pop(key)

        if key in old:
            _settings[key] = old.pop(key)

    assert not old
