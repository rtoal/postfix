from interpreter import run


def test_trivial_pushes_and_pops():
    assert run([1, 2, 3]) == 3
    assert run([1, 2, 3, 'pop']) == 2
    assert run([1, 2, 3, 'pop', 'pop']) == 1
    assert run([1, 'pop', 2, 3, 'pop']) == 2
    assert run([1, 'pop']) is None
    assert run(['pop'], 5) is None

def test_swaps():
    assert run(['swap'], 3, 4) == 4
    assert run(['pop', 'swap'], 3, 4, 5) == 5
    assert run([1, 2, 'swap', 3, 'pop']) == 1

def test_empty_program_returns_stack_top():
    assert run([], 3, 4) == 3

def test_insufficient_stack_sizes_are_detected():
    assert run(['swap'], 3) == 'STACK_SIZE_UNDER_2'
    assert run([4, 'mul', 'add'], 3) == 'STACK_SIZE_UNDER_2'
    assert run([1, 'ge']) == 'STACK_SIZE_UNDER_2'
    assert run(['pop']) == 'STACK_SIZE_UNDER_1'
    assert run([1, 'pop', 'pop']) == 'STACK_SIZE_UNDER_1'

def test_divide_by_zero_is_caught():
    assert run([2, 0, 'div']) == 'DIVIDE_BY_ZERO'
    assert run([4, 'sub', 'div'], 4, 5) == 'DIVIDE_BY_ZERO'

def test_arithmetic_commands():
    assert run([17, 4, 'rem']) == 1
    assert run([3, 4, 'sub']) == -1
    assert run([3, 4, 5, 6, 7, 'add', 'mul', 'sub', 'swap', 'div']) == -21
    assert run([3, 4, 'add', 5, 'mul', 6, 'sub', 7, 'div']) == 4

def test_relational_commands():
    assert run([3, 4, 'lt']) == 1
    assert run([3, 4, 'gt']) == 0
    assert run([4, 4, 'ge', 10, 'add']) == 11

def test_average_program_works():
    program = ['add', 2, 'div']
    assert run(program, 1, 1) == 1
    assert run(program, 75, -25) == 25
    assert run(program, -30, -20) == -25
    assert run(program, 6, 7) == 6

def test_some_programs_from_the_tetxbook():
    assert run([2, 3, 'sel'], 1) == 2
    assert run([2, 3, 'sel'], 0) == 3
    assert run([2, 3, 'sel'], 17) == 2
    assert run([[2, 'mul'], 3, 4, 'sel']) == 'INT_EXPECTED'
