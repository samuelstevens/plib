Module plib.compilers
=====================

Classes
-------

`BootstrapFewShot(n_examples: int = 3)`
:   Compiler that finds good few-shot examples by trying them on a dataset.
    
    For each successful run through the module:
    1. Captures traces from each Predict node
    2. If metric scores well, saves those traces as candidate examples
    3. Updates each Predict with its best examples
    
    # TODO: each Predict should use contextvars for its _trace attribute, so that you can trace in parallel.

    ### Ancestors (in MRO)

    * plib._compiling.Compiler
    * abc.ABC

    ### Methods

    `compile(self, module: plib._predict.Module, metric: plib._compiling.Metric, dataset: Sequence[plib._data.Example])`
    :