"""Simple interpreter for the PostFix language

"""


import operator

class Command(object):
    def __init__(self, kind, argument=None):
        self.kind = kind
        self.argument = argument

    def __repr__(self):
        return self.kind + (' ' + str(self.argument) if self.argument else '')

    def execute(self, commands, stack):
        if self.kind in ('STRING', 'INT', 'SEQUENCE'):
            stack.append(self.argument)
        elif self.kind in ['le', 'lt', 'eq', 'ne', 'ge', 'gt']:
            _check_two_integers_on_top(stack)
            y = stack.pop()
            x = stack.pop()
            stack.append(1 if operator.__dict__[self.kind](x, y) else 0)
        elif self.kind in ['add', 'sub', 'mul', 'div', 'rem']:
            _check_two_integers_on_top(stack)
            y = stack.pop()
            x = stack.pop()
            op = 'mod' if self.kind == 'rem' else self.kind
            _check_not_dividing_by_zero(x, y)
            stack.append(operator.__dict__[op](x, y))
        elif self.kind == 'pop':
            _check_minimum_length(stack, 1)
            stack.pop()
        elif self.kind == 'swap':
            _check_minimum_length(stack, 2)
            stack[-1], stack[-2] = stack[-2], stack[-1]
        elif self.kind == 'sel':
            _check_minimum_length(stack, 3)
            _check_integer_on_top(stack)
            condition = stack.pop()
            y = stack.pop()
            x = stack.pop()
            stack.append(x if condition else y)
        elif self.kind == 'get':
            _check_integer_on_top(stack)
            index = stack.pop()
            _check_minimum_length(stack, index)
            stack.append(stack[~index])
        elif self.kind == 'put':
            _check_minimum_length(stack, 2)
            _check_integer_on_top(stack)
            index = stack.pop()
            value = stack.pop()
            _check_minimum_length(stack, index)
            stack[~index] = value
        elif self.kind == 'prs':
            _check_string_on_top(stack)
            print stack.pop()
        elif self.kind == 'pri':
            _check_integer_on_top(stack)
            print stack.pop()
        elif self.kind == 'exec':
            _check_command_list_on_top(stack)
            commands.extend(self.argument)


def _check(condition, message):
    if not condition:
        raise(Exception, message)

def _check_minimum_length(stack, expected_length):
    _check(len(stack) >= expected_length, 'Expected stack to have %d items' % expected_length)

def _check_two_integers_on_top(stack):
    _check_minimum_length(stack, 2)
    _check_integer_on_top(stack)
    _check(type(stack[-2]) in (int, long), 'Expected integer just below top of stack')

def _check_integer_on_top(stack):
    _check_minimum_length(stack, 1)
    _check(type(stack[-1]) in (int, long), 'Expected integer on top of stack')

def _check_string_on_top(stack):
    _check_minimum_length(stack, 1)
    _check(type(stack[-1]) in (str, unicode), 'Expected string on top of stack')

def _check_command_list_on_top(stack):
    _check_minimum_length(stack, 1)
    _check(stack[-1].isinstance(Command) and stack[-1].kind == 'SEQUENCE',
        'Expected command list on top of stack')

def _check_not_dividing_by_zero(kind, divisor):
    _check(kind not in ('div','rem') or divisor != 0, 'Divide by zero error')


def run(commands, stack, debug=False):
    commands = commands[:]
    while commands:
        if debug:
            print 'Commands:', commands
            print 'Stack', stack
            print '--------'
        command = commands.pop(0)
        command.execute(commands, stack)
    program_result = stack[-1] if stack else None
    if debug:
        print 'Returning', stack[-1]
    return program_result
