"""
LeetCode #28 - Find the Index of the First Occurrence in a String (Easy)

Given two strings needle and haystack, return the index of the first
occurrence of needle in haystack, or -1 if needle is not part of haystack.

Example 1:
    Input: haystack = "sadbutsad", needle = "sad"
    Output: 0
    Explanation: "sad" occurs at index 0 and 6. The first occurrence
                 is at index 0, so we return 0.

Example 2:
    Input: haystack = "leetcode", needle = "leeto"
    Output: -1
    Explanation: "leeto" did not occur in "leetcode", so we return -1.

Constraints:
    1 <= haystack.length, needle.length <= 10^4
    haystack and needle consist of only lowercase English characters.
"""

import unittest


class Solution:
    """Sliding window approach — O(n * m) worst case, O(1) extra space.

    Compare needle against every possible starting position in haystack.
    For each candidate window haystack[i:i+len(needle)], check if it
    matches needle character by character. Return the first index where
    a full match is found, or -1 if none exists.

    Python's built-in str.find() uses a highly optimized C implementation
    (Boyer-Moore variants), but we implement the logic explicitly here
    for educational purposes.
    """

    def strStr(self, haystack: str, needle: str) -> int:
        n, m = len(haystack), len(needle)

        # Edge case: empty needle — by convention return 0
        if m == 0:
            return 0

        # If needle is longer than haystack, no match is possible
        if m > n:
            return -1

        # Slide a window of length m over haystack
        for i in range(n - m + 1):
            # Quick check: first char must match (cheap filter)
            if haystack[i] != needle[0]:
                continue
            # Full comparison of the window
            if haystack[i : i + m] == needle:
                return i

        return -1


# --- Tests ---


class TestStrStr(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example_1(self):
        self.assertEqual(self.sol.strStr("sadbutsad", "sad"), 0)

    def test_example_2(self):
        self.assertEqual(self.sol.strStr("leetcode", "leeto"), -1)

    def test_needle_equals_haystack(self):
        self.assertEqual(self.sol.strStr("hello", "hello"), 0)

    def test_needle_longer_than_haystack(self):
        self.assertEqual(self.sol.strStr("hi", "hello"), -1)

    def test_needle_at_end(self):
        self.assertEqual(self.sol.strStr("abcde", "de"), 3)

    def test_single_char_needle(self):
        self.assertEqual(self.sol.strStr("abcdef", "d"), 3)

    def test_single_char_not_found(self):
        self.assertEqual(self.sol.strStr("abcdef", "g"), -1)

    def test_repeated_pattern(self):
        self.assertEqual(self.sol.strStr("aaaaa", "aaa"), 0)

    def test_overlapping_occurrence(self):
        # "aa" appears at index 0 and 1; first is 0
        self.assertEqual(self.sol.strStr("aaa", "aa"), 0)

    def test_empty_needle(self):
        self.assertEqual(self.sol.strStr("abc", ""), 0)

    def test_empty_haystack_nonempty_needle(self):
        self.assertEqual(self.sol.strStr("", "a"), -1)

    def test_both_empty(self):
        self.assertEqual(self.sol.strStr("", ""), 0)

    def test_large_haystack(self):
        haystack = "a" * 10000 + "b"
        needle = "b"
        self.assertEqual(self.sol.strStr(haystack, needle), 10000)

    def test_large_needle(self):
        haystack = "a" * 10000 + "b" + "c" * 100
        needle = "b" + "c" * 100
        self.assertEqual(self.sol.strStr(haystack, needle), 10000)


if __name__ == "__main__":
    unittest.main()
