"""
Compilers optimize Modules by finding good few-shot examples for their Predict components
Modules form a tree structure:

Internal nodes are Modules that transform programs (CoT, BestOfN, etc.).
Leaf nodes are Predict modules that make actual LLM calls.
Only Predict nodes need examples/optimization.

Similar to PyTorch's parameters(), modules expose named_predicts() to find all Predict leaves.
Compilers are immutable - they return new optimized modules rather than modifying in place.
The core job of a compiler somehow modify Predict modules so they perform better.
"""

import abc
import collections.abc
import contextvars

import beartype

from ._data import Example, Response
from ._predict import Module

trace_stack = contextvars.ContextVar("trace_stack", default=None)


@beartype.beartype
class Metric(abc.ABC):
    """
    Describes how to score a given response with a reference gold example. Can use a plib.Module if you want!
    """

    async def score(self, gold: Example, response: Response) -> tuple[float, bool]:
        raise NotImplementedError()


@beartype.beartype
class Compiler(abc.ABC):
    """
    Abstract base class for compilers that optimize Module trees.

    Compilers can modify various aspects of modules to improve their performance:
    - Select good few-shot examples for Predict nodes
    - Modify prompt instructions
    - Transform schemas
    - Other optimizations

    Compilers are immutable - they return new optimized modules rather than modifying in place.
    """

    async def compile(
        self, module: Module, metric: Metric, dataset: collections.abc.Sequence[Example]
    ) -> Module:
        raise NotImplementedError()
