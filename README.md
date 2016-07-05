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

You can run the interpreter from the command line. Supply the program
as the first argument, with subsequent arguments (if any) comprising
the initial stack (starting with the top element):

```
$ ./postfix '((mul sub) (1 nget mul) 4 nget swap exec swap exec)' -10 2
42
```

You can also invoke the interpreter from within Python code like so:
 
```python
from interpreter import run
program = "((mul sub) (1 nget mul) 4 nget swap exec swap exec)"
run(command, -10, 2)
# => 42

```
