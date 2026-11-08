"""
LeetCode #190 - Reverse Bits (Easy)

Reverse bits of a given 32-bit unsigned integer.

Example 1:
    Input:  n = 43261596  (00000010100101000001111010011100)
    Output: 964176192     (00111001011110000010100101000000)

Example 2:
    Input:  n = 2147483644 (01111111111111111111111111111100)
    Output: 1073741822     (00111111111111111111111111111110)

Constraints:
    0 <= n <= 2**31 - 2
    n is even.

(The current statement restricts inputs to even integers <= 2^31 - 2 so
that the reversed value also fits in a signed 32-bit int. Historically
the full unsigned range 0 <= n < 2**32 was allowed; the solutions below
handle that whole range and are tested against both.)

Follow up: If this function is called many times, how would you optimize
it? ByteCacheSolution answers this: memoize the reversal of a single
byte, then reverse any 32-bit word with 4 cache lookups.

Key insight: a bit reversal is a permutation of 32 fixed positions, so
it can be produced either iteratively (peel one bit per step) or by a
"divide and conquer" exchange schedule that swaps hierarchically larger
blocks: halves, bytes, nibbles, pairs, then adjacent bits. Each round
of swaps doubles the size of the blocks already in correct relative
order — log2(32) = 5 rounds total, versus 32 iterations for the loop.
"""

import unittest
from functools import lru_cache


class LoopSolution:
    """Iterative bit-peeling — the canonical O(32) loop.

    Invariant: after k iterations, `result` holds the first k bits of n
    in reverse order, placed at the top of the word. Each step shifts
    `result` left (making room at bit 0), appends n's lowest bit via OR,
    then shifts n right to expose the next bit. After 32 steps the bit
    at original position i sits at position 31 - i for every i.

    In fixed-width languages this is the textbook answer. In Python the
    ints are arbitrary precision, but since n < 2**32 and the loop runs
    exactly 32 times, `result` never exceeds 32 bits — no masking
    needed (32 iterations of appending one bit = 32-bit result).

    Time complexity:  O(1) — exactly 32 iterations.
    Space complexity: O(1).
    """

    def reverseBits(self, n):
        result = 0
        for _ in range(32):
            result = (result << 1) | (n & 1)
            n >>= 1
        return result


class DivideConquerSolution:
    """Hierarchical mask-and-swap — 5 rounds of parallel block exchanges.

    Reverse by swapping blocks that are already internally ordered:
      round 1: swap 16-bit halves                     (2 x 16)
      round 2: swap the two bytes within each half    (4 x 8)
      round 3: swap nibbles within each byte          (8 x 4)
      round 4: swap bit pairs within each nibble      (16 x 2)
      round 5: swap adjacent bits                     (32 x 1)
    After round k, blocks of size 2**k are in correct relative position;
    after round 5 the blocks are single bits — fully reversed.

    Each round keeps the two halves separate with a mask (e.g.
    0xFF00FF00 selects the bytes that must move right) and shifts them
    towards each other. Masks in hex spell the pattern they select:
    0xAAAAAAAA = 1010...10 (high bit of each pair), 0x55555555 = its
    complement, 0xF0F0F0F0 / 0x0F0F0F0F for nibbles, and so on.

    O(log 32) rounds — this is what the "Divide and Conquer" tag means
    here, and the same schedule is how hardware reversing circuits are
    wired.

    Time complexity:  O(1) — 5 constant rounds.
    Space complexity: O(1).
    """

    def reverseBits(self, n):
        n = ((n & 0xFFFF0000) >> 16) | ((n & 0x0000FFFF) << 16)
        n = ((n & 0xFF00FF00) >> 8) | ((n & 0x00FF00FF) << 8)
        n = ((n & 0xF0F0F0F0) >> 4) | ((n & 0x0F0F0F0F) << 4)
        n = ((n & 0xCCCCCCCC) >> 2) | ((n & 0x33333333) << 2)
        n = ((n & 0xAAAAAAAA) >> 1) | ((n & 0x55555555) << 1)
        return n


class StringSliceSolution:
    """One-liner via the 32-bit binary string — Pythonic reference.

    Format n as a zero-padded 32-character binary string, reverse it
    with a slice step of -1, and parse back with int(..., 2). Slowest
    of the three (string allocation + parsing) but the easiest to read
    and verify, which makes it the natural oracle in the tests below.

    Time complexity:  O(1) with a 32-character string constant factor.
    Space complexity: O(1) — one 32-char string.
    """

    def reverseBits(self, n):
        return int(f"{n:032b}"[::-1], 2)


@lru_cache(maxsize=256)
def _reverse_byte(b):
    """Reverse the 8 bits of one byte — memoized for the follow-up.

    lru_cache turns this into a 256-entry lookup table that fills
    lazily on first use. After at most 256 distinct calls every entry
    is O(1) — exactly the optimization the follow-up asks for when
    reverseBits is called many times.
    """
    r = 0
    for _ in range(8):
        r = (r << 1) | (b & 1)
        b >>= 1
    return r


