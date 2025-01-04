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
import copy
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

    def __init__(self, n_examples: int = 3):
        """Initialize the compiler with configuration parameters

        Args:
            n_examples: Number of examples to select for few-shot learning
        """
        self.n_examples = n_examples

    async def compile(
        self, module: Module, metric: Metric, dataset: typing.Sequence[Example]
    ) -> Module:
        """Optimize the module by finding good few-shot examples

        Args:
            module: The module to optimize
            metric: Metric for scoring predictions
            dataset: Examples to learn from

        Returns:
            New optimized module with selected examples
        """

        # Create a copy of the module to avoid modifying the original
        optimized = copy.deepcopy(module)

        # Get all Predict nodes in the module tree
        predicts = module.get_predicts()
        if not predicts:
            return optimized  # No Predict nodes to optimize

        # Initialize empty set of candidate examples
        candidate_examples = []

        # Bootstrap process:
        # Process examples in parallel until we have enough candidates
        async def process_example(example):
            pred = await optimized.process(example.query)
            _, is_good = await metric.score(example, pred)
            return example if is_good else None

        candidate_examples = []
        async with asyncio.TaskGroup() as tg:
            # Create task for each example
            tasks = [tg.create_task(process_example(ex)) for ex in dataset]
            
            # Wait for tasks and collect results until we have enough
            for task in asyncio.as_completed(tasks):
                try:
                    result = await task
                    if result is not None:
                        candidate_examples.append(result)
                        if len(candidate_examples) >= self.n_examples:
                            # Cancel remaining tasks once we have enough examples
                            for t in tasks:
                                if not t.done():
                                    t.cancel()
                            break
                except asyncio.CancelledError:
                    pass

        # Select best examples from candidates
        selected_examples = self._select_examples(candidate_examples)

        # Update each Predict node with selected examples
        for predict in predicts:
            predict.clear_examples()
            for example in selected_examples:
                predict.add_example(example)

        return optimized
