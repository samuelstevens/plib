import asyncio

import plib.settings
from plib import (
    BootstrapFewShot,
    Example,
    InputField,
    Metric,
    OutputField,
    Predict,
    Query,
    Response,
    Schema,
)

# Define the schema for trivia QA
trivia_schema = Schema(
    instruction="Answer the trivia question accurately and concisely.",
    inputs=[InputField("question", str, "the trivia question")],
    outputs=[OutputField("answer", str, "the correct answer")],
)


# Define what makes a good answer (used by compiler to find examples)
class TriviaMetric(Metric):
    async def score(self, gold: Example, pred: Response) -> tuple[float, bool]:
        """Returns score and whether prediction is good enough to use as example"""
        # In practice, would compare against known correct answer
        # For now, just check answer isn't too long or too short
        answer = pred.outputs["answer"]
        score = 1.0 if 10 <= len(answer) <= 100 else 0.0
        return score, score > 0.9


# Create dataset of questions to learn from
dataset = [
    Example.from_dicts(
        trivia_schema,
        {"question": "What is the capital of France?"},
        {"answer": "Paris"},
    ),
    Example.from_dicts(
        trivia_schema,
        {"question": "Who wrote Romeo and Juliet?"},
        {"answer": "Shakespeare"},
    ),
    Example.from_dicts(
        trivia_schema,
        {"question": "What is the chemical symbol for gold?"},
        {"answer": "Au"},
    ),
]


async def main():
    plib.settings.configure(llm="ollama_chat/tulu3:8b")

    # Create base predictor
    predictor = Predict(trivia_schema)

    # Create compiler to find good examples
    compiler = BootstrapFewShot(n_examples=3)

    # Find good examples and add them to predictor
    metric = TriviaMetric()
    optimized_predictor = await compiler.compile(
        predictor, metric=metric, dataset=dataset
    )

    # Use the optimized predictor
    query = Query(
        trivia_schema, {"question": "Which planet is known as the Red Planet?"}
    )
    response = await optimized_predictor(query)
    print(f"Q: {query.inputs['question']}")
    print(f"A: {response.outputs['answer']}")


if __name__ == "__main__":
    asyncio.run(main())
