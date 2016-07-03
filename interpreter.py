"""Simple interpreter for the PostFix language

"""


import operator

def execute(command, commands, stack):
    if isinstance(command, int) or isinstance(command, list):
        stack.append(command)
    elif command in ['le', 'lt', 'eq', 'ne', 'ge', 'gt', 'add', 'sub', 'mul', 'div', 'rem']:
        _check_two_integers_on_top(stack)
        y = stack.pop()
        x = stack.pop()
        if command in ('div', 'rem'):
            command = 'floordiv' if command == 'div' else 'mod'
            _check_not_dividing_by_zero(x, y)
        stack.append(int(operator.__dict__[command](x, y)))
    elif command == 'pop':
        _check_minimum_length(stack, 1)
        stack.pop()
    elif command == 'swap':
        _check_minimum_length(stack, 2)
        stack[-1], stack[-2] = stack[-2], stack[-1]
    elif command == 'sel':
        _check_minimum_length(stack, 3)
        _check_integer_on_top(stack)
        condition = stack.pop()
        y = stack.pop()
        x = stack.pop()
        stack.append(x if condition else y)
    elif command == 'get':
        _check_integer_on_top(stack)
        index = stack.pop()
        _check_minimum_length(stack, index)
        stack.append(stack[~index])
    elif command == 'put':
        _check_minimum_length(stack, 2)
        _check_integer_on_top(stack)
        index = stack.pop()
        value = stack.pop()
        _check_minimum_length(stack, index)
        stack[~index] = value
    elif command == 'prs':
        _check_string_on_top(stack)
        print(stack.pop())
    elif command == 'pri':
        _check_integer_on_top(stack)
        print(stack.pop())
    elif command == 'exec':
        _check_list_on_top(stack)
        commands.extend(command)


def _check(condition, message):
    if not condition:
        raise(Exception, message)

def _check_minimum_length(stack, expected_length):
    _check(len(stack) >= expected_length, 'Expected stack to have {} items'.format(expected_length))

def _check_two_integers_on_top(stack):
    _check_minimum_length(stack, 2)
    _check_integer_on_top(stack)
    _check(isinstance(stack[-2], int), 'Expected integer just below top of stack')

def _check_integer_on_top(stack):
    _check_minimum_length(stack, 1)
    _check(isinstance(stack[1], int), 'Expected integer on top of stack')

def _check_string_on_top(stack):
    _check_minimum_length(stack, 1)
    _check(isinstance(stack[-1], str), 'Expected string on top of stack')

def _check_list_on_top(stack):
    _check_minimum_length(stack, 1)
    _check(isinstance(stack[-1], list), 'Expected command list on top of stack')

def _check_not_dividing_by_zero(command, divisor):
    _check(command not in ('div','rem') or divisor != 0, 'Divide by zero error')


def run(commands, stack, debug=False):
    commands = commands[:]
    while commands:
        if debug:
            print('Commands:', commands)
            print('Stack', stack)
            print('--------')
        command = commands.pop(0)
        execute(command, commands, stack)
    program_result = stack[-1] if stack else None
    if debug:
        print('Returning', stack[-1])
    return program_result
