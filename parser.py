import re

TOKEN_REGEX = re.compile(
    r'\s*(-?\d+|\(|\)|(add|sub|mul|div|rem|eq|ne|lt|le|gt|ge|pop|swap|sel|nget|exec)(\b|$))')

def parse_program(source):
    tokens = tokenize(source)
    result = parse(tokens)
    print(result)

def parse(tokens):
    result = []
    while True:
        token = next(tokens)
        if token[0] in '-0123456789':
            result.append(int(token))
        elif token == '(':
            command = parse(tokens)
            result.append(command)
        elif token in (')', 'END'):
            return result
        else:
            result.append(token)

def tokenize(source):
    start = 0
    while start < len(source):
        m = TOKEN_REGEX.match(source, start)
        if m is None:
            raise ValueError("Parse Error")
        yield m.group(0).strip()
        start = m.end()
    yield 'END'