class ByteCacheSolution:
    """Follow-up answer: 4 memoized byte reversals per call.

    Split the word into its 4 bytes (most significant first), reverse
    each through the shared lru_cache table, and reassemble in opposite
    byte order. Byte at index i (from the top) must end up at byte
    index 3 - i, i.e. shifted left by (3 - i) * 8.

    Steady-state cost per call: 4 dict/cache lookups + 3 shifts and
    ORs — much cheaper than LoopSolution's 32 iterations, and the
    cache is shared across all calls of this class, so repeated calls
    on similar data pay nothing after warm-up.

    Time complexity:  O(1) — 4 lookups once the 256-entry table is warm.
    Space complexity: O(1) — at most 256 cache entries.
    """

    def reverseBits(self, n):
        return (
            (_reverse_byte((n >> 24) & 0xFF))
            | (_reverse_byte((n >> 16) & 0xFF) << 8)
            | (_reverse_byte((n >> 8) & 0xFF) << 16)
            | (_reverse_byte(n & 0xFF) << 24)
        )


# --- Tests ---


class TestReverseBits(unittest.TestCase):
    def setUp(self):
        self.solutions = [
            LoopSolution(),
            DivideConquerSolution(),
            StringSliceSolution(),
            ByteCacheSolution(),
        ]
        self.oracle = StringSliceSolution()

    def test_example_1(self):
        # 00000010100101000001111010011100 -> 00111001011110000010100101000000
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.reverseBits(43261596), 964176192)

    def test_example_2(self):
        # 01111111111111111111111111111100 -> 00111111111111111111111111111110
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.reverseBits(2147483644), 1073741822)

    def test_zero_maps_to_zero(self):
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.reverseBits(0), 0)

    def test_single_bit_travels_end_to_end(self):
        # Historical full-unsigned range: 1 (bit 0 set) must reverse to
        # bit 31 set. The current "n is even" constraint excludes this
        # input, but the reversal itself must handle it correctly.
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.reverseBits(1), 2**31)

    def test_historical_example_odd_input(self):
        # 11111111111111111111111111111101 -> 10111111111111111111111111111111
        # (official example from the pre-constraint-change statement).
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.reverseBits(4294967293), 3221225471)

    def test_power_of_two_sweep(self):
        # Bit k set must reverse to bit 31 - k set: a dense sweep over
        # every single-bit input in the legal space (all even for k>=1,
        # and k=0 covered by test_single_bit_travels_end_to_end).
        for k in range(32):
            for sol in self.solutions:
                with self.subTest(sol=type(sol).__name__, k=k):
                    self.assertEqual(sol.reverseBits(2**k), 2 ** (31 - k))

    def test_alternating_patterns(self):
        # Hand-derived constants: alternating masks swap partners under
        # reversal — 1010...10 -> 0101...01, 1100...00 -> 0011...1 (top
        # 16 bits down, bottom 16 up).
        cases = {
            0xAAAAAAAA: 0x55555555,
            0x55555555: 0xAAAAAAAA,
            0xFFFF0000: 0x0000FFFF,
            0x0000FFFF: 0xFFFF0000,
        }
        for n, expected in cases.items():
            for sol in self.solutions:
                with self.subTest(sol=type(sol).__name__, n=hex(n)):
                    self.assertEqual(sol.reverseBits(n), expected)

    def test_low_byte_sweep(self):
        # Dense check of all 256 single-byte input patterns: reversing a
        # one-byte word is its internal bit-reversal moved to the top of
        # the word — compared here against the string-format oracle.
        for b in range(256):
            expected = self.oracle.reverseBits(b)
            for sol in self.solutions:
                with self.subTest(sol=type(sol).__name__, b=b):
                    self.assertEqual(sol.reverseBits(b), expected)

    def test_agree_with_oracle_and_double_reversal_randomized(self):
        # Two oracles at once on random inputs drawn from the official
        # constraint space (0 <= n <= 2^31 - 2, n even):
        #   1. every solution matches the string-slicing reference, and
        #   2. reversing twice is the identity (bit reversal is an
        #      involution — each position maps to exactly one partner).
        import random

        rng = random.Random(190)
        for _ in range(500):
            n = rng.randint(0, 2**31 - 2)
            n -= n % 2  # honour the "n is even" constraint
            expected = self.oracle.reverseBits(n)
            for sol in self.solutions:
                with self.subTest(sol=type(sol).__name__, n=n):
                    self.assertEqual(sol.reverseBits(n), expected)
                    self.assertEqual(sol.reverseBits(sol.reverseBits(n)), n)


if __name__ == "__main__":
    unittest.main()
