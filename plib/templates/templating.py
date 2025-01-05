import pathlib

import jinja2

from .. import settings

# Initialize Jinja environment
_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(pathlib.Path(__file__).parent),
    trim_blocks=True,
    lstrip_blocks=True,
    autoescape=jinja2.select_autoescape(),
)

# Cache for loaded templates
_cache: dict[str, jinja2.Template] = {}


def load(template_type: str = None) -> jinja2.Template:
    """Get the appropriate template based on settings or override"""
    # Use provided type or get from settings
    template_type = template_type or settings.get("template")

    # Load template if not already loaded
    if template_type not in _cache:
        try:
            _cache[template_type] = _env.get_template(f"{template_type}.tmpl")
        except jinja2.TemplateNotFound:
            raise ValueError(f"Unsupported template type: {template_type}")

    return _cache[template_type]
