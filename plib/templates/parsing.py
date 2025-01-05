import re

from .._data import Schema

from .. import settings


def parse_xml(text: str, schema: Schema) -> dict[str, object]:
    """Parse XML formatted LLM response"""
    outputs = {}
    for field in schema.outputs:
        pattern = f"<{field.name.lower()}>(.*?)</{field.name.lower()}>"
        match = re.search(pattern, text, re.DOTALL)
        if not match:
            raise ValueError(f"Missing required output field: {field.name}")
        outputs[field.name] = field.type_(match.group(1).strip())
    return outputs


def parse_markdown(text: str, schema: Schema) -> dict[str, object]:
    """Parse Markdown formatted LLM response"""
    outputs = {}
    for field in schema.outputs:
        # Look for either bullet or header style outputs
        patterns = [
            rf"[*-] {field.name}:\s*(.*?)(?:\n|$)",  # Bullet format
            rf"\*\*{field.name}\*\*:\s*(.*?)(?:\n|$)",  # Bold format
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL)
            if match:
                outputs[field.name] = field.type_(match.group(1).strip())
                break
        if field.name not in outputs:
            raise ValueError(f"Missing required output field: {field.name}")
    return outputs


_PARSERS = {"xml": parse_xml, "markdown": parse_markdown}


def parse(text: str, schema: Schema, template_type: str = "") -> dict[str, object]:
    """Parse LLM response according to template type"""
    template_type = template_type or settings.get("template")
    if template_type not in _PARSERS:
        raise ValueError(
            f"Unknown template type: {template_type}. Must be one of: {', '.join(_PARSERS.keys())}"
        )
    parser = _PARSERS[template_type]
    return parser(text)
