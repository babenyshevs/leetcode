"""
LeetCode #69 - Sqrt(x) (Easy)

Given a non-negative integer x, return the square root of x rounded
down to the nearest integer. The returned integer should be non-negative
as well. Do not use any built-in exponent function or operator.

Example 1:
    Input: x = 4
    Output: 2
    Explanation: The square root of 4 is 2, so we return 2.

Example 2:
    Input: x = 8
    Output: 2
    Explanation: The square root of 8 is 2.82842..., and since we round
                 it down to the nearest integer, we return 2.

Constraints:
    0 <= x <= 2^31 - 1
"""

import unittest


class Solution:
    """Binary search — O(log x) time, O(1) space.

    We search for the largest integer `mid` such that `mid * mid <= x`
    in the range [0, x].  At each step we compare `mid * mid` with x:
      - If `mid * mid == x`, we found the exact square root.
      - If `mid * mid < x`, the answer is `mid` or higher — move `left`.
      - If `mid * mid > x`, the answer is strictly less — move `right`.

    We use `mid + 1` as the left bound when `mid * mid <= x` so that when
    the loop terminates, `right` points to the largest valid value.

    Note: `mid * mid` is computed via `mid * mid` directly. For 32-bit
    inputs the product fits comfortably in Python's arbitrary-precision
    integers, so there is no overflow concern.
    """

    def mySqrt(self, x: int) -> int:
        if x < 2:
            return x  # sqrt(0)=0, sqrt(1)=1

        left, right = 2, x // 2  # sqrt(x) <= x//2 for x >= 4

        while left <= right:
            mid = left + (right - left) // 2
            square = mid * mid

            if square == x:
                return mid
            elif square < x:
                left = mid + 1
            else:
                right = mid - 1

        return right  # `right` is the floor of sqrt(x)


class BuiltInSolution:
    """Python built-in approach — O(1) time, O(1) space.

    Uses `int(x ** 0.5)` which leverages Python's floating-point sqrt.
    Works for the given constraint range, but technically violates
    the "no built-in exponent" rule. Included for comparison only.
    """

    def mySqrt(self, x: int) -> int:
        return int(x ** 0.5)


class NewtonSolution:
    """Newton's method (Heron's method) — O(log x) time, O(1) space.

    Starting from an initial guess, iteratively refine using:
        next_guess = (guess + x / guess) / 2
    Converges quadratically — extremely fast for large inputs.
    We stop when successive guesses differ by less than 1.
    """

    def mySqrt(self, x: int) -> int:
        if x < 2:
            return x

        guess = x
        while guess * guess > x:
            guess = (guess + x // guess) // 2

        return guess


# --- Tests ---


class TestSqrtX(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()
        self.builtin = BuiltInSolution()
        self.newton = NewtonSolution()

    def test_example_1(self):
        self.assertEqual(self.sol.mySqrt(4), 2)

    def test_example_2(self):
        self.assertEqual(self.sol.mySqrt(8), 2)

    def test_zero(self):
        self.assertEqual(self.sol.mySqrt(0), 0)

    def test_one(self):
        self.assertEqual(self.sol.mySqrt(1), 1)

    def test_two(self):
        self.assertEqual(self.sol.mySqrt(2), 1)

    def test_perfect_square(self):
        self.assertEqual(self.sol.mySqrt(9), 3)
        self.assertEqual(self.sol.mySqrt(16), 4)
        self.assertEqual(self.sol.mySqrt(25), 5)
        self.assertEqual(self.sol.mySqrt(36), 6)
        self.assertEqual(self.sol.mySqrt(100), 10)
        self.assertEqual(self.sol.mySqrt(144), 12)

    def test_non_perfect_square(self):
        self.assertEqual(self.sol.mySqrt(3), 1)
        self.assertEqual(self.sol.mySqrt(5), 2)
        self.assertEqual(self.sol.mySqrt(10), 3)
        self.assertEqual(self.sol.mySqrt(26), 5)
        self.assertEqual(self.sol.mySqrt(50), 7)

    def test_large_perfect_square(self):
        # 46340^2 = 2147395600, largest perfect square <= 2^31-1
        self.assertEqual(self.sol.mySqrt(2147395600), 46340)

    def test_max_int(self):
        # 2^31 - 1 = 2147483647, floor(sqrt) = 46340
        self.assertEqual(self.sol.mySqrt(2147483647), 46340)

    def test_newton_matches_binary_search(self):
        for x in [0, 1, 2, 3, 4, 8, 9, 15, 16, 27, 100, 999, 10000, 2147395600]:
            self.assertEqual(
                self.sol.mySqrt(x),
                self.newton.mySqrt(x),
                f"Newton mismatch for x={x}",
            )

    def test_builtin_matches_binary_search(self):
        for x in [0, 1, 2, 3, 4, 8, 9, 15, 16, 27, 100, 999, 10000, 2147395600]:
            self.assertEqual(
                self.sol.mySqrt(x),
                self.builtin.mySqrt(x),
                f"Builtin mismatch for x={x}",
            )


if __name__ == "__main__":
    unittest.main()
