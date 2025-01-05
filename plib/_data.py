"""
`Query`, `Response`, and `Example` represent different states in the lifecycle of an LLM interaction:
`Query` represents "what we want to know". It's a request waiting for an answer - like asking a question or describing a task. A Query must have values for all the input fields defined in its Schema. Think of it as the "question" part of a question-answer pair.

`Response` represents "what the LLM told us". It contains both the original Query (to maintain context) and the outputs the LLM generated. Every Response must have values for all the output fields defined in its Schema. Think of it as the "answer" part combined with the original question for context.

`Example` represents a complete Query-Response pair that we know worked well. We use Examples to teach the LLM through few-shot learning - showing it "here's a question like this, and here's how you answered it well before." Examples are the core teaching material we use to guide the LLM's behavior.

The key relationships:

* A Query becomes a Response after the LLM processes it
* A good Query-Response pair can become an Example for future use
* Examples are broken down into their Query and Response parts when used for teaching

This is why you'll often see functions taking a Query (asking something new) and a list of Examples (showing previous successful cases) to help guide the LLM to produce a good Response.
"""

import dataclasses
from typing import Type, Union

import beartype


@beartype.beartype
@dataclasses.dataclass(frozen=True)
class InputField:
    name: str
    type_: Union[type, Type]
    desc: str


@beartype.beartype
@dataclasses.dataclass(frozen=True)
class OutputField:
    name: str
    type_: type
    desc: str


@beartype.beartype
@dataclasses.dataclass(frozen=True)
class Schema:
    instruction: str
    inputs: list[InputField]
    outputs: list[OutputField]


@beartype.beartype
@dataclasses.dataclass(frozen=True)
class Query:
    """Holds input values that match a schema's input fields"""

    schema: Schema
    inputs: dict[str, object]

    def __post_init__(self):
        # Validate all schema inputs are provided
        missing = set(f.name for f in self.schema.inputs) - set(self.inputs.keys())
        if missing:
            raise ValueError(f"Missing required inputs: {missing}")

        # Validate input types
        for field in self.schema.inputs:
            if not isinstance(self.inputs[field.name], field.type_):
                raise TypeError(f"Input '{field.name}' must be {field.type_}")


@beartype.beartype
@dataclasses.dataclass(frozen=True)
class Response:
    """Holds output values produced by LLM that match a schema's output fields"""

    schema: Schema
    outputs: dict[str, object]

    def __post_init__(self):
        # Validate all schema outputs are provided
        missing = set(f.name for f in self.schema.outputs) - set(self.outputs.keys())
        if missing:
            raise ValueError(f"Missing required outputs: {missing}")

        # Validate output types
        for field in self.schema.outputs:
            if not isinstance(self.outputs[field.name], field.type_):
                raise TypeError(f"Output '{field.name}' must be {field.type_}")


@beartype.beartype
@dataclasses.dataclass(frozen=True)
class Example:
    """A complete input/output pair used for few-shot learning"""

    query: Query
    response: Response

    def __post_init__(self):
        # Validate query and response share same schema
        if self.query.schema != self.response.schema:
            raise ValueError("Query and Response must have same schema")

    @property
    def schema(self) -> Schema:
        return self.query.schema

    @classmethod
    def from_dicts(cls, schema: Schema, inputs: dict, outputs: dict) -> "Example":
        """Convenience constructor from raw dicts"""
        query = Query(schema, inputs)
        response = Response(schema, outputs)
        return cls(query, response)

    @property
    def inputs(self) -> dict:
        """Access input values"""
        return self.query.inputs

    @property
    def outputs(self) -> dict:
        """Access output values"""
        return self.response.outputs
