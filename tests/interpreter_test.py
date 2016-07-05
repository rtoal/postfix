from interpreter import run


def test_trivial_pushes_and_pops():
    assert run('(1 2 3)') == 3
    assert run('(1 2 3 pop)') == 2
    assert run('(1 2 3 pop pop)') == 1
    assert run('(1 pop 2 3 pop)') == 2
    assert run('(1 pop)') == 'NO_RESULT'
    assert run('(pop)', 5) == 'NO_RESULT'

def test_swaps():
    assert run('(swap)', 3, 4) == 4
    assert run('(pop swap)', 3, 4, 5) == 5
    assert run('(1 2 swap 3 pop)') == 1

def test_empty_program_returns_stack_top():
    assert run('()', 3, 4) == 3

def test_insufficient_stack_sizes_are_detected():
    assert run('(swap)', 3) == 'STACK_SIZE_UNDER_2'
    assert run('(1 ge)') == 'STACK_SIZE_UNDER_2'
    assert run('(pop)') == 'STACK_SIZE_UNDER_1'
    assert run('(1 pop pop)') == 'STACK_SIZE_UNDER_1'

def test_divide_by_zero_is_caught():
    assert run('(2 0 div)') == 'DIVIDE_BY_ZERO'
    assert run('(4 sub div)', 4, 5) == 'DIVIDE_BY_ZERO'
    assert run('(4 sub rem)', 4, 5) == 'DIVIDE_BY_ZERO'

def test_arithmetic_commands():
    assert run('(4 sub)', 3) == -1
    assert run('(4 add 5 mul 6 sub 7 div)', 3) == 4
    assert run('(add mul sub swap div)', 7, 6, 5, 4, 3) == -21
    assert run('(4000 swap pop add)', 300, 20, 1) == 4020
    assert run('(3 div)', 17) == 5
    assert run('(3 rem)', 17) == 2
    assert run('(4 mul add)', 3) == 'STACK_SIZE_UNDER_2'

def test_relational_commands():
    assert run('(4 lt)', 3) == 1
    assert run('(4 lt)', 5) == 0
    assert run('(4 lt 10 add)', 3) == 11
    assert run('(3 (2 mul) gt)') == 'INT_EXPECTED'

def test_average_program_works():
    program = '(add 2 div)'
    assert run(program, 1, 1) == 1
    assert run(program, 75, -25) == 25
    assert run(program, -30, -20) == -25
    assert run(program, 6, 7) == 6

def test_nget_cases():
    assert run('(1 nget)', 4, 5) == 4
    assert run('(2 nget)', 4, 5) == 5
    assert run('(3 nget)', 4, 5) == 'STACK_SIZE_UNDER_3'
    assert run('(0 nget)', 4, 5) == 'POSITIVE_INT_EXPECTED'
    assert run('((2 mul) 1 nget)', 3) == 'INT_EXPECTED'

def test_ax_plus_by_plus_c():
    program = '(4 nget 5 nget mul mul swap 4 nget mul add add)'
    assert run(program, 3, 4, 5, 2) == 25

def test_absolute_value():
    program = '(1 nget 0 lt (0 swap sub) () sel exec)'
    assert run(program, -7) == 7
    assert run(program, 7) == 7
    assert run(program, 7, 8, 9) == 7

def test_some_programs_from_the_tetxbook():
    assert run('((2 mul) exec)', 7) == 14
    assert run('((0 swap sub) 7 swap exec)') == -7
    assert run('(2 3 sel)', 1) == 2
    assert run('(2 3 sel)', 0) == 3
    assert run('(2 3 sel)', 17) == 2
    assert run('((2 mul) 3 4 sel)') == 'INT_EXPECTED'
    assert run('(lt (add) (mul) sel exec)', 3, 4, 5, 6) == 30
    assert run('(lt (add) (mul) sel exec)', 4, 3, 5, 6) == 11
    assert run('((7 swap exec) (0 swap sub) swap exec)') == -7
    assert run('((mul sub) (1 nget mul) 4 nget swap exec swap exec)', -10, 2) == 42

def test_exec_requires_list():
    assert run('(3 exec)') == 'LIST_EXPECTED'

def test_non_integer_result_is_detected():
    assert run('((2 mul))') == 'NON_INT_RESULT'

def test_parser_errors_are_detected():
    assert run('') == 'PREMATURE_END_OF_PROGRAM'
    assert run('(mul') == 'PREMATURE_END_OF_PROGRAM'
    assert run('(mulz)') == 'LEXICAL_ERROR'
    assert run('(mul4)') == 'LEXICAL_ERROR'
    assert run('(mul,4)') == 'LEXICAL_ERROR'
    assert run(')') == 'UNEXPECTED_RIGHT_PAREN'
    assert run('(3 4 add ) sub)') == 'EXTRA_PROGRAM_TEXT'


