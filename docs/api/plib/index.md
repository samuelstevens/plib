Module plib
===========

Sub-modules
-----------
* plib.compilers
* plib.settings
* plib.templates

Classes
-------

`BootstrapFewShot(n_examples: int = 3)`
:   Compiler that finds good few-shot examples by trying them on a dataset.
    
    For each successful run through the module:
    1. Captures traces from each Predict node
    2. If metric scores well, saves those traces as candidate examples
    3. Updates each Predict with its best examples

    ### Ancestors (in MRO)

    * plib._compiling.Compiler
    * abc.ABC

    ### Methods

    `compile(self, module: plib._predict.Module, metric: plib._compiling.Metric, dataset: Sequence[plib._data.Example])`
    :

`Compiler()`
:   Abstract base class for compilers that optimize Module trees.
    
    Compilers can modify various aspects of modules to improve their performance:
    - Select good few-shot examples for Predict nodes
    - Modify prompt instructions
    - Transform schemas
    - Other optimizations
    
    Compilers are immutable - they return new optimized modules rather than modifying in place.

    ### Ancestors (in MRO)

    * abc.ABC

    ### Descendants

    * plib.compilers.BootstrapFewShot

    ### Methods

    `compile(self, module: plib._predict.Module, metric: plib._compiling.Metric, dataset: Sequence[plib._data.Example]) ‑> plib._predict.Module`
    :

`Example(query: plib._data.Query, response: plib._data.Response)`
:   A complete input/output pair used for few-shot learning

    ### Class variables

    `query: plib._data.Query`
    :   The type of the None singleton.

    `response: plib._data.Response`
    :   The type of the None singleton.

    ### Static methods

    `from_dicts(cls, schema: plib._data.Schema, inputs: dict, outputs: dict) ‑> plib._data.Example`
    :   Convenience constructor from raw dicts

    ### Instance variables

    `inputs: dict`
    :   Access input values

    `outputs: dict`
    :   Access output values

    `schema: plib._data.Schema`
    :

`InputField(name: str, type_: type, desc: str)`
:   InputField(name: str, type_: type, desc: str)

    ### Class variables

    `desc: str`
    :   The type of the None singleton.

    `name: str`
    :   The type of the None singleton.

    `type_: type`
    :   The type of the None singleton.

`Metric()`
:   Describes how to score a given response with a reference gold example. Can use a plib.Module if you want!

    ### Ancestors (in MRO)

    * abc.ABC

    ### Methods

    `score(self, gold: plib._data.Example, response: plib._data.Response) ‑> tuple[float, bool]`
    :

`Module()`
:   Base class for LLM program transformations

    ### Descendants

    * plib._predict.Predict

    ### Instance variables

    `schema: plib._data.Schema`
    :   The schema this module expects/produces

    ### Methods

    `forward(self, query: plib._data.Query) ‑> plib._data.Response`
    :   Transform the query according to module's logic.
        Example transformations:
        - Add reasoning steps (Chain of Thought)
        - Sample multiple responses (Best of N)
        - Run multi-step loops (ReAct)

    `named_predicts(self) ‑> Iterator[tuple[str, plib._predict.Predict]]`
    :   Returns an iterator over (name, predict) pairs for this module and children

    `predicts(self) ‑> Iterator[plib._predict.Predict]`
    :   Returns an iterator over all Predict nodes in this module and children

    `register_module(self, name: str, module: Module) ‑> None`
    :   Registers a child module

`OutputField(name: str, type_: type, desc: str)`
:   OutputField(name: str, type_: type, desc: str)

    ### Class variables

    `desc: str`
    :   The type of the None singleton.

    `name: str`
    :   The type of the None singleton.

    `type_: type`
    :   The type of the None singleton.

`Predict(schema: plib._data.Schema, examples: list[plib._data.Example] = None)`
:   Makes LLM calls using few-shot examples
    
    Args:
        schema: Defines input/output structure
        examples: Optional few-shot examples to use in prompts

    ### Ancestors (in MRO)

    * plib._predict.Module

    ### Instance variables

    `trace: plib._data.Example`
    :

    ### Methods

    `add_example(self, example: plib._data.Example)`
    :   Add a few-shot example

    `clear_examples(self)`
    :   Remove all few-shot examples

    `forward(self, query: plib._data.Query) ‑> plib._data.Response`
    :   Make LLM call with few-shot examples

    `named_predicts(self) ‑> Iterator[tuple[str, plib._predict.Predict]]`
    :   Returns an iterator over (name, predict) pairs (just self for Predict)

    `predicts(self) ‑> Iterator[plib._predict.Predict]`
    :   Returns an iterator over all Predict nodes in this module (just self for Predict)

`Query(schema: plib._data.Schema, inputs: dict[str, object])`
:   Holds input values that match a schema's input fields

    ### Class variables

    `inputs: dict[str, object]`
    :   The type of the None singleton.

    `schema: plib._data.Schema`
    :   The type of the None singleton.

`Response(schema: plib._data.Schema, outputs: dict[str, object])`
:   Holds output values produced by LLM that match a schema's output fields

    ### Class variables

    `outputs: dict[str, object]`
    :   The type of the None singleton.

    `schema: plib._data.Schema`
    :   The type of the None singleton.

`Schema(instruction: str, inputs: list[plib._data.InputField], outputs: list[plib._data.OutputField])`
:   Schema(instruction: str, inputs: list[plib._data.InputField], outputs: list[plib._data.OutputField])

    ### Class variables

    `inputs: list[plib._data.InputField]`
    :   The type of the None singleton.

    `instruction: str`
    :   The type of the None singleton.

    `outputs: list[plib._data.OutputField]`
    :   The type of the None singleton.