Module plib.templates
=====================

Sub-modules
-----------
* plib.templates.parsing
* plib.templates.templating

Functions
---------

`load(template_type: str = None) ‑> jinja2.environment.Template`
:   Get the appropriate template based on settings or override

`parse(text: str, schema: plib._data.Schema, template_type: str = '') ‑> dict[str, object]`
:   Parse LLM response according to template type