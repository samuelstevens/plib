# plib

The key insight of plib is that selecting good examples (few-shot learning) is often more effective than spending time crafting the perfect zero-shot prompt.

## Components:

Schemas

* Simple definitions of input/output structure
* Just ordered lists of fields with types and descriptions
* Easy to modify and compose
* No complex inheritance or class magic

Predict Module

* Main interface for making LLM calls
* Takes a schema and optional examples
* Examples are just input/output pairs used in prompt construction
* Simple interface: inputs -> outputs

Program Logic Modules

* Transform the basic predict/response flow
* Examples: Chain of Thought adds reasoning steps, Best-of-N samples multiple responses
* Focus on defining logical transformations, not prompt engineering
* Think of them like regular programming constructs (loops, conditionals, etc.)

Compilers

* Find and select good examples automatically
* BootstrapFewShot runs predictions and saves successful examples
* Separate example selection from program logic
* Let users develop different strategies for finding good examples

The big idea is separation of concerns:

* Schemas define structure
* Predict handles LLM interaction
* Modules define program flow
* Compilers handle example selection

This makes the system more modular and easier to extend - users can add new modules without worrying about example selection, or create new compilers without touching program logic.
