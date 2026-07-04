"""
LeetCode #14 - Longest Common Prefix (Easy)

Write a function to find the longest common prefix string amongst
an array of strings.

If there is no common prefix, return an empty string "".

Example 1:
    Input: strs = ["flower","flow","flight"]
    Output: "fl"
    Explanation: "fl" is the longest common prefix among all strings.

Example 2:
    Input: strs = ["dog","racecar","car"]
    Output: ""
    Explanation: There is no common prefix among the input strings.

Example 3:
    Input: strs = ["a"]
    Output: "a"

Constraints:
    1 <= strs.length <= 200
    0 <= strs[i].length <= 200
    strs[i] consists of only lowercase English letters.
"""

import unittest
from typing import List


class Solution:
    """Horizontal scanning — O(S) time where S is the sum of all characters,
    O(1) extra space (ignoring output).

    Compare the prefix character-by-character across all strings.
    Start with the first string as the candidate prefix and shorten it
    each time a mismatch is found with another string.
    """

    def longestCommonPrefix(self, strs: List[str]) -> str:
        if not strs:
            return ""

        prefix = strs[0]
        for s in strs[1:]:
            # Shorten prefix until it matches the start of s
            while not s.startswith(prefix):
                prefix = prefix[:-1]
                if not prefix:
                    return ""
        return prefix


class SolutionCharByChar:
    """Character-by-character vertical scanning — O(S) time, O(1) space.

    Compare characters column by column across all strings.
    Stops as soon as any string ends or a mismatch is found.
    More intuitive and avoids repeated string slicing.
    """

    def longestCommonPrefix(self, strs: List[str]) -> str:
        if not strs:
            return ""

        for i, ch in enumerate(strs[0]):
            for s in strs[1:]:
                if i >= len(s) or s[i] != ch:
                    return strs[0][:i]
        return strs[0]


# --- Tests ---


class TestLongestCommonPrefix(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()
        self.sol2 = SolutionCharByChar()

    def _check_both(self, strs: List[str], expected: str):
        self.assertEqual(self.sol.longestCommonPrefix(strs), expected)
        self.assertEqual(self.sol2.longestCommonPrefix(strs), expected)

    def test_example_1(self):
        self._check_both(["flower", "flow", "flight"], "fl")

    def test_example_2(self):
        self._check_both(["dog", "racecar", "car"], "")

    def test_example_3(self):
        self._check_both(["a"], "a")

    def test_all_identical(self):
        self._check_both(["abc", "abc", "abc"], "abc")

    def test_empty_string_in_list(self):
        self._check_both(["abc", "", "def"], "")

    def test_prefix_is_entire_shortest_string(self):
        self._check_both(["ab", "abc", "abcd"], "ab")

    def test_no_common_prefix(self):
        self._check_both(["abc", "def", "ghi"], "")

    def test_single_character_common(self):
        self._check_both(["a", "ab", "ac"], "a")

    def test_long_strings(self):
        long_prefix = "a" * 200
        self._check_both([long_prefix, long_prefix + "b", long_prefix + "c"], long_prefix)

    def test_large_input_size(self):
        strs = ["prefix" + str(i) for i in range(200)]
        self._check_both(strs, "prefix")

    def test_empty_strings(self):
        self._check_both(["", "", ""], "")


if __name__ == "__main__":
    unittest.main()
