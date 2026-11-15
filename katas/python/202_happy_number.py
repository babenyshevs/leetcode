"""
LeetCode #202 - Happy Number (Easy)

Write an algorithm to determine if a number is "happy".

A happy number is defined by the following process: starting with any
positive integer, replace the number by the sum of the squares of its
digits, and repeat the process until the number equals 1 (where it will
stay), or it loops endlessly in a cycle which does not include 1.
Numbers for which this process ends in 1 are happy numbers.

Example 1:
    Input:  n = 19
    Output: true
    Explanation:
        1^2 + 9^2 = 82
        8^2 + 2^2 = 68
        6^2 + 8^2 = 100
        1^2 + 0^2 + 0^2 = 1

Example 2:
    Input:  n = 2
    Output: false   (2 is trapped in the cycle 2 -> 4 -> 20 -> 4 -> ...)

Constraints:
    1 <= n <= 2**31 - 1

Key insight: every value in the process is eventually bounded. A number
with d digits has sum of digit squares <= 81*d, so any number below 10^3
maps to at most 243 and every starting value falls into that region after
a few steps. Because the successor function is deterministic, the
sequence must either hit 1 (happy) or repeat a value (stuck in a cycle
that does not include 1 — the classic one is 4 -> 16 -> 37 -> 58 -> 89
-> 145 -> 42 -> 20 -> 4). Detecting "repeat" is exactly cycle detection,
solved either with a set (O(n) memory) or Floyd's tortoise-and-hare
(O(1) memory), and — since the only cycle is known — even by checking
for a member of that cycle.
"""

import unittest


def _sum_of_squared_digits(n):
    """One step of the process: replace n by the sum of squared digits.

    Peels digits from the low end with divmod — no string conversion,
    no extra allocation. E.g. 19 -> 1*1 + 9*9 = 82.
    """
    total = 0
    while n:
        n, digit = divmod(n, 10)
        total += digit * digit
    return total


class HashSetSolution:
    """Simulate the process and remember every value seen.

    Iterate the digit-square-sum function; if we reach 1 the number is
    happy, if we reach a value we have seen before we are inside a cycle
    and can never reach 1. Correct because the successor function is
    deterministic: a repeated value means the sequence is periodic
    forever after. This is the clearest solution and serves as the test
    oracle below.

    Time complexity:  O(log n) per step, and the sequence drops below
                      243 within a few steps, so O(log n) steps overall.
    Space complexity: O(log n) — the set of seen values is bounded by a
                      constant (<= 243 distinct values below the bound).
    """

    def isHappy(self, n):
        seen = set()
        while n != 1 and n not in seen:
            seen.add(n)
            n = _sum_of_squared_digits(n)
        return n == 1


class FloydCycleSolution:
    """Floyd's cycle detection (tortoise and hare) — O(1) memory.

    Treat the process as a functional graph where each node n points to
    _sum_of_squared_digits(n). A happy number's path ends at the fixed
    point 1; an unhappy number's path is a rho shape ending in a cycle
    that misses 1. Advance a slow pointer one step and a fast pointer
    two steps per round: if there is a cycle they must meet inside it
    (fast gains one position per round on a loop); if there is no cycle
    both reach 1. Happy iff slow reaches 1.

    Time complexity:  O(log n) — same step count as the set solution,
                      each round does at most 3 successor computations.
    Space complexity: O(1) — only two pointers, no auxiliary structure.
    """

    def isHappy(self, n):
        slow = n
        fast = _sum_of_squared_digits(n)
        while fast != 1 and slow != fast:
            slow = _sum_of_squared_digits(slow)
            fast = _sum_of_squared_digits(_sum_of_squared_digits(fast))
        return fast == 1


class HardcodedCycleSolution:
    """Short-circuit on the known unhappy cycle — constant work.

    All unhappy numbers funnel into the single 8-node cycle
    4 -> 16 -> 37 -> 58 -> 89 -> 145 -> 42 -> 20 -> 4. It therefore
    suffices to iterate until n is 1 (happy) or 4 (unhappy). Checking
    just the member 4 is enough because the cycle always passes through
    it. Fastest constant factor of the three, at the price of encoding
    a mathematical fact rather than detecting cycles generically.

    Time complexity:  O(log n) — a handful of steps to fall below 243,
                      then at most 8 more to land on 4 or 1.
    Space complexity: O(1).
    """

    def isHappy(self, n):
        while n != 1 and n != 4:
            n = _sum_of_squared_digits(n)
        return n == 1


