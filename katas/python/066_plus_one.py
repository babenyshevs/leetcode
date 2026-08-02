"""
LeetCode #66 - Plus One (Easy)

Given a non-empty array of decimal digits representing a non-negative
integer, increment the integer by one. The digits are stored such that
the most significant digit is at the head of the list, and each element
is a single digit. Return the resulting array of digits.

Example 1:
    Input: digits = [1,2,3]
    Output: [1,2,4]
    Explanation: The array represents the integer 123.
                 Incrementing by one gives 123 + 1 = 124.

Example 2:
    Input: digits = [4,3,2,1]
    Output: [4,3,2,2]
    Explanation: The array represents the integer 4321.
                 Incrementing by one gives 4321 + 1 = 4322.

Example 3:
    Input: digits = [9]
    Output: [1,0]
    Explanation: The array represents the integer 9.
                 Incrementing by one gives 9 + 1 = 10.

Constraints:
    1 <= digits.length <= 100
    0 <= digits[i] <= 9
    digits does not contain any leading 0's, except for the number 0 itself.
"""

import unittest


class Solution:
    """Reverse scan with carry — O(n) time, O(1) extra space.

    We simulate adding 1 starting from the least significant digit
    (rightmost) and propagate the carry leftward. If we carry past the
    most significant digit (e.g., 999 → 1000), we prepend a 1.

    This avoids converting to an integer, which would overflow for
    very large inputs, and works in a single pass from right to left.
    """

    def plusOne(self, digits: list[int]) -> list[int]:
        n = len(digits)

        # Work from right to left, adding carry
        for i in range(n - 1, -1, -1):
            if digits[i] < 9:
                digits[i] += 1
                return digits
            # Digit is 9 — it wraps to 0 and carry continues
            digits[i] = 0

        # If we exited the loop, all digits were 9 (e.g., 999 → 1000)
        return [1] + digits


class BuiltInSolution:
    """Conversion-based approach — O(n) time, O(n) space.

    Convert the digit list to an integer, add 1, then convert back
    to a list of digits. This is more readable but uses O(n) extra
    space and could overflow in languages without big integers.
    Python handles big integers natively, so this works here.
    """

    def plusOne(self, digits: list[int]) -> list[int]:
        num = 0
        for d in digits:
            num = num * 10 + d
        num += 1
        return [int(c) for c in str(num)]


# --- Tests ---


class TestPlusOne(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()
        self.builtin = BuiltInSolution()

    def test_example_1(self):
        self.assertEqual(self.sol.plusOne([1, 2, 3]), [1, 2, 4])

    def test_example_2(self):
        self.assertEqual(self.sol.plusOne([4, 3, 2, 1]), [4, 3, 2, 2])

    def test_example_3(self):
        self.assertEqual(self.sol.plusOne([9]), [1, 0])

    def test_single_digit_no_carry(self):
        self.assertEqual(self.sol.plusOne([5]), [6])

    def test_carry_in_middle(self):
        self.assertEqual(self.sol.plusOne([1, 9, 9]), [2, 0, 0])

    def test_all_nines(self):
        self.assertEqual(self.sol.plusOne([9, 9, 9]), [1, 0, 0, 0])

    def test_zero(self):
        self.assertEqual(self.sol.plusOne([0]), [1])

    def test_no_carry_at_all(self):
        self.assertEqual(self.sol.plusOne([1, 2, 4, 9, 0]), [1, 2, 4, 9, 1])

    def test_max_length_no_overflow(self):
        digits = [9] * 100
        result = self.sol.plusOne(digits)
        self.assertEqual(result[0], 1)
        self.assertEqual(len(result), 101)
        self.assertEqual(result[1:], [0] * 100)

    def test_builtin_matches_optimized(self):
        test_cases = [
            [1, 2, 3],
            [4, 3, 2, 1],
            [9],
            [1, 9, 9],
            [9, 9, 9],
            [0],
            [5],
            [1, 2, 4, 9, 0],
            [8, 9, 9, 9],
            [2, 5, 0, 0],
        ]
        for digits in test_cases:
            self.assertEqual(
                self.sol.plusOne(digits[:]),
                self.builtin.plusOne(digits[:]),
                f"Mismatch for input: {digits}",
            )


if __name__ == "__main__":
    unittest.main()
