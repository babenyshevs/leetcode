"""
LeetCode #67 - Add Binary (Easy)

Given two binary strings a and b, return their sum as a binary string.

Example 1:
    Input: a = "11", b = "1"
    Output: "100"
    Explanation: 11 (3) + 1 (1) = 100 (4).

Example 2:
    Input: a = "1010", b = "1011"
    Output: "10101"
    Explanation: 1010 (10) + 1011 (11) = 10101 (21).

Constraints:
    1 <= a.length, b.length <= 10^4
    a and b consist only of '0' and '1' characters.
    Each string does not contain leading zeros except for the zero itself.
"""

import unittest


class Solution:
    """Elementary addition with carry — O(max(n, m)) time, O(max(n, m)) space.

    We simulate binary addition the way you'd do it by hand: start from the
    least significant bit (rightmost character) of both strings, add the
    corresponding bits plus any carry, record the result bit, and propagate
    the new carry.  Continue until both strings are exhausted and no carry
    remains.  Finally, reverse the collected bits to obtain the answer.

    This avoids converting the inputs to integers, which would overflow for
    strings up to 10^4 bits long in most languages.
    """

    def addBinary(self, a: str, b: str) -> str:
        i, j = len(a) - 1, len(b) - 1
        carry = 0
        result = []

        while i >= 0 or j >= 0 or carry:
            bit_a = int(a[i]) if i >= 0 else 0
            bit_b = int(b[j]) if j >= 0 else 0
            total = bit_a + bit_b + carry
            result.append(str(total % 2))
            carry = total // 2
            i -= 1
            j -= 1

        # Bits were collected LSB-first; reverse to get the correct order
        return "".join(reversed(result))


class BuiltInSolution:
    """Python built-in conversion approach — O(n + m) time, O(n + m) space.

    Convert both binary strings to integers, add them, then format the
    result back as a binary string.  Python's arbitrary-precision integers
    make this trivially correct even for very long inputs.  Less portable
    to languages without big-int support.
    """

    def addBinary(self, a: str, b: str) -> str:
        return bin(int(a, 2) + int(b, 2))[2:]


# --- Tests ---


class TestAddBinary(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()
        self.builtin = BuiltInSolution()

    def test_example_1(self):
        self.assertEqual(self.sol.addBinary("11", "1"), "100")

    def test_example_2(self):
        self.assertEqual(self.sol.addBinary("1010", "1011"), "10101")

    def test_both_zero(self):
        self.assertEqual(self.sol.addBinary("0", "0"), "0")

    def test_one_zero(self):
        self.assertEqual(self.sol.addBinary("0", "101"), "101")
        self.assertEqual(self.sol.addBinary("101", "0"), "101")

    def test_different_lengths(self):
        self.assertEqual(self.sol.addBinary("1", "111"), "1000")

    def test_carry_propagation(self):
        self.assertEqual(self.sol.addBinary("1111", "1"), "10000")

    def test_no_carry(self):
        self.assertEqual(self.sol.addBinary("101", "010"), "111")

    def test_builtin_matches_optimized(self):
        test_cases = [
            ("11", "1"),
            ("1010", "1011"),
            ("0", "0"),
            ("0", "101"),
            ("101", "0"),
            ("1", "111"),
            ("1111", "1"),
            ("101", "010"),
            ("1", "0"),
            ("10", "10"),
        ]
        for a, b in test_cases:
            self.assertEqual(
                self.sol.addBinary(a, b),
                self.builtin.addBinary(a, b),
                f"Mismatch for input: a={a}, b={b}",
            )

    def test_large_input(self):
        # 2^500 + 1 = 1 followed by 500 zeros, plus 1
        a = "1" + "0" * 500
        b = "1"
        result = self.sol.addBinary(a, b)
        self.assertEqual(result, "1" + "0" * 499 + "1")

    def test_all_ones(self):
        # 2^n - 1 + 2^n - 1 = 2^(n+1) - 2
        n = 20
        a = "1" * n
        b = "1" * n
        result = self.sol.addBinary(a, b)
        expected = "1" + "1" * (n - 1) + "0"
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
