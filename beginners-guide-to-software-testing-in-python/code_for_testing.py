import unittest
import test_math_functions


class TestMathOps(unittest.TestCase):
    def test_number_check(self):
        # test case 1
        self.assertFalse(test_math_functions.is_not_a_number(7))
        # test case 2
        self.assertFalse(test_math_functions.is_not_a_number(7.1))
        # test case 3
        self.assertTrue(test_math_functions.is_not_a_number("HoneyBadger"))

    def test_addition(self):
        # test on basic operations
        self.assertEqual(test_math_functions.add(2, 3), 5)
        self.assertEqual(test_math_functions.add(-2, 3), 1)
        self.assertEqual(test_math_functions.add(0, 0), 0)
        # test case 1
        self.assertIsInstance(test_math_functions.add(3, 5), int)
        # test case 2
        self.assertIsInstance(test_math_functions.add(3.1, -5.7), float)
        # test case 3
        self.assertIsInstance(test_math_functions.add(3, 5.1), float)
        # test case 4
        self.assertRaises(TypeError, test_math_functions.add, "Honeybadger", 1117)

    def test_subtraction(self):
        # test on basic operations
        self.assertEqual(test_math_functions.subtract(2, 3), -1)
        self.assertEqual(test_math_functions.subtract(-2, 3), -5)
        self.assertEqual(test_math_functions.subtract(0, 0), 0)
        # test case 1
        self.assertIsInstance(test_math_functions.subtract(3, 5), int)
        # test case 2
        self.assertIsInstance(test_math_functions.subtract(3.1, -5.7), float)
        # test case 3
        self.assertIsInstance(test_math_functions.subtract(3, 5.1), float)
        # test case 4
        self.assertRaises(TypeError, test_math_functions.subtract, "Honeybadger", 1117)
        # test case 5
        self.assertLess(test_math_functions.subtract(3, 5), 0)

    def test_multiplication(self):
        # test case 1
        self.assertIsInstance(test_math_functions.multiply(3, 5), int)
        # test case 2
        self.assertIsInstance(test_math_functions.multiply(3.1, -5.7), float)
        # test case 3
        self.assertIsInstance(test_math_functions.multiply(3, 5.1), float)
        # test case 4
        self.assertRaises(TypeError, test_math_functions.multiply, "Honeybadger", 1117)
        # test case 5
        self.assertLessEqual(test_math_functions.multiply(3, -5), 0)
        # test case 6
        self.assertGreaterEqual(test_math_functions.multiply(3, 5), 0)
        # test case 7
        self.assertGreaterEqual(test_math_functions.multiply(-3, -5), 0)
        # test case 8
        self.assertEqual(test_math_functions.multiply(3, 0), 0)

    def test_division(self):
        # test basic operations
        self.assertEqual(test_math_functions.divide(6, 3), 2)
        self.assertEqual(test_math_functions.divide(-6, 3), -2)
        # test case 1
        self.assertIsInstance(test_math_functions.divide(6, 3), float)
        self.assertIsInstance(test_math_functions.divide(6, 2.5), float)
        self.assertIsInstance(test_math_functions.multiply(9.3, 3.1), float)
        # test case 2
        self.assertRaises(TypeError, test_math_functions.divide, "Honeybadger", 1117)
        # test case 3
        self.assertLessEqual(test_math_functions.divide(9.1, -3.1), 0)
        self.assertLessEqual(test_math_functions.divide(-9.1, 3.1), 0)
        # test case 4
        self.assertGreaterEqual(test_math_functions.divide(9.1, 3.1), 0)
        # test case 5
        self.assertGreaterEqual(test_math_functions.divide(-9.1, -3.1), 0)
        # test case 6
        self.assertRaises(ValueError, test_math_functions.divide, 5, 0)


if __name__ == '__main__':
    unittest.main()
