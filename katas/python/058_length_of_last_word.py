"""
LeetCode #58 - Length of Last Word (Easy)

Given a string s consisting of words and spaces, return the length
of the last word in the string.

A word is a maximal substring consisting of non-space characters only.

Example 1:
    Input: s = "Hello World"
    Output: 5
    Explanation: The last word is "World" with length 5.

Example 2:
    Input: s = "   fly me   to   the moon  "
    Output: 4
    Explanation: The last word is "moon" with length 4.

Example 3:
    Input: s = "luffy is still joyboy"
    Output: 6
    Explanation: The last word is "joyboy" with length 6.

Constraints:
    1 <= s.length <= 10^4
    s consists of only English letters and spaces ' '.
    There will be at least one word in s.
"""

import unittest


class Solution:
    """Reverse scan approach — O(n) time, O(1) extra space.

    Instead of splitting the string (which requires O(n) extra space for
    the resulting list), we scan from the end:

    1. Skip trailing spaces.
    2. Count characters until we hit a space or the start of the string.

    This uses a single pass from right to left with no extra allocations,
    making it the most memory-efficient approach.
    """

    def lengthOfLastWord(self, s: str) -> int:
        # Step 1: skip trailing spaces
        i = len(s) - 1
        while i >= 0 and s[i] == ' ':
            i -= 1

        # Step 2: count characters of the last word
        length = 0
        while i >= 0 and s[i] != ' ':
            length += 1
            i -= 1

        return length


class BuiltInSolution:
    """Pythonic one-liner using str.split() — O(n) time, O(n) space.

    str.split() without arguments splits on any whitespace and strips
    leading/trailing whitespace, so split()[-1] gives the last word
    directly. Less memory-efficient than the reverse scan, but very
    readable and idiomatic Python.
    """

    def lengthOfLastWord(self, s: str) -> int:
        return len(s.split()[-1])


# --- Tests ---


class TestLengthOfLastWord(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()
        self.builtin = BuiltInSolution()

    def test_example_1(self):
        self.assertEqual(self.sol.lengthOfLastWord("Hello World"), 5)

    def test_example_2(self):
        self.assertEqual(self.sol.lengthOfLastWord("   fly me   to   the moon  "), 4)

    def test_example_3(self):
        self.assertEqual(self.sol.lengthOfLastWord("luffy is still joyboy"), 6)

    def test_single_word(self):
        self.assertEqual(self.sol.lengthOfLastWord("hello"), 5)

    def test_single_word_with_trailing_spaces(self):
        self.assertEqual(self.sol.lengthOfLastWord("hello   "), 5)

    def test_single_word_with_leading_spaces(self):
        self.assertEqual(self.sol.lengthOfLastWord("   hello"), 5)

    def test_single_character(self):
        self.assertEqual(self.sol.lengthOfLastWord("a"), 1)

    def test_single_word_surrounded_by_spaces(self):
        self.assertEqual(self.sol.lengthOfLastWord("   x   "), 1)

    def test_long_last_word(self):
        self.assertEqual(self.sol.lengthOfLastWord("a " + "b" * 10000), 10000)

    def test_builtin_matches_optimized(self):
        test_cases = [
            "Hello World",
            "   fly me   to   the moon  ",
            "luffy is still joyboy",
            "hello",
            "hello   ",
            "   hello",
            "a",
            "   x   ",
            "a b c d e",
        ]
        for s in test_cases:
            self.assertEqual(
                self.sol.lengthOfLastWord(s),
                self.builtin.lengthOfLastWord(s),
                f"Mismatch for input: {repr(s)}",
            )


if __name__ == "__main__":
    unittest.main()
