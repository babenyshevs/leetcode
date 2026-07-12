"""
LeetCode #26 - Remove Duplicates from Sorted Array (Easy)

Given an integer array nums sorted in non-decreasing order, remove the
duplicates in-place such that each unique element appears only once.
The relative order of the elements should be kept the same.

Return the number of unique elements k. The first k elements of nums
should contain the unique numbers in sorted order. Elements beyond
index k-1 can be ignored.

Example 1:
    Input: nums = [1,1,2]
    Output: 2, nums = [1,2,_]
    Explanation: Your function returns k = 2, with the first two
                 elements of nums being 1 and 2.

Example 2:
    Input: nums = [0,0,1,1,1,2,2,3,3,4]
    Output: 5, nums = [0,1,2,3,4,_,_,_,_,_]
    Explanation: Your function returns k = 5, with the first five
                 elements of nums being 0, 1, 2, 3, and 4.

Constraints:
    1 <= nums.length <= 3 * 10^4
    -100 <= nums[i] <= 100
    nums is sorted in non-decreasing order.
"""

import unittest
from typing import List


class Solution:
    """Two-pointer approach — O(n) time, O(1) extra space.

    Since the array is sorted, duplicates are always adjacent.
    Use a slow-runner `write` pointer that tracks where the next
    unique element should go, and a fast-runner `read` pointer
    that scans through the array. Whenever nums[read] differs from
    nums[write], advance write and copy the value over.

    After processing, `write + 1` is the number of unique elements,
    and nums[0..write] contains them in sorted order.
    """

    def removeDuplicates(self, nums: List[int]) -> int:
        if not nums:
            return 0

        write = 0  # position for the next unique element
        for read in range(1, len(nums)):
            if nums[read] != nums[write]:
                write += 1
                nums[write] = nums[read]

        return write + 1


# --- Tests ---


class TestRemoveDuplicates(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def _check(self, nums: List[int], expected_k: int, expected_first_k: List[int]):
        """Run solution and verify both k and the first k elements."""
        # Work on a copy so the original is preserved for display
        result = list(nums)
        k = self.sol.removeDuplicates(result)
        self.assertEqual(k, expected_k)
        self.assertEqual(result[:k], expected_first_k)

    def test_example_1(self):
        self._check([1, 1, 2], 2, [1, 2])

    def test_example_2(self):
        self._check([0, 0, 1, 1, 1, 2, 2, 3, 3, 4], 5, [0, 1, 2, 3, 4])

    def test_single_element(self):
        self._check([1], 1, [1])

    def test_all_duplicates(self):
        self._check([2, 2, 2, 2, 2], 1, [2])

    def test_all_unique(self):
        self._check([1, 2, 3, 4, 5], 5, [1, 2, 3, 4, 5])

    def test_negative_numbers(self):
        self._check([-3, -3, -1, 0, 0, 2], 4, [-3, -1, 0, 2])

    def test_two_elements_same(self):
        self._check([7, 7], 1, [7])

    def test_two_elements_different(self):
        self._check([1, 2], 2, [1, 2])

    def test_large_input(self):
        nums = [i // 2 for i in range(200)]  # [0,0,1,1,2,2,...,99,99]
        self._check(nums, 100, list(range(100)))

    def test_empty_input(self):
        self._check([], 0, [])


if __name__ == "__main__":
    unittest.main()
