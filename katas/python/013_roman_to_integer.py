"""
LeetCode #13 - Roman to Integer (Easy)

Given a roman numeral string s, convert it to an integer.

Roman numerals are represented by seven different symbols:
    I  V  X  L  C   D   M
    1  5  10 50 100 500 1000

Subtractive notation is used in six cases:
    IV = 4, IX = 9, XL = 40, XC = 90, CD = 400, CM = 900

Example 1:
    Input: s = "III"
    Output: 3
    Explanation: III = 3.

Example 2:
    Input: s = "LVIII"
    Output: 58
    Explanation: L = 50, V = 5, III = 3.

Example 3:
    Input: s = "MCMXCIV"
    Output: 1994
    Explanation: M = 1000, CM = 900, XC = 90, IV = 4.

Constraints:
    1 <= s.length <= 15
    s contains only the characters ('I', 'V', 'X', 'L', 'C', 'D', 'M').
    It is guaranteed that s is a valid roman numeral in the range [1, 3999].
"""

import unittest


class Solution:
    """Single-pass left-to-right — O(n) time, O(1) space.

    For each character, compare its value with the next character's value.
    If the current value is less than the next, subtract it (subtractive pair).
    Otherwise, add it. This naturally handles all six subtractive cases
    (IV, IX, XL, XC, CD, CM) without any special-casing.
    """

    # Map of single roman symbols to their integer values
    VALUES = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000,
    }

    def romanToInt(self, s: str) -> int:
        total = 0
        for i, ch in enumerate(s):
            value = self.VALUES[ch]
            # If a smaller value precedes a larger one, subtract it
            if i + 1 < len(s) and value < self.VALUES[s[i + 1]]:
                total -= value
            else:
                total += value
        return total


# --- Tests ---


class TestRomanToInteger(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example_1(self):
        self.assertEqual(self.sol.romanToInt("III"), 3)

    def test_example_2(self):
        self.assertEqual(self.sol.romanToInt("LVIII"), 58)

    def test_example_3(self):
        self.assertEqual(self.sol.romanToInt("MCMXCIV"), 1994)

    def test_single_characters(self):
        self.assertEqual(self.sol.romanToInt("I"), 1)
        self.assertEqual(self.sol.romanToInt("V"), 5)
        self.assertEqual(self.sol.romanToInt("X"), 10)
        self.assertEqual(self.sol.romanToInt("L"), 50)
        self.assertEqual(self.sol.romanToInt("C"), 100)
        self.assertEqual(self.sol.romanToInt("D"), 500)
        self.assertEqual(self.sol.romanToInt("M"), 1000)

    def test_subtractive_pairs(self):
        self.assertEqual(self.sol.romanToInt("IV"), 4)
        self.assertEqual(self.sol.romanToInt("IX"), 9)
        self.assertEqual(self.sol.romanToInt("XL"), 40)
        self.assertEqual(self.sol.romanToInt("XC"), 90)
        self.assertEqual(self.sol.romanToInt("CD"), 400)
        self.assertEqual(self.sol.romanToInt("CM"), 900)

    def test_additive_construction(self):
        self.assertEqual(self.sol.romanToInt("VI"), 6)
        self.assertEqual(self.sol.romanToInt("VII"), 7)
        self.assertEqual(self.sol.romanToInt("VIII"), 8)
        self.assertEqual(self.sol.romanToInt("XII"), 12)
        self.assertEqual(self.sol.romanToInt("XX"), 20)
        self.assertEqual(self.sol.romanToInt("MMXXIII"), 2023)

    def test_mixed(self):
        self.assertEqual(self.sol.romanToInt("XIV"), 14)
        self.assertEqual(self.sol.romanToInt("XIX"), 19)
        self.assertEqual(self.sol.romanToInt("XLIV"), 44)
        self.assertEqual(self.sol.romanToInt("XCIX"), 99)

    def test_minimum(self):
        self.assertEqual(self.sol.romanToInt("I"), 1)

    def test_maximum(self):
        self.assertEqual(self.sol.romanToInt("MMMCMXCIX"), 3999)

    def test_round_numbers(self):
        self.assertEqual(self.sol.romanToInt("C"), 100)
        self.assertEqual(self.sol.romanToInt("D"), 500)
        self.assertEqual(self.sol.romanToInt("M"), 1000)
        self.assertEqual(self.sol.romanToInt("MM"), 2000)
        self.assertEqual(self.sol.romanToInt("MMM"), 3000)


if __name__ == "__main__":
    unittest.main()
