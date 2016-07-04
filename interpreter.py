"""Simple interpreter for the PostFix language"""

import operator


def execute(command, commands, stack):
    if isinstance(command, int) or isinstance(command, list):
        stack.append(command)
    elif command in 'le lt eq ne ge gt add sub mul div rem'.split():
        _check_minimum_length(stack, 2)
        _check_integer(stack[-1])
        _check_integer(stack[-2])
        y = stack.pop()
        x = stack.pop()
        if command in ('div', 'rem'):
            _check_non_zero(y)
            command = {'div': 'floordiv', 'rem': 'mod'}[command]
        stack.append(int(operator.__dict__[command](x, y)))
    elif command == 'pop':
        _check_minimum_length(stack, 1)
        stack.pop()
    elif command == 'swap':
        _check_minimum_length(stack, 2)
        stack[-1], stack[-2] = stack[-2], stack[-1]
    elif command == 'sel':
        _check_minimum_length(stack, 3)
        _check_integer(stack[-3])
        x = stack.pop()
        y = stack.pop()
        condition = stack.pop()
        stack.append(y if condition else x)
    elif command == 'nget':
        _check_minimum_length(stack, 1)
        _check_integer(stack[-1])
        index = stack.pop()
        _check_positive_integer(index)
        _check_minimum_length(stack, index)
        _check_integer(stack[-index])           # Not allowed to access a non-int
        stack.append(stack[-index])
    elif command == 'exec':
        _check_minimum_length(stack, 1)
        _check_list(stack[-1])
        commands[:0] = stack.pop()


def _check(condition, message):
    if not condition:
        raise ValueError(message)

def _check_minimum_length(stack, expected_length):
    _check(len(stack) >= expected_length, 'STACK_SIZE_UNDER_{}'.format(expected_length))

def _check_integer(value):
    _check(isinstance(value, int), 'INT_EXPECTED')

def _check_non_zero(value):
    _check(value != 0, 'DIVIDE_BY_ZERO')

def _check_positive_integer(value):
    _check(isinstance(value, int) and value >= 1, 'POSITIVE_INT_EXPECTED')

def _check_list(value):
    _check(isinstance(value, list), 'LIST_EXPECTED')

def run(commands, *stack):
    try:
        commands = commands[:]
        stack = list(reversed(stack))
        while commands:
            command = commands.pop(0)
            execute(command, commands, stack)
        return 'NO_RESULT' if not stack else 'NON_INT_RESULT' if not isinstance(stack[-1], int) else stack[-1]
    except ValueError as e:
        return str(e)
