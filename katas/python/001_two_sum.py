"""
LeetCode #1 - Two Sum (Easy)

Given an array of integers nums and an integer target,
return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution,
and you may not use the same element twice.

You can return the answer in any order.

Example 1:
    Input: nums = [2,7,11,15], target = 9
    Output: [0,1]
    Explanation: nums[0] + nums[1] == 9

Example 2:
    Input: nums = [3,2,4], target = 6
    Output: [1,2]

Constraints:
    2 <= nums.length <= 10^4
    -10^9 <= nums[i] <= 10^9
    -10^9 <= target <= 10^9
"""

from typing import List


class Solution:
    """Hash map approach — O(n) time, O(n) space."""

    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen: dict[int, int] = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in seen:
                return [seen[complement], i]
            seen[num] = i
        raise ValueError("No solution exists")


class BruteForce:
    """Brute-force approach — O(n^2) time, O(1) space.
    Useful as a reference to compare against the optimized version."""

    def twoSum(self, nums: List[int], target: int) -> List[int]:
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[i] + nums[j] == target:
                    return [i, j]
        raise ValueError("No solution exists")


# --- Tests ---

import unittest


class TestTwoSum(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example_1(self):
        result = self.sol.twoSum([2, 7, 11, 15], 9)
        self.assertEqual(sorted(result), [0, 1])

    def test_example_2(self):
        result = self.sol.twoSum([3, 2, 4], 6)
        self.assertEqual(sorted(result), [1, 2])

    def test_negative_numbers(self):
        result = self.sol.twoSum([-1, -2, -3, -4, -5], -8)
        self.assertEqual(sorted(result), [2, 4])

    def test_single_solution(self):
        result = self.sol.twoSum([0, 4, 3, 0], 0)
        self.assertEqual(sorted(result), [0, 3])

    def test_large_numbers(self):
        # 10^9 + 2 = (10^9) + 2 -> indices 0 and 1
        result = self.sol.twoSum([10**9, 2, 10**9 - 2], 10**9 + 2)
        self.assertEqual(sorted(result), [0, 1])

    def test_brute_force_matches(self):
        brute = BruteForce()
        nums = [2, 7, 11, 15]
        self.assertEqual(self.sol.twoSum(nums, 9), brute.twoSum(nums, 9))


if __name__ == "__main__":
    unittest.main()
