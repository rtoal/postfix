import re

TOKEN_REGEX = re.compile(
    r'\s*(-?\d+|\(|\)|(add|sub|mul|div|rem|eq|ne|lt|le|gt|ge|pop|swap|sel|nget|exec)(\b|$))')

def parse_program(source):
    tokens = tokenize(source)
    program = parse(tokens, next(tokens))
    if next(tokens) != 'END':
        raise ValueError('Extra text after end of program')
    return program

def parse(tokens, token):
    if token[0] in '-0123456789':
        return int(token)
    elif token == '(':
        token = next(tokens)   # consume '('
        result = []
        while token != ')':
            result.append(parse(tokens, token))
            token = next(tokens)
        return result
    elif token == ')':
        raise ValueError('Unexpected ")"')
    elif token == 'END':
        raise ValueError('Premature end of program')
    else:
        return token

def tokenize(source):
    start = 0
    while start < len(source):
        m = TOKEN_REGEX.match(source, start)
        if m is None:
            raise ValueError("Lexical Error")
        yield m.group(0).strip()
        start = m.end()
    yield 'END'
