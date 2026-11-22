"""
LeetCode #204 - Count Primes (Easy)

Given an integer n, return the number of prime numbers that are
strictly less than n.

Example 1:
    Input:  n = 10
    Output: 4
    Explanation: There are 4 prime numbers less than 10: 2, 3, 5, 7.

Example 2:
    Input:  n = 0
    Output: 0

Example 3:
    Input:  n = 1
    Output: 0

Constraints:
    0 <= n <= 5 * 10**6

Key insight: testing every integer below n for primality individually
costs O(n * sqrt(n)) and is hopeless at n = 5 * 10^6. The sieve of
Eratosthenes flips the work around: instead of asking "is k prime?"
once per k, it records for every k all the composites discovered by
the primes below it. Each composite is crossed out by its prime
factors, and the total crossing-out work is n * (1/2 + 1/3 + 1/5 + ...)
= n * log log n by Mertens' theorem — effectively linear. Two further
constant-factor tricks used below: only sieve odd numbers (2 is the
only even prime), and start crossing out at p*p because any smaller
multiple of p has a smaller prime factor and was already removed.
"""

import unittest


def _is_prime_trial_division(k):
    """Primality test by trial division up to sqrt(k).

    Used as the independent oracle for the tests. Handles k < 2 as
    "not prime" (0, 1 and negatives are excluded by definition);
    checks 2 separately, then only odd divisors, stepping over the
    even ones. E.g. 9: try 2, then 3 -> 9 % 3 == 0 -> composite.
    """
    if k < 2:
        return False
    if k == 2:
        return True
    if k % 2 == 0:
        return False
    d = 3
    while d * d <= k:
        if k % d == 0:
            return False
        d += 2
    return True


class TrialDivisionSolution:
    """Count primes by testing each candidate independently.

    For every k in [2, n) ask the oracle whether k is prime. This is
    the naive baseline the problem hints steer you away from: correct
    and simple, but quadratic-ish — at n = 5 * 10^6 it does billions
    of modulo operations. Included because it is the clearest
    statement of the specification and serves as the test oracle.

    Time complexity:  O(n * sqrt(n)) — n candidates, sqrt(k) work each.
    Space complexity: O(1).
    """

    def countPrimes(self, n):
        return sum(1 for k in range(2, n) if _is_prime_trial_division(k))


class SieveOfEratosthenesSolution:
    """Classic full-size sieve of Eratosthenes.

    Keep a boolean table is_prime[0..n-1]; assume everything prime,
    then for each p starting at 2 that is still marked prime, cross
    out p*p, p*(p+1), ... up to n. Start at p*p because any smaller
    multiple m = p*q with q < p was already crossed out when q was
    processed. Only iterate p up to sqrt(n): a composite below n has
    a factor <= sqrt(n), so nothing new happens beyond that point.
    The answer is simply how many entries survived — i.e. the prime
    counting function pi(n-1) counted over strictly-less-than n.

    Time complexity:  O(n log log n) — sum of n/p over primes p < n.
    Space complexity: O(n) — the boolean table.
    """

    def countPrimes(self, n):
        if n < 3:
            # No primes strictly below 0, 1 or 2.
            return 0
        is_prime = [True] * n
        is_prime[0] = is_prime[1] = False
        p = 2
        while p * p < n:
            if is_prime[p]:
                # Cross out p*p, p*p + p, ... — slice assignment lets
                # Python do the stride loop in C instead of bytecode.
                is_prime[p * p :: p] = [False] * len(is_prime[p * p :: p])
            p += 1
        return sum(is_prime)