class PythonicSolution:
    """String-based digit-square sum — readable one-pass variant.

    str(n) iterates the digits directly; sum the squares with a
    generator expression. Allocation makes it slower than divmod, but
    it is the most transparent expression of "sum of squares of its
    digits" and doubles as an independent oracle: it computes the
    successor through a completely different mechanism (string vs.
    arithmetic), so agreement between solutions is meaningful evidence.

    Time complexity:  O(log n) per step (d digits, d = log10 n + 1).
    Space complexity: O(log n) — one short string per step.
    """

    def isHappy(self, n):
        seen = set()
        while n != 1 and n not in seen:
            seen.add(n)
            n = sum(int(ch) ** 2 for ch in str(n))
        return n == 1


# --- Tests ---


class TestIsHappy(unittest.TestCase):
    def setUp(self):
        self.solutions = [
            HashSetSolution(),
            FloydCycleSolution(),
            HardcodedCycleSolution(),
            PythonicSolution(),
        ]
        self.oracle = HashSetSolution()

    def test_example_1(self):
        # 19 -> 82 -> 68 -> 100 -> 1
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertTrue(sol.isHappy(19))

    def test_example_2(self):
        # 2 loops in the cycle 2 -> 4 -> 20 -> 4 -> ...
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertFalse(sol.isHappy(2))

    def test_trivial_happy(self):
        # The smallest legal input is already the fixed point.
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertTrue(sol.isHappy(1))

    def test_known_happy_numbers_up_to_100(self):
        # OEIS A007770 (happy numbers), initial terms <= 100.
        known_happy = {
            1, 7, 10, 13, 19, 23, 28, 31, 32, 44, 49,
            68, 70, 79, 82, 86, 91, 94, 97, 100,
        }
        for n in range(1, 101):
            expected = n in known_happy
            for sol in self.solutions:
                with self.subTest(sol=type(sol).__name__, n=n):
                    self.assertEqual(sol.isHappy(n), expected)

    def test_single_digit_numbers(self):
        # Hand-derived: only 1 and 7 among 1..9 are happy; e.g.
        # 7 -> 49 -> 97 -> 130 -> 10 -> 1, while 3 enters the 4-cycle.
        happy_single = {1, 7}
        for n in range(1, 10):
            for sol in self.solutions:
                with self.subTest(sol=type(sol).__name__, n=n):
                    self.assertEqual(sol.isHappy(n), n in happy_single)

    def test_maximum_input(self):
        # Largest legal input 2**31 - 1: successor chain is
        # 260 -> 40 -> 16 -> ... -> the 4-cycle, so unhappy.
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertFalse(sol.isHappy(2**31 - 1))

    def test_powers_of_ten_are_happy(self):
        # 10^k collapses to 1 immediately (digit squares 1 + 0 + ...).
        for k in range(10):
            for sol in self.solutions:
                with self.subTest(sol=type(sol).__name__, k=k):
                    self.assertTrue(sol.isHappy(10**k))

    def test_agree_with_oracle_randomized(self):
        # Random inputs drawn from the official constraint space
        # (1 <= n <= 2**31 - 1): every solution must match the oracle.
        import random

        rng = random.Random(202)
        for _ in range(300):
            n = rng.randint(1, 2**31 - 1)
            expected = self.oracle.isHappy(n)
            for sol in self.solutions:
                with self.subTest(sol=type(sol).__name__, n=n):
                    self.assertEqual(sol.isHappy(n), expected)

    def test_successor_function_agrees_between_oracles(self):
        # The arithmetic and string successor implementations must be
        # equivalent on a dense sweep; this validates the mechanism,
        # not just the final yes/no answer.
        for n in range(1, 2000):
            arithmetic = _sum_of_squared_digits(n)
            string_based = sum(int(ch) ** 2 for ch in str(n))
            with self.subTest(n=n):
                self.assertEqual(arithmetic, string_based)


if __name__ == "__main__":
    unittest.main()
