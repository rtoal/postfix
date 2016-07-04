"""Simple interpreter for the PostFix language"""

import operator


def execute(command, commands, stack):
    if isinstance(command, int) or isinstance(command, list):
        stack.append(command)
    elif command in ['le', 'lt', 'eq', 'ne', 'ge', 'gt', 'add', 'sub', 'mul', 'div', 'rem']:
        _check_integer(stack, 1)
        _check_integer(stack, 2)
        y = stack.pop()
        x = stack.pop()
        if command in ('div', 'rem'):
            _check_not_dividing_by_zero(command, y)
            command = {'div': 'floordiv', 'rem': 'mod'}[command]
        stack.append(int(operator.__dict__[command](x, y)))
    elif command == 'pop':
        _check_minimum_length(stack, 1)
        stack.pop()
    elif command == 'swap':
        _check_minimum_length(stack, 2)
        stack[-1], stack[-2] = stack[-2], stack[-1]
    elif command == 'sel':
        _check_integer(stack, 3)
        x = stack.pop()
        y = stack.pop()
        condition = stack.pop()
        stack.append(y if condition else x)
    elif command == 'nget':
        _check_integer(stack)
        index = stack.pop()
        _check_positive_integer(index)
        _check_minimum_length(stack, index)
        _check_integer(stack, index)           # Not allowed to access a non-int
        stack.append(stack[-index])
    elif command == 'put':
        _check_minimum_length(stack, 2)
        _check_integer(stack)
        index = stack.pop()
        value = stack.pop()
        _check_minimum_length(stack, index)
        stack[~index] = value
    elif command == 'exec':
        _check_list_on_top(stack)
        new_commands = stack.pop()
        commands[:0] = new_commands


def _check(condition, message):
    if not condition:
        raise ValueError(message)

def _check_minimum_length(stack, expected_length):
    _check(len(stack) >= expected_length, 'STACK_SIZE_UNDER_{}'.format(expected_length))

def _check_integer(stack, pos=1):
    _check_minimum_length(stack, pos)
    _check(isinstance(stack[-pos], int), 'INT_EXPECTED')

def _check_positive_integer(n):
    _check(isinstance(n, int) and n >= 1, 'POSITIVE_INT_EXPECTED')

def _check_list_on_top(stack):
    _check_minimum_length(stack, 1)
    _check(isinstance(stack[-1], list), 'LIST_EXPECTED')

def _check_not_dividing_by_zero(command, divisor):
    _check(command not in ('div','rem') or divisor != 0, 'DIVIDE_BY_ZERO')


def run(commands, *stack):
    try:
        commands = commands[:]
        stack = list(reversed(stack))
        while commands:
            print('C', list(commands), 'S', list(stack))
            command = commands.pop(0)
            execute(command, commands, stack)
        return 'NO_RESULT' if not stack else 'NON_INT_RESULT' if not isinstance(stack[-1], int) else stack[-1]
    except ValueError as e:
        return str(e)
