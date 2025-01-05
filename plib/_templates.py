import os
import pathlib

import jinja2

from . import settings

# Initialize Jinja environment
_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        os.path.join(pathlib.Path(__file__).parent, "templates")
    ),
    trim_blocks=True,
    lstrip_blocks=True,
)

# Cache for loaded templates
_templates: dict[str, jinja2.Template] = {}


def get_template(template_type: str = None) -> jinja2.Template:
    """Get the appropriate template based on settings or override"""
    # Use provided type or get from settings
    template_type = template_type or settings.get("template")

    # Validate template type
    if template_type not in ["xml", "markdown"]:
        raise ValueError(f"Unsupported template type: {template_type}")

    # Load template if not already loaded
    # Instead of validating template type, just try to load it and then throw a ValueError if it's not present. AI!
    if template_type not in _templates:
        _templates[template_type] = _env.get_template(f"{template_type}.tmpl")

    return _templates[template_type]
