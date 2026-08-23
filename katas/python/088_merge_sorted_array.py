"""
LeetCode #88 - Merge Sorted Array (Easy)

You are given two integer arrays nums1 and nums2, sorted in non-decreasing
order, and two integers m and n, representing the number of elements in
nums1 and nums2 respectively.

Merge nums1 and nums2 into a single array sorted in non-decreasing order.

The final sorted array should not be returned by the function, but instead
be stored inside the array nums1. To accommodate this, nums1 has a length
of m + n, where the first m elements denote the elements that should be
merged, and the last n elements are set to 0 and should be ignored.

Example 1:
    Input: nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3
    Output: [1,2,2,3,5,6]

Example 2:
    Input: nums1 = [1], m = 1, nums2 = [], n = 0
    Output: [1]

Example 3:
    Input: nums1 = [0], m = 0, nums2 = [1], n = 1
    Output: [1]

Constraints:
    nums1.length == m + n
    nums2.length == n
    0 <= m, n <= 200
    1 <= m + n <= 200
    -10^9 <= nums1[i], nums2[j] <= 10^9
"""

import unittest


class Solution:
    """Two-pointer merge from the end — O(m + n) time, O(1) space.

    Key insight: fill nums1 from the back to avoid overwriting elements
    we still need to compare. Use three pointers:
      - `i`: last valid element in nums1 (m - 1)
      - `j`: last element in nums2 (n - 1)
      - `k`: last position in nums1's full buffer (m + n - 1)

    At each step, place the larger of nums1[i] and nums2[j] at nums1[k],
    then decrement the corresponding pointer(s).

    After the loop, if nums2 still has remaining elements, copy them over
    (if nums1 has leftovers they're already in place).
    """

    def merge(self, nums1, m, nums2, n):
        i = m - 1       # pointer for nums1's valid elements
        j = n - 1       # pointer for nums2
        k = m + n - 1   # pointer for placement position in nums1

        # Merge from the end, placing largest elements first
        while i >= 0 and j >= 0:
            if nums1[i] > nums2[j]:
                nums1[k] = nums1[i]
                i -= 1
            else:
                nums1[k] = nums2[j]
                j -= 1
            k -= 1

        # If nums2 has remaining elements, copy them over
        # (nums1 leftovers are already in correct position)
        while j >= 0:
            nums1[k] = nums2[j]
            j -= 1
            k -= 1


class SimpleSolution:
    """Naive approach — O((m+n) log(m+n)) time, O(m) extra space.

    Copy nums2 into nums1's trailing space, then sort the whole array.
    Simple but doesn't meet the O(m+n) follow-up challenge.
    """

    def merge(self, nums1, m, nums2, n):
        for i in range(n):
            nums1[m + i] = nums2[i]
        nums1.sort()


# --- Tests ---


class TestMergeSortedArray(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()
        self.simple = SimpleSolution()

    def _merge(self, sol, nums1, m, nums2, n):
        """Helper that works on a copy so we can assert the result."""
        nums1 = list(nums1)  # copy
        sol.merge(nums1, m, nums2, n)
        return nums1

    def test_example_1(self):
        result = self._merge(self.sol, [1, 2, 3, 0, 0, 0], 3, [2, 5, 6], 3)
        self.assertEqual(result, [1, 2, 2, 3, 5, 6])

    def test_example_2(self):
        result = self._merge(self.sol, [1], 1, [], 0)
        self.assertEqual(result, [1])

    def test_example_3(self):
        result = self._merge(self.sol, [0], 0, [1], 1)
        self.assertEqual(result, [1])

    def test_all_nums1(self):
        """nums2 is empty, nums1 already sorted."""
        result = self._merge(self.sol, [1, 2, 3], 3, [], 0)
        self.assertEqual(result, [1, 2, 3])

    def test_all_nums2(self):
        """nums1 is empty, everything from nums2."""
        result = self._merge(self.sol, [0, 0], 0, [1, 2], 2)
        self.assertEqual(result, [1, 2])

    def test_negative_numbers(self):
        result = self._merge(self.sol, [-3, -1, 0, 0, 0], 2, [-2, 1, 4], 3)
        self.assertEqual(result, [-3, -2, -1, 1, 4])

    def test_duplicates(self):
        result = self._merge(self.sol, [1, 2, 3, 0, 0], 3, [1, 2], 2)
        self.assertEqual(result, [1, 1, 2, 2, 3])

    def test_simple_matches_optimal(self):
        """Verify both solutions produce the same result."""
        cases = [
            ([1, 2, 3, 0, 0, 0], 3, [2, 5, 6], 3),
            ([1], 1, [], 0),
            ([0], 0, [1], 1),
            ([0, 0], 0, [1, 2], 2),
            ([1, 2, 3], 3, [], 0),
            ([-3, -1, 0, 0, 0], 2, [-2, 1, 4], 3),
            ([1, 2, 3, 0, 0], 3, [1, 2], 2),
        ]
        for nums1, m, nums2, n in cases:
            r1 = self._merge(self.sol, nums1, m, nums2, n)
            r2 = self._merge(self.simple, nums1, m, nums2, n)
            self.assertEqual(r1, r2, f"Mismatch for input {nums1}, {m}, {nums2}, {n}")


if __name__ == "__main__":
    unittest.main()
