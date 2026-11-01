"""
LeetCode #169 - Majority Element (Easy)

Given an array nums of size n, return the majority element.

The majority element is the element that appears more than floor(n / 2)
times. You may assume that the majority element always exists in the
array.

Example 1:
    Input:  nums = [3,2,3]
    Output: 3

Example 2:
    Input:  nums = [2,2,1,1,1,2,2]
    Output: 2

Constraints:
    n == nums.length
    1 <= n <= 5 * 10^4
    -10^9 <= nums[i] <= 10^9
    The input is generated such that a majority element will exist.

Follow-up: Could you solve the problem in linear time and O(1) space?
"""

import unittest
from collections import Counter


class HashMapSolution:
    """Count occurrences with a hash map, then pick the dominant key.

    The most direct approach: one pass to count every distinct value,
    one pass over the counter to return the key with the maximal count.
    Because the problem guarantees a majority element (> n/2 occurrences)
    exists, `max()` over the counts is guaranteed to find exactly it —
    no tie-breaking is possible (two elements cannot both exceed n/2).

    Time complexity:  O(n) — one pass to count, one pass over <= n keys.
    Space complexity: O(n) — the counter, in the worst case n distinct keys.
    """

    def majorityElement(self, nums):
        return Counter(nums).most_common(1)[0][0]


class BoyerMooreSolution:
    """Boyer–Moore majority vote — linear time, O(1) space (the follow-up).

    Intuition: pair off and cancel every element against one of a
    *different* value. If some value occurs more than n/2 times, it
    survives every such pairing because each non-majority element can
    cancel at most one majority element, leaving majority occurrences
    uncancelled. The algorithm maintains:

        candidate — the value whose survival is being tested
        count     — its current "vote margin" (net unpaired occurrences)

    Walk the array once:
        count == 0   -> adopt the current value as the new candidate
        value == candidate -> count += 1  (vote for)
        value != candidate -> count -= 1  (cancel one against it)

    Why the survivor is the majority: when the scan ends, every element
    that was cancelled was paired against another element of a different
    value, so cancelled pairs contain at most one majority element each
    while the candidate retains net count > 0 exactly when it occurs
    more than n/2 times. Formally, if v is the true majority (c_v > n/2
    occurrences), each "cancellation" consumes at most one v, so at most
    n - c_v < c_v of the v's can be cancelled — at least one survives,
    and the final candidate must be v.

    Note: without the guarantee that a majority exists, a second
    verification pass over the array would be required; here the
    problem statement makes the candidate automatically correct.

    Time complexity:  O(n) — a single pass.
    Space complexity: O(1) — two scalar variables.
    """

    def majorityElement(self, nums):
        candidate = None
        count = 0
        for value in nums:
            if count == 0:
                candidate = value
            count += 1 if value == candidate else -1
        return candidate


class SortingSolution:
    """Sort and take the middle element — short, but O(n log n).

    After sorting, equal values are contiguous. A value occupying more
    than n/2 slots must cover the middle index n // 2: any window of
    length > n/2 inside an array of length n unavoidably contains the
    midpoint. So `sorted(nums)[n // 2]` is the majority element.

    Time complexity:  O(n log n) — dominated by the sort.
    Space complexity: O(n) here for the sorted copy (O(1) extra if the
                      input may be sorted in place).
    """

    def majorityElement(self, nums):
        return sorted(nums)[len(nums) // 2]


# --- Tests ---


class TestMajorityElement(unittest.TestCase):
    def setUp(self):
        self.solutions = [
            HashMapSolution(),
            BoyerMooreSolution(),
            SortingSolution(),
        ]

    def test_example_1(self):
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.majorityElement([3, 2, 3]), 3)

    def test_example_2(self):
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.majorityElement([2, 2, 1, 1, 1, 2, 2]), 2)

    def test_single_element(self):
        # n == 1: the only element trivially appears more than 0 times.
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.majorityElement([1]), 1)

    def test_all_same_values(self):
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.majorityElement([-7] * 10), -7)

    def test_majority_at_minimum_margin(self):
        # [x, y, x, y, x]: x appears 3 == floor(5/2) + 1 times — the
        # smallest legal majority for n = 5. Same shape for even n = 6.
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.majorityElement([5, 9, 5, 9, 5]), 5)
                self.assertEqual(sol.majorityElement([5, 9, 5, 9, 5, 5]), 5)

    def test_negative_values(self):
        # Values span +/-10^9; negative majorities must not be mangled.
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(
                    sol.majorityElement([-10**9, 10**9, -10**9]), -10**9
                )

    def test_majority_in_second_half(self):
        # The majority block sits at the END — stresses Boyer-Moore's
        # mid-scan candidate switches (it must recover, not stick to an
        # early candidate) and proves the midpoint trick is about
        # coverage, not position.
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.majorityElement([1, 2, 3, 4, 4, 4, 4]), 4)

    def test_boundary_max_size(self):
        # n = 5 * 10^4 at the constraint ceiling, majority by one over
        # exactly n/2 (even n): 25001 occurrences of 42, 24999 of -1.
        nums = [42] * 25_001 + [-1] * 24_999
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.majorityElement(nums), 42)

    def test_against_counter_oracle_randomized(self):
        # Oracle: Counter-derived majority on 300 random arrays that are
        # *constructed* to contain a majority (counts range from n/2 + 1
        # to n), with random shuffling so majority position varies.
        import random

        rng = random.Random(169)
        for _ in range(300):
            n = rng.randint(1, 200)
            majority_value = rng.randint(-10**9, 10**9)
            filler = [
                rng.randint(-10**9, 10**9)
                for _ in range(rng.randint(0, n - 1))
            ]
            majority_count = max(n // 2 + 1, n - len(filler))
            nums = [majority_value] * majority_count + filler
            nums = nums[:n]
            rng.shuffle(nums)
            expected = Counter(nums).most_common(1)[0][0]
            # Guard the oracle itself: the built array must really have
            # a strict majority (sanity check on test construction).
            self.assertGreater(Counter(nums)[expected], n // 2)
            for sol in self.solutions:
                with self.subTest(sol=type(sol).__name__):
                    self.assertEqual(sol.majorityElement(nums), expected)


if __name__ == "__main__":
    unittest.main()
