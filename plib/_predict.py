import collections.abc

import beartype

from . import settings, templates, _llms
from ._data import Example, Query, Response, Schema


@beartype.beartype
class Module:
    """Base class for LLM program transformations"""

    def __init__(self):
        self._modules = {}

    def register_module(self, name: str, module: "Module") -> None:
        """Registers a child module"""
        self._modules[name] = module

    def predicts(self) -> collections.abc.Iterator["Predict"]:
        """Returns an iterator over all Predict nodes in this module and children"""
        for module in self._modules.values():
            if module is not None:
                yield from module.predicts()

    def named_predicts(self) -> collections.abc.Iterator[tuple[str, "Predict"]]:
        """Returns an iterator over (name, predict) pairs for this module and children"""
        for name, module in self._modules.items():
            if module is not None:
                for subname, predict in module.named_predicts():
                    yield (f"{name}.{subname}" if subname else name), predict

    @property
    def schema(self) -> Schema:
        """The schema this module expects/produces"""
        if hasattr(self, "_schema") and isinstance(self._schema, Schema):
            return self._schema
        raise NotImplementedError

    async def __call__(self, query: Query) -> Response:
        resp = await self.forward(query)
        if not isinstance(resp, Response):
            raise TypeError(
                f"{self.__class__.__name__}({query}) produced {resp}, which is a {type(resp)}, not a Response."
            )

        return resp

    async def forward(self, query: Query) -> Response:
        """
        Transform the query according to module's logic.
        Example transformations:
        - Add reasoning steps (Chain of Thought)
        - Sample multiple responses (Best of N)
        - Run multi-step loops (ReAct)
        """
        raise NotImplementedError


@beartype.beartype
class Predict(Module):
    """Makes LLM calls using few-shot examples"""

    def __init__(self, schema: Schema, examples: list[Example] = None):
        """
        Args:
            schema: Defines input/output structure
            examples: Optional few-shot examples to use in prompts
        """
        super().__init__()
        self._schema: Schema = schema
        self.examples: list[Example] = examples or []

        self._trace: Example | None = None

    async def forward(self, query: Query) -> Response:
        """Make LLM call with few-shot examples"""
        template = templates.get_template()

        context = {
            "instruction": self.schema.instruction,
            "schema": {"inputs": self.schema.inputs, "outputs": self.schema.outputs},
            "examples": [
                {**example.inputs, **example.outputs} for example in self.examples
            ],
            "todo": query.inputs,
            "output_tags": ", ".join(f.name for f in self.schema.outputs),
        }

        # Render prompt
        prompt = template.render(**context)
        response_text, _ = await _llms.send(prompt)

        # Create Response object from LLM output
        response = Response(outputs={"text": response_text})

        # Create Example from query inputs and response outputs for tracing
        example = Example(inputs=query.inputs, outputs=response.outputs)

        if settings.get("trace"):
            self._trace = example

        return response

    def predicts(self) -> collections.abc.Iterator["Predict"]:
        """Returns an iterator over all Predict nodes in this module (just self for Predict)"""
        yield self

    def named_predicts(self) -> collections.abc.Iterator[tuple[str, "Predict"]]:
        """Returns an iterator over (name, predict) pairs (just self for Predict)"""
        yield "", self

    def add_example(self, example: Example):
        """Add a few-shot example"""
        self.examples.append(example)

    def clear_examples(self):
        """Remove all few-shot examples"""
        self.examples = []

    @property
    def trace(self) -> Example:
        if self._trace is None:
            raise ValueError(
                f"Missing trace. You need to call {self}(example) with plib.settings.context(trace=True) to record a trace."
            )

        return self._trace