class OddOnlyBytearraySolution:
    """Half-size sieve over odd numbers using a bytearray.

    Two optimizations stacked on the classic sieve. (1) Memory and
    cache: 2 is the only even prime, so store flags only for odd
    numbers — index i represents the number 2*i + 1 (and index 0 is
    pinned to "not prime" since 1 is not prime). This halves the
    table: 5 * 10^6 numbers fit in 2.5 MB of a bytearray instead of
    a 40 MB list of Python bool objects. (2) Type: bytearray is a
    flat C buffer, so slice assignment with a bytes object of the
    right length crosses out a whole arithmetic progression in one
    C-level memcpy-like pass. The count is recovered as 1 (for the
    prime 2, absent from the table) plus the surviving odd flags
    below n.

    Time complexity:  O(n log log n) — half the constants of the
                      classic sieve.
    Space complexity: O(n) bits-per-flag = n/2 bytes.
    """

    def countPrimes(self, n):
        if n < 3:
            return 0
        # Sieve over candidates 1, 3, 5, ..., i.e. numbers 2*i + 1
        # for i in [0, (n-1)//2]. Largest index needed: 2*i+1 < n.
        size = n // 2  # covers all odd numbers below n
        sieve = bytearray([1]) * size
        sieve[0] = 0  # 1 is not prime
        i = 1
        while (2 * i + 1) ** 2 < n:
            if sieve[i]:
                p = 2 * i + 1
                # First composite to cross out is p*p = (2i+1)^2,
                # an odd number, at index (p*p - 1) // 2 = 2*i*i + 2*i.
                # Stepping by p in index space moves by 2*p in value
                # space, staying on odd multiples of p only.
                start = 2 * i * (i + 1)
                sieve[start::p] = bytes(len(sieve[start::p]))
            i += 1
        # +1 accounts for the prime 2, which the odd-only table omits.
        return 1 + sum(sieve)


# --- Tests ---


class TestCountPrimes(unittest.TestCase):
    def setUp(self):
        self.solutions = [
            TrialDivisionSolution(),
            SieveOfEratosthenesSolution(),
            OddOnlyBytearraySolution(),
        ]
        self.oracle = TrialDivisionSolution()

    def test_example_1(self):
        # Primes below 10: 2, 3, 5, 7.
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.countPrimes(10), 4)

    def test_example_2(self):
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.countPrimes(0), 0)

    def test_example_3(self):
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.countPrimes(1), 0)

    def test_strictly_less_than_boundary(self):
        # "strictly less than n": moving the exclusive bound from n to
        # n + 1 adds exactly one prime iff n itself is prime; for a
        # composite n the count must not change.
        for n in range(2, 50):
            expected_delta = 1 if _is_prime_trial_division(n) else 0
            for sol in self.solutions:
                with self.subTest(sol=type(sol).__name__, n=n):
                    delta = sol.countPrimes(n + 1) - sol.countPrimes(n)
                    self.assertEqual(delta, expected_delta)

    def test_known_prime_counting_values(self):
        # pi(x) values of the prime counting function (OEIS A006880):
        # pi(10)=4, pi(100)=25, pi(10^3)=168, pi(10^4)=1229, pi(10^5)=9592.
        # countPrimes(n) = pi(n - 1); for n = 10^k + 1 that is pi(10^k).
        known = {11: 4, 101: 25, 1001: 168, 10001: 1229, 100001: 9592}
        for n, expected in known.items():
            for sol in self.solutions:
                with self.subTest(sol=type(sol).__name__, n=n):
                    self.assertEqual(sol.countPrimes(n), expected)

    def test_agree_with_oracle_dense_sweep(self):
        # Every solution must match the trial-division oracle on a
        # dense sweep of the small range, catching off-by-one errors
        # at 0, 1, 2, 3 and 4 in particular.
        for n in range(0, 200):
            expected = self.oracle.countPrimes(n)
            for sol in self.solutions:
                with self.subTest(sol=type(sol).__name__, n=n):
                    self.assertEqual(sol.countPrimes(n), expected)

    def test_agree_with_oracle_randomized(self):
        # Random inputs from the official constraint space: the fast
        # sieves must agree with the oracle on scattered large n.
        import random

        rng = random.Random(204)
        for _ in range(50):
            n = rng.randint(0, 200000)
            expected = self.oracle.countPrimes(n)
            for sol in self.solutions:
                with self.subTest(sol=type(sol).__name__, n=n):
                    self.assertEqual(sol.countPrimes(n), expected)

    def test_large_input_performance(self):
        # pi(10^6) = 78498 — a full-constraint-scale smoke test for the
        # sieves (the trial-division oracle is too slow to join here).
        for sol in (SieveOfEratosthenesSolution(), OddOnlyBytearraySolution()):
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.countPrimes(1000000), 78498)


if __name__ == "__main__":
    unittest.main()
