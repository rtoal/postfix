import unittest
from interpreter import run, Command

class TestInterpreter(unittest.TestCase):

    def test_average_works(self):
        program = [Command('add'), Command('INT', 2), Command('div')]
        self.assertEqual(run(program, [1, 1]), 1)
        self.assertEqual(run(program, [75, -25]), 25)
        self.assertEqual(run(program, [-30, -20]), -25)
        self.assertEqual(run(program, [6, 7]), 6)
