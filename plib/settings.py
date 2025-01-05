"""
Settings management for the plib library.

This module provides a simple key-value store for global settings with context management.
Settings can be configured globally or temporarily modified within a context.

Example usage:

    # Configure global settings
    import plib
    plib.settings.configure(
        lm=plib.OpenAi(...),  # Set the language model
        n_proc=100,           # Set number of processes
        temperature=0.7,      # Set temperature for LLM sampling
        use_cache=True,       # Enable response caching
        trace=True,          # Enable tracing
        logdir="custom_logs"  # Set custom log directory
    )

    # Get individual settings
    temperature = plib.settings.get("temperature")
    
    # Temporarily override settings in a context
    with plib.settings.context(temperature=0.9, trace=False):
        # Settings are modified only within this block
        ...
    # Settings revert to previous values
"""

import contextlib
import os
import typing

_settings = {"trace": False, "logdir": "logs", "use_cache": True, "temperature": None}

os.makedirs(_settings["logdir"], exist_ok=True)

_known_errors = {
    "lm": "Need to call plib.settings.configure(lm=plib.OpenAi(...))",
    "n_proc": "Need to call plib.settings.configure(n_proc=100)",
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
