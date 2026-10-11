"""
LeetCode #136 - Single Number (Easy)

Given a non-empty array of integers nums, every element appears twice
except for one. Find that single one.

You must implement a solution with a linear runtime complexity and use
only constant extra space.

Example 1:
    Input: nums = [2,2,1]
    Output: 1

Example 2:
    Input: nums = [4,1,2,1,2]
    Output: 4

Example 3:
    Input: nums = [1]
    Output: 1

Constraints:
    1 <= nums.length <= 3 * 10^4
    -3 * 10^4 <= nums[i] <= 3 * 10^4
    Each element in the array appears twice except for one element
    which appears only once.
"""

import unittest
from collections import Counter
from functools import reduce
from operator import xor


class XorSolution:
    """Fold XOR over the array — O(n) time, O(1) space. The canonical one.

    XOR is the perfect tool here because of three properties:

      - x ^ x = 0      (a value cancels itself)
      - x ^ 0 = x      (0 is the identity)
      - XOR is commutative and associative (order doesn't matter)

    So if every value but one appears exactly twice, folding XOR over
    the whole array pairs each duplicate up somewhere in the fold and
    annihilates it to 0 — regardless of position. What survives is
    0 ^ single = single. No hashing, no sorting, no extra memory:
    one running integer is all it takes, which satisfies both the
    linear-time and constant-space requirements.

    Python ints are arbitrary precision, so the bounded constraint
    (-3 * 10^4 <= nums[i] <= 3 * 10^4) never causes overflow concerns.

    Time complexity:  O(n) — one fold, one operation per element.
    Space complexity: O(1) — a single accumulator integer.
    """

    def singleNumber(self, nums):
        return reduce(xor, nums, 0)


class LoopXorSolution:
    """Explicit-loop variant of the XOR fold — O(n) time, O(1) space.

    Identical math to XorSolution, spelled out with a running
    accumulator so the pairwise cancellation is visible step by step:

        acc = 0
        for x in nums: acc ^= x   # pairs cancel; single survives

    Kept alongside `reduce` for readability and as a cross-check.

    Time complexity:  O(n).
    Space complexity: O(1).
    """

    def singleNumber(self, nums):
        acc = 0
        for x in nums:
            acc ^= x
        return acc


class MathSolution:
    """Arithmetic identity 2 * sum(set) - sum = single — O(n) time, O(n) space.

    If every element appeared exactly twice, then twice the sum of the
    distinct values would equal the sum of the whole array. The lone
    singleton breaks that symmetry by exactly its own value:

        2 * (a + b + c) - (a + a + b + b + c) = c

    Elegant, but building the set costs O(n) extra space, so it does
    not meet the follow-up's constant-space requirement — still a very
    common and readable interview alternative.

    Time complexity:  O(n) — one pass to build the set, two sums.
    Space complexity: O(n) — the set of distinct values.
    """

    def singleNumber(self, nums):
        return 2 * sum(set(nums)) - sum(nums)


class CounterSolution:
    """Count occurrences, return the key with count 1 — oracle.

    Uses collections.Counter to tally every element and picks out the
    one whose count is exactly 1. It is logically independent of the
    XOR tricks above, which makes it a good oracle for the randomized
    cross-check test. O(n) time but O(n) extra space.

    Time complexity:  O(n).
    Space complexity: O(n) — the counter.
    """

    def singleNumber(self, nums):
        counts = Counter(nums)
        for value, count in counts.items():
            if count == 1:
                return value
        raise ValueError("no singleton present")


# --- Tests ---


class TestSingleNumber(unittest.TestCase):
    def setUp(self):
        self.solutions = [
            XorSolution(),
            LoopXorSolution(),
            MathSolution(),
        ]

    def test_example_1(self):
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.singleNumber([2, 2, 1]), 1)

    def test_example_2(self):
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.singleNumber([4, 1, 2, 1, 2]), 4)

    def test_example_3_single_element(self):
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.singleNumber([1]), 1)

    def test_singleton_in_middle(self):
        # The pairs cancel no matter where the singleton sits.
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.singleNumber([7, 3, 9, 3, 7]), 9)

    def test_negative_numbers(self):
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.singleNumber([-4, -1, -4]), -1)

    def test_mixed_signs(self):
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.singleNumber([-30000, 30000, 0, 30000, -30000]), 0)

    def test_zero_as_singleton(self):
        # Zero is a perfectly valid singleton; XOR fold still finds it.
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.singleNumber([5, 0, 5]), 0)

    def test_boundary_values(self):
        # Constraints: -3*10^4 <= nums[i] <= 3*10^4.
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.singleNumber([30000, -30000, 30000]), -30000)

    def test_large_input(self):
        # 3 * 10^4 elements: 14999 distinct pairs plus one singleton.
        nums = list(range(15000))
        nums = nums + nums + [15000]
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.singleNumber(nums), 15000)

    def test_against_oracle_on_random_inputs(self):
        # Oracle test: all solutions must agree with a Counter-based
        # tally on many random arrays honoring the constraints.
        import random

        rng = random.Random(136)  # fixed seed -> deterministic tests
        oracle = CounterSolution()
        for _ in range(200):
            pair_count = rng.randint(0, 30)
            single = rng.randint(-30000, 30000)
            # The premise: every non-singleton value appears EXACTLY
            # twice. Sample pair values without replacement and exclude
            # the singleton itself so no value ends up appearing 3 or 4
            # times (which would violate the constraints).
            pool = [v for v in range(-50, 51) if v != single]
            pair_values = rng.sample(pool, pair_count)
            nums = []
            for v in pair_values:
                nums.extend([v, v])
            nums.append(single)
            rng.shuffle(nums)
            expected = oracle.singleNumber(nums)
            for sol in self.solutions:
                with self.subTest(sol=type(sol).__name__, single=single):
                    self.assertEqual(sol.singleNumber(nums), expected)


if __name__ == "__main__":
    unittest.main()
