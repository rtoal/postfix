import pytest
from interpreter import run


def test_trivial_pushes_and_pops():
    assert run([1, 2, 3], []) == 3
    assert run([1, 2, 3, 'pop'], []) == 2
    assert run([1, 2, 3, 'pop', 'pop'], []) == 1
    assert run([1, 'pop', 2, 3, 'pop'], []) == 2
    assert run([1, 'pop'], []) is None
    assert run(['pop'], [5]) is None

def test_exception_raised_when_stack_not_big_enough():
    tests = [
        (['swap'], [5]),
        ([4, 'mul', 'add'], [3]),
        ([4, 'sub', 'div'], [3, 4]),
        ]
    for program, stack in tests:
        with pytest.raises(Exception):
            run(program, stack)

def test_arithmetic_commands():
    assert run([17, 4, 'rem'], []) == 1
    assert run([3, 4, 'sub'], []) == -1
    assert run([3, 4, 5, 6, 7, 'add', 'mul', 'sub', 'swap', 'div'], []) == -21
    assert run([3, 4, 'add', 5, 'mul', 6, 'sub', 7, 'div'], []) == 4

def test_relational_commands():
    assert run([3, 4, 'lt'], []) == 1
    assert run([3, 4, 'gt'], []) == 0
    assert run([4, 4, 'ge', 10, 'add'], []) == 11

def test_average_program_works():
    program = ['add', 2, 'div']
    assert run(program, [1, 1]) == 1
    assert run(program, [75, -25]) == 25
    assert run(program, [-30, -20]) == -25
    assert run(program, [6, 7]) == 6
