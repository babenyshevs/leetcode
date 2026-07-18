"""
LeetCode #27 - Remove Element (Easy)

Given an integer array nums and an integer val, remove all occurrences
of val in nums in-place. The relative order of the elements may be
changed.

Return the number of elements in nums which are not equal to val.
The first k elements of nums should contain the elements that are
not equal to val. Elements beyond index k-1 can be ignored.

It does not matter what you leave beyond the first k elements.

Example 1:
    Input: nums = [3,2,2,3], val = 3
    Output: 2, nums = [2,2,_,_]
    Explanation: Your function returns k = 2, with the first two
                 elements of nums being 2. The order can change.

Example 2:
    Input: nums = [0,1,2,2,3,0,4,2], val = 2
    Output: 5, nums = [0,1,4,0,3,_,_,_]
    Explanation: Your function returns k = 5, with the first five
                 elements of nums containing 0, 1, 4, 0, and 3.

Constraints:
    0 <= nums.length <= 100
    0 <= nums[i] <= 50
    0 <= val <= 100
"""

import unittest
from typing import List


class Solution:
    """Two-pointer approach — O(n) time, O(1) extra space.

    Use a slow-runner `write` pointer that tracks where the next
    non-val element should go, and a fast-runner `read` pointer
    that scans through the array. Whenever nums[read] != val,
    copy nums[read] to nums[write] and advance write.

    After processing, `write` is the number of elements not equal
    to val, and nums[0..write-1] contains them (order preserved).
    """

    def removeElement(self, nums: List[int], val: int) -> int:
        write = 0  # position for the next non-val element
        for read in range(len(nums)):
            if nums[read] != val:
                nums[write] = nums[read]
                write += 1
        return write


# --- Tests ---


class TestRemoveElement(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def _check(self, nums: List[int], val: int, expected_k: int, expected_first_k: List[int]):
        """Run solution and verify both k and the first k elements."""
        result = list(nums)
        k = self.sol.removeElement(result, val)
        self.assertEqual(k, expected_k)
        self.assertEqual(sorted(result[:k]), sorted(expected_first_k))

    def test_example_1(self):
        self._check([3, 2, 2, 3], 3, 2, [2, 2])

    def test_example_2(self):
        self._check([0, 1, 2, 2, 3, 0, 4, 2], 2, 5, [0, 1, 4, 0, 3])

    def test_empty_input(self):
        self._check([], 1, 0, [])

    def test_no_removals_needed(self):
        self._check([1, 2, 3], 4, 3, [1, 2, 3])

    def test_all_elements_removed(self):
        self._check([4, 4, 4], 4, 0, [])

    def test_single_element_keep(self):
        self._check([1], 2, 1, [1])

    def test_single_element_remove(self):
        self._check([5], 5, 0, [])

    def test_val_at_start_and_end(self):
        self._check([0, 1, 2, 0], 0, 2, [1, 2])

    def test_all_same_value(self):
        self._check([7, 7, 7, 7], 7, 0, [])

    def test_val_not_present(self):
        self._check([1, 2, 3, 4, 5], 6, 5, [1, 2, 3, 4, 5])

    def test_large_input(self):
        nums = [i % 10 for i in range(200)]  # 0..9 repeated 20 times
        k = self.sol.removeElement(list(nums), 5)
        self.assertEqual(k, 180)  # 20 values of 5 removed


if __name__ == "__main__":
    unittest.main()
