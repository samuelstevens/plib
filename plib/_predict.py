import collections.abc

import beartype

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
        # Return self._schema if it's defined and is an instance of Schema, otherwise raise NotImplementedError. AI!
        raise NotImplementedError

    async def process(self, query: Query) -> Response:
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
        self._schema = schema
        self.examples = examples or []

    def schema(self) -> Schema
        return self

    async def __call__(self, query: Query) -> Response:
        """Make LLM call with few-shot examples"""
        pass

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
