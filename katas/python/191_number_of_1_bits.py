"""
LeetCode #191 - Number of 1 Bits (Easy)

Given a positive integer n, write a function that returns the number of
set bits in its binary representation (also known as the Hamming weight).

Example 1:
    Input:  n = 11  (binary 1011)
    Output: 3  -- the binary string 1011 has three set bits.

Example 2:
    Input:  n = 128 (binary 10000000)
    Output: 1  -- one set bit.

Example 3:
    Input:  n = 2147483645 (binary 1111111111111111111111111111101)
    Output: 30 -- thirty set bits.

Constraints:
    1 <= n <= 2**31 - 1

Follow up: If this function is called many times, how would you optimize
it? ByteTableSolution answers this: precompute the popcount of every
byte (256 entries), then count any 32-bit word with 4 table lookups.

Key insight: counting set bits can be done either bit by bit (peel or
clear), in O(popcount) via Brian Kernighan's trick (x & (x-1) drops the
lowest set bit), or in O(word/8) with a memoized byte table. Python also
ships the answer directly as int.bit_count(); bin(n).count("1") is its
portable equivalent and serves as the test oracle below.
"""

import unittest
from functools import lru_cache


class ShiftSolution:
    """Bit peeling — the canonical loop over all 32 positions.

    Invariant: after k iterations, `count` equals the number of set bits
    among the lowest k bits of the original n. Each step adds n's lowest
    bit (n & 1) to the tally, then shifts n right to expose the next
    bit. The loop runs until n is 0, so it costs O(number of bits) —
    for a fixed 32-bit word, O(1), up to 32 iterations.

    Time complexity:  O(1) — at most 32 iterations for the given bounds.
    Space complexity: O(1).
    """

    def hammingWeight(self, n):
        count = 0
        while n:
            count += n & 1
            n >>= 1
        return count


class BrianKernighanSolution:
    """Brian Kernighan's trick — one loop iteration per set bit.

    The identity n & (n - 1) clears the lowest set bit of n: subtracting
    1 flips that bit to 0 and every bit below it to 1, so ANDing leaves
    everything above the lowest set bit untouched and zeroes it plus the
    tail. Each iteration therefore removes exactly one set bit, and the
    loop runs popcount(n) times — independent of word size. For sparse
    words (e.g. n = 1) this is dramatically faster than the full loop;
    for dense words (n = 2**31 - 1) it degrades to the same 32 steps.

    Time complexity:  O(1) — at most popcount(n) <= 32 iterations.
    Space complexity: O(1).
    """

    def hammingWeight(self, n):
        count = 0
        while n:
            n &= n - 1  # drop the lowest set bit
            count += 1
        return count


class PythonicSolution:
    """One-liner via the binary string — Pythonic reference / oracle.

    bin(n) yields a string like '0b1011'; count("1") tallies the set
    bits. (Since Python 3.10 the same answer is int.bit_count(), which
    avoids the string entirely.) Slowest of the bit-level approaches in
    practice (string allocation) but the easiest to read and verify,
    which makes it the natural oracle in the tests below.

    Time complexity:  O(1) with a 32-character string constant factor.
    Space complexity: O(1) — one short string.
    """

    def hammingWeight(self, n):
        return bin(n).count("1")


@lru_cache(maxsize=256)
def _popcount_byte(b):
    """Popcount of one byte — memoized for the follow-up.

    lru_cache turns this into a 256-entry lookup table that fills
    lazily on first use. After at most 256 distinct calls every entry
    is O(1) — exactly the optimization the follow-up asks for when
    hammingWeight is called many times.
    """
    count = 0
    while b:
        b &= b - 1
        count += 1
    return count


class ByteTableSolution:
    """Follow-up answer: 4 memoized byte lookups per call.

    Split the 32-bit word into its 4 bytes, add their popcounts through
    the shared lru_cache table. With table lookups costed at O(1), each
    call does 4 lookups + 3 shifts/ANDs instead of scanning 32 bits.
    The cache is shared across all calls, so repeated calls on similar
    data pay nothing after warm-up. (A truly "hard" variant would
    precompute all 256 entries up front in __init__; lru_cache gives
    the same steady state with lazy initialization.)

    Time complexity:  O(1) — 4 lookups once the 256-entry table is warm.
    Space complexity: O(1) — at most 256 cache entries.
    """

    def hammingWeight(self, n):
        return (
            _popcount_byte((n >> 24) & 0xFF)
            + _popcount_byte((n >> 16) & 0xFF)
            + _popcount_byte((n >> 8) & 0xFF)
            + _popcount_byte(n & 0xFF)
        )


# --- Tests ---


class TestHammingWeight(unittest.TestCase):
    def setUp(self):
        self.solutions = [
            ShiftSolution(),
            BrianKernighanSolution(),
            PythonicSolution(),
            ByteTableSolution(),
        ]
        self.oracle = PythonicSolution()

    def test_example_1(self):
        # 1011 -> three set bits
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.hammingWeight(11), 3)

    def test_example_2(self):
        # 10000000 -> one set bit
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.hammingWeight(128), 1)

    def test_example_3(self):
        # 1111111111111111111111111111101 -> thirty set bits
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.hammingWeight(2147483645), 30)

    def test_minimum_input(self):
        # Smallest legal input: a single set bit.
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.hammingWeight(1), 1)

    def test_maximum_input(self):
        # Largest legal input: 2**31 - 1, all 31 low bits set.
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.hammingWeight(2**31 - 1), 31)

    def test_power_of_two_sweep(self):
        # 2**k has exactly one set bit, for every legal exponent.
        for k in range(31):
            for sol in self.solutions:
                with self.subTest(sol=type(sol).__name__, k=k):
                    self.assertEqual(sol.hammingWeight(2**k), 1)

    def test_alternating_patterns(self):
        # Hand-derived constants: alternating masks have 16 set bits,
        # the all-ones word 2**32 - 1 has 32.
        cases = {
            0xAAAAAAAA: 16,
            0x55555555: 16,
            0xFFFF0000: 16,
            0x0000FFFF: 16,
            0xFFFFFFFF: 32,
        }
        for n, expected in cases.items():
            for sol in self.solutions:
                with self.subTest(sol=type(sol).__name__, n=hex(n)):
                    self.assertEqual(sol.hammingWeight(n), expected)

    def test_low_byte_sweep(self):
        # Dense check of all 256 single-byte input patterns against the
        # string-count oracle.
        for b in range(256):
            expected = self.oracle.hammingWeight(b)
            for sol in self.solutions:
                with self.subTest(sol=type(sol).__name__, b=b):
                    self.assertEqual(sol.hammingWeight(b), expected)

    def test_agree_with_oracle_randomized(self):
        # Random inputs drawn from the official constraint space
        # (1 <= n <= 2**31 - 1): every solution must match the oracle.
        import random

        rng = random.Random(191)
        for _ in range(500):
            n = rng.randint(1, 2**31 - 1)
            expected = self.oracle.hammingWeight(n)
            for sol in self.solutions:
                with self.subTest(sol=type(sol).__name__, n=n):
                    self.assertEqual(sol.hammingWeight(n), expected)


if __name__ == "__main__":
    unittest.main()
