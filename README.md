# PostFix

An interpreter for the Turbak and Gifford's language PostFix.
PostFix is a stack-based language described in Chapter 1 of the 
book [Design Concepts in Programming 
Languages](https://mitpress.mit.edu/books/design-concepts-programming-languages).

The interpreter is written in Python 3, with a test suite runnable
with [py.test](http://pytest.org/latest/). After cloning this 
repo, run the tests with something like:

```
python3 -m pytest -s -v tests
```

To run the interpreter:

```python
from interpreter import run
command = [['mul', 'sub'], [1, 'nget', 'mul'], 4, 'nget', 'swap', 'exec', 'swap', 'exec']]
run(command, -10, 2)
# => 42

```

The interpreter runs a list of commands on an initial stack, given as
the second to last arguments of `run`, with the top of the stack first.
You can also run a text-based program like so:
 
```python
from interpreter import run
program = "((mul sub) (1 nget mul) 4 nget swap exec swap exec)"
run(command, -10, 2)
# => 42

```
