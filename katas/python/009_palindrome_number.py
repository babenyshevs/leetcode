"""
LeetCode #9 - Palindrome Number (Easy)

Given an integer x, return true if x is a palindrome, and false otherwise.

An integer is a palindrome when it reads the same forward and backward.

Example 1:
    Input: x = 121
    Output: true
    Explanation: 121 reads as 121 from left to right and from right to left.

Example 2:
    Input: x = -121
    Output: false
    Explanation: From left to right, it reads -121. From right to left it becomes 121-.

Example 3:
    Input: x = 10
    Output: false
    Explanation: Reads 01 from right to left. Therefore it is not a palindrome.

Constraints:
    -2^31 <= x <= 2^31 - 1

Follow-up: Could you solve it without converting the integer to a string?
"""

import unittest


class Solution:
    """Reverse-half approach — O(log10(n)) time, O(1) space.

    Reverses only the second half of the number and compares with the first half.
    When the number of digits is odd, the middle digit doesn't matter
    (it will always equal itself), so we discard it via reversed_half // 10.

    This avoids overflow issues and doesn't require string conversion.
    """

    def isPalindrome(self, x: int) -> bool:
        # Negatives and numbers ending in 0 (except 0 itself) are not palindromes
        if x < 0 or (x % 10 == 0 and x != 0):
            return False

        reversed_half = 0
        while x > reversed_half:
            reversed_half = reversed_half * 10 + x % 10
            x //= 10

        # Even digits: x == reversed_half (e.g., 1221 -> 12 == 12)
        # Odd digits: x == reversed_half // 10 (e.g., 12321 -> 12 == 123//10)
        return x == reversed_half or x == reversed_half // 10


# --- Tests ---


class TestPalindromeNumber(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example_1(self):
        self.assertTrue(self.sol.isPalindrome(121))

    def test_example_2(self):
        self.assertFalse(self.sol.isPalindrome(-121))

    def test_example_3(self):
        self.assertFalse(self.sol.isPalindrome(10))

    def test_single_digit(self):
        for d in range(10):
            self.assertTrue(self.sol.isPalindrome(d))

    def test_zero(self):
        self.assertTrue(self.sol.isPalindrome(0))

    def test_negative(self):
        self.assertFalse(self.sol.isPalindrome(-1))
        self.assertFalse(self.sol.isPalindrome(-11))
        self.assertFalse(self.sol.isPalindrome(-12321))

    def test_even_digits(self):
        self.assertTrue(self.sol.isPalindrome(1221))
        self.assertTrue(self.sol.isPalindrome(11))
        self.assertTrue(self.sol.isPalindrome(1001))
        self.assertFalse(self.sol.isPalindrome(1234))

    def test_odd_digits(self):
        self.assertTrue(self.sol.isPalindrome(12321))
        self.assertTrue(self.sol.isPalindrome(101))
        self.assertFalse(self.sol.isPalindrome(12345))

    def test_ends_with_zero(self):
        self.assertFalse(self.sol.isPalindrome(120))
        self.assertFalse(self.sol.isPalindrome(100))
        self.assertFalse(self.sol.isPalindrome(1000020))

    def test_large_palindrome(self):
        self.assertTrue(self.sol.isPalindrome(2147447412))

    def test_large_non_palindrome(self):
        self.assertFalse(self.sol.isPalindrome(2147483647))


if __name__ == "__main__":
    unittest.main()
