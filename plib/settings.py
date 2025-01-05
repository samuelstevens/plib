# Document this file. Describe example public usage. AI!


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
