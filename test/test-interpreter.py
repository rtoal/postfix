import unittest
from interpreter import run, Command


def _(*args):
    return Command(*args)

class TestInterpreter(unittest.TestCase):

    # Initial programs from http://cs.wellesley.edu/~cs301/postfix.pdf
    def test_some_very_simple_programs(self):
        self.assertEqual(run([_('INT', 1), _('INT', 2), _('INT', 3)], []), 3)
        self.assertEqual(run([_('INT', 1), _('INT', 2), _('INT', 3), _('pop')], []), 2)
        self.assertEqual(run([_('INT', 1), _('INT', 2), _('swap'), _('INT', 3), _('pop')], []), 1)
        self.assertRaises(Exception, run, [_('swap')], [5])
        self.assertEqual(run([_('pop')], [17]), None)

    # Numerical operation examples from http://cs.wellesley.edu/~cs301/postfix.pdf
    def test_some_numerical_programs(self):
        self.assertEqual(run([_('INT', 3), _('INT', 4), _('sub')], []), -1)
        self.assertEqual(run([_('INT', 3), _('INT', 4), _('INT', 5), _('INT', 6), _('INT', 7),
            _('add'), _('mul'), _('sub'), _('swap'), _('div')], []), -21)
        self.assertEqual(run([_('INT', 3), _('INT', 4), _('add'), _('INT', 5), _('mul'),
            _('INT', 6), _('sub'), _('INT', 7), _('div')], []), 4)

        self.assertEqual(run([_('INT', 17), _('INT', 4), _('rem')], []), 1)
        self.assertEqual(run([_('INT', 3), _('INT', 4), _('lt')], []), 1)
        self.assertEqual(run([_('INT', 3), _('INT', 4), _('gt')], []), 0)
        self.assertEqual(run([_('INT', 3), _('INT', 4), _('lt'), _('INT', 10), _('add')], []), 11)


        self.assertRaises(Exception, run, [_('INT', 4), _('mul'), _('add')], [3])
        self.assertRaises(Exception, run, [_('INT', 4), _('sub'), _('div')], [3, 4])

    def test_average_works(self):
        program = [Command('add'), Command('INT', 2), Command('div')]
        self.assertEqual(run(program, [1, 1]), 1)
        self.assertEqual(run(program, [75, -25]), 25)
        self.assertEqual(run(program, [-30, -20]), -25)
        self.assertEqual(run(program, [6, 7]), 6)
