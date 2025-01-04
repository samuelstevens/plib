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
import typing

import beartype

from ._predict import Module
from ._data import Response, Example


@beartype.beartype
class Metric(abc.ABC):
    """
    Describes how to score
    """

    async def score(self, gold: Example, pred: Response) -> tuple[float, bool]:
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
        self, module: Module, metric: Metric, dataset: typing.Sequence[Example]
    ) -> Module:
        raise NotImplementedError()


@beartype.beartype
class BootstrapFewShot(Compiler):
    """
    A compiler that optimizes modules by bootstrapping few-shot examples.
    
    This compiler iteratively:
    1. Runs the module on a dataset to get predictions
    2. Scores the predictions using the metric
    3. Selects the best performing examples as few-shot examples
    4. Updates the module with these examples
    
    This bootstrapping process helps find effective few-shot examples
    that improve the module's performance on the given task.
    """
    pass
