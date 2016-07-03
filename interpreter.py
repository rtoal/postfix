"""Simple interpreter for the PostFix language

"""


import operator

class Command(object):
    def __init__(self, value):
        self.value = value

    def execute(self, commands, stack):
        if isinstance(self.value, int) or isinstance(self.value, list):
            stack.append(self.value)
        elif self.value in ['le', 'lt', 'eq', 'ne', 'ge', 'gt']:
            _check_two_integers_on_top(stack)
            y = stack.pop()
            x = stack.pop()
            stack.append(1 if operator.__dict__[self.value](x, y) else 0)
        elif self.value in ['add', 'sub', 'mul', 'div', 'rem']:
            _check_two_integers_on_top(stack)
            y = stack.pop()
            x = stack.pop()
            op = 'mod' if self.value == 'rem' else self.value
            _check_not_dividing_by_zero(x, y)
            stack.append(operator.__dict__[op](x, y))
        elif self.value == 'pop':
            _check_minimum_length(stack, 1)
            stack.pop()
        elif self.value == 'swap':
            _check_minimum_length(stack, 2)
            stack[-1], stack[-2] = stack[-2], stack[-1]
        elif self.value == 'sel':
            _check_minimum_length(stack, 3)
            _check_integer_on_top(stack)
            condition = stack.pop()
            y = stack.pop()
            x = stack.pop()
            stack.append(x if condition else y)
        elif self.value == 'get':
            _check_integer_on_top(stack)
            index = stack.pop()
            _check_minimum_length(stack, index)
            stack.append(stack[~index])
        elif self.value == 'put':
            _check_minimum_length(stack, 2)
            _check_integer_on_top(stack)
            index = stack.pop()
            value = stack.pop()
            _check_minimum_length(stack, index)
            stack[~index] = value
        elif self.value == 'prs':
            _check_string_on_top(stack)
            print(stack.pop())
        elif self.value == 'pri':
            _check_integer_on_top(stack)
            print(stack.pop())
        elif self.value == 'exec':
            _check_command_list_on_top(stack)
            commands.extend(self.value)


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

def _check_command_list_on_top(stack):
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
        command.execute(commands, stack)
    program_result = stack[-1] if stack else None
    if debug:
        print('Returning', stack[-1])
    return program_result
