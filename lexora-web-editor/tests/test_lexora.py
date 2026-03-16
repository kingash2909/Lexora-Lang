import unittest
import os
import sys
import io
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from lexora.lexora import SimpleEnglishInterpreter

class TestLexora(unittest.TestCase):
    def setUp(self):
        self.interpreter = SimpleEnglishInterpreter()

    def test_display(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.interpreter.parse_and_execute('Display "Hello"')
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue().strip(), "Hello")

    def test_set_and_display(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.interpreter.execute_script(['Set X to 10', 'Display X'])
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue().strip(), "10")

    def test_if_block(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        script = [
            'Set X to 10',
            'If X is greater than 5:',
            '    Display "Large"',
            'End'
        ]
        self.interpreter.execute_script(script)
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue().strip(), "Large")

    def test_for_block(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        script = [
            'For i from 1 to 2:',
            '    Display i',
            'End'
        ]
        self.interpreter.execute_script(script)
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue().strip(), "1\n2")

    def test_add_subtract(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        script = [
            'Set Y to 20',
            'Add 5 to Y',
            'Display Y',
            'Subtract 10 from Y',
            'Display Y'
        ]
        self.interpreter.execute_script(script)
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue().strip(), "25\n15")

if __name__ == '__main__':
    unittest.main()
