"""
LeetCode #35 - Search Insert Position (Easy)

Given a sorted array of distinct integers and a target value, return
the index if the target is found. If not, return the index where it
would be if it were inserted in order.

You must write an algorithm with O(log n) runtime complexity.

Example 1:
    Input: nums = [1,3,5,6], target = 5
    Output: 2

Example 2:
    Input: nums = [1,3,5,6], target = 2
    Output: 1

Example 3:
    Input: nums = [1,3,5,6], target = 7
    Output: 4

Constraints:
    1 <= nums.length <= 10^4
    -10^4 <= nums[i] <= 10^4
    nums contains distinct values sorted in ascending order.
    -10^4 <= target <= 10^4
"""

import unittest


class Solution:
    """Binary search approach — O(log n) time, O(1) extra space.

    Classic binary search on the sorted array. We maintain a search
    window [lo, hi] and repeatedly halve it. When the loop terminates,
    lo == hi and points to the correct insertion position:
      - If target was found, lo is its index.
      - If target was not found, lo is where it should be inserted.

    The key insight is that we narrow lo/hi until lo > hi, then lo
    is always the correct answer because it is the first position
    where nums[lo] >= target.
    """

    def searchInsert(self, nums: list[int], target: int) -> int:
        lo, hi = 0, len(nums) - 1

        while lo <= hi:
            mid = lo + (hi - lo) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1

        # lo is the insertion point when target is not found
        return lo


# --- Tests ---


class TestSearchInsert(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example_1(self):
        self.assertEqual(self.sol.searchInsert([1, 3, 5, 6], 5), 2)

    def test_example_2(self):
        self.assertEqual(self.sol.searchInsert([1, 3, 5, 6], 2), 1)

    def test_example_3(self):
        self.assertEqual(self.sol.searchInsert([1, 3, 5, 6], 7), 4)

    def test_insert_at_beginning(self):
        self.assertEqual(self.sol.searchInsert([1, 3, 5, 6], 0), 0)

    def test_insert_at_end(self):
        self.assertEqual(self.sol.searchInsert([1, 3, 5, 6], 7), 4)

    def test_single_element_found(self):
        self.assertEqual(self.sol.searchInsert([1], 1), 0)

    def test_single_element_insert_before(self):
        self.assertEqual(self.sol.searchInsert([1], 0), 0)

    def test_single_element_insert_after(self):
        self.assertEqual(self.sol.searchInsert([1], 2), 1)

    def test_negative_numbers(self):
        self.assertEqual(self.sol.searchInsert([-5, -3, 0, 2, 4], -3), 1)

    def test_negative_insert(self):
        self.assertEqual(self.sol.searchInsert([-5, -3, 0, 2, 4], -4), 1)

    def test_large_array(self):
        nums = list(range(0, 10000, 2))  # [0, 2, 4, ..., 9998]
        self.assertEqual(self.sol.searchInsert(nums, 5000), 2500)
        self.assertEqual(self.sol.searchInsert(nums, 4999), 2500)  # between 4998 and 5000
        self.assertEqual(self.sol.searchInsert(nums, 10000), 5000)  # past the end


if __name__ == "__main__":
    unittest.main()
