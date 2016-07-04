from parser import parse_program

def test_parsing_empty_program_fails():
    pass

def test_parses_single_number_program_okay():
    assert parse_program("808") == 808
    assert parse_program("-80877") == -80877

def test_parses_single_word_program_okay():
    assert parse_program("sel") == 'sel'
    assert parse_program(" le") == 'le'
    assert parse_program("rem") == 'rem'
    assert parse_program("    sub") == 'sub'
    assert parse_program("nget") == 'nget'

def test_parses_simple_list_okay():
    assert parse_program(("()")) == []
    assert parse_program("(1)") == [1]
    assert parse_program("(1 sub)") == [1, 'sub']
    assert parse_program("(1 sub 7 div rem)") == [1, 'sub', 7, 'div', 'rem']

def test_nested_expressions():
    assert parse_program("(())") == [[]]
    assert parse_program("((1 2) 3)") == [[1, 2], 3]
    assert parse_program("(sub (sub sub) exec ())") == ['sub', ['sub', 'sub'], 'exec', []]
    assert parse_program("(() ())") == [[], []]

def test_lexical_errors():
    pass

def test_premature_end_during_parsing():
    pass

