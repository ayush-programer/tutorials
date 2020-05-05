# Python3 Unit Test Examples

import unittest

def fibonacci_step(prev, curr, step, step_max):
    if step == step_max:
        return curr
    else:
        return fibonacci_step(curr, prev+curr, step + 1, step_max)

def fibonacci(n):
    return fibonacci_step(0, 1, 1, n)

class SomeTestCase(unittest.TestCase):
    """Tests for fibonacci() function"""

    def setUp(self):
        self.fibonacci_list = [ 1, 1, 2, 3, 5, 8, 13, 21, 34 ]

# Note: The setUp method will be run first on unittest.main()

    def test_fibonacci_first(self):
        for index, fib_num in enumerate(self.fibonacci_list, start=1):
            self.assertEqual(fibonacci(index), fib_num)

# Note: The opposite of this is assertNotEqual

    def test_fibonacci_second(self):
        for fib_num in [ fibonacci(n) for n in range(1, len(self.fibonacci_list) + 1) ]:
            self.assertIn(fib_num, self.fibonacci_list)

# Note: The opposite of this is assertNotIn

    def test_fibonacci_third(self):
        fib_list = [ fibonacci(n) for n in range(1, len(self.fibonacci_list) + 1) ]
        prev1 = fib_list[0]
        prev2 = fib_list[1]
        for fib_index in range(2, len(fib_list)):
            self.assertTrue(prev1 + prev2 == fib_list[fib_index])
            prev1 = prev2
            prev2 = fib_list[fib_index]

# Note: The opposite of this is assertFalse

unittest.main()

# Note: Tests will be run for any method starting with test_ prefix
