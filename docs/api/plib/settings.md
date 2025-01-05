Module plib.settings
====================
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

Functions
---------

`configure(**kwargs)`
:   

`context(**kwargs)`
:   

`get(key) ‑> Any`
: