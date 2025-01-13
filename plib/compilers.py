import collections
import copy

from . import settings
from ._compiling import Compiler, Metric
from ._data import Example
from ._predict import Module


class BootstrapFewShot(Compiler):
    """Compiler that finds good few-shot examples by trying them on a dataset.

    For each successful run through the module:
    1. Captures traces from each Predict node
    2. If metric scores well, saves those traces as candidate examples
    3. Updates each Predict with its best examples

    # TODO: each Predict should use contextvars for its _trace attribute, so that you can trace in parallel.
    """

    def __init__(self, n_examples: int = 3):
        self.n_examples: int = n_examples

    async def compile(
        self, module: Module, metric: Metric, dataset: collections.abc.Sequence[Example]
    ):
        optimized = copy.deepcopy(module)
        candidate_examples: dict[str, list[tuple[Example, float]]] = (
            collections.defaultdict(list)
        )

        # Try each example in dataset
        for example in dataset:
            # Set tracing on to capture the full interaction
            with settings.context(trace=True):
                try:
                    # Make prediction with full module
                    response = await module(example.query)

                    # Score the prediction
                    score, is_good = await metric.score(example, response)

                    if is_good:
                        # If good, collect traces from all Predicts
                        for name, predict in module.named_predicts():
                            # Each predict's trace is an Example we can use
                            candidate_examples[name].append((predict.trace, score))

                except Exception as e:
                    print(f"Error processing example: {e}")
                    continue

        if not candidate_examples:
            raise ValueError("No good examples found in dataset")

        # For each Predict node, select its best examples
        for name, predict in optimized.named_predicts():
            predict.clear_examples()

            # Sort candidate examples by score
            candidates = candidate_examples[name]
            best_examples = sorted(
                candidates,
                key=lambda x: x[1],  # sort by score
                reverse=True,
            )[: self.n_examples]

            # Add best examples to the predict
            for example, _ in best_examples:
                predict.add_example(example)

        return optimized
