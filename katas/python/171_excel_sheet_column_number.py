"""
LeetCode #171 - Excel Sheet Column Number (Easy)

Given a string columnTitle that represents the column title as appears
in an Excel sheet, return its corresponding column number.

For example:
    A -> 1
    B -> 2
    C -> 3
    ...
    Z -> 26
    AA -> 27
    AB -> 28
    ...

Example 1:
    Input:  columnTitle = "A"
    Output: 1

Example 2:
    Input:  columnTitle = "AB"
    Output: 28

Example 3:
    Input:  columnTitle = "ZY"
    Output: 701

Constraints:
    1 <= columnTitle.length <= 7
    columnTitle consists only of uppercase English letters.
    columnTitle is in the range ["A", "FXSHRXW"].

Note: this is the inverse of problem 168 (Excel Sheet Column Title).
It is a *bijective* base-26 numeral system: digits run 1..26 (A..Z)
and there is no zero digit, so a plain "subtract the ordinal" mapping
plus a positional power-of-26 accumulation converts a title back to
its number. The largest input, "FXSHRXW", decodes to 2,147,483,647 =
2^31 - 1 — Excel column titles end exactly at INT32_MAX.
"""

import unittest
from functools import reduce
from string import ascii_uppercase


class HornerSolution:
    """Left-to-right accumulation — Horner's method in base 26.

    Reading the title from left to right, each new character shifts
    everything decoded so far up by one 26-place and appends the new
    digit. For title c_1 c_2 ... c_k:

        result = ((...((c_1)*26 + c_2)*26 + c_3) ... )*26 + c_k

    This is exactly Horner's scheme for evaluating a polynomial whose
    coefficients are the digit values, and it generalises unchanged to
    any bijective base. Digit value: ord(c) - ord('A') + 1 (A=1 ... Z=26;
    the +1 is what makes this bijective base rather than base-26-with-zero).

    Time complexity:  O(n) — one pass over the title (n <= 7 here).
    Space complexity: O(1) — a single accumulator.
    """

    def titleToNumber(self, columnTitle):
        result = 0
        for ch in columnTitle:
            result = result * 26 + (ord(ch) - ord("A") + 1)
        return result


class PositionalSolution:
    """Right-to-left positional notation — sum digit * 26^position.

    The textbook place-value formula: the rightmost letter contributes
    d_k * 26^0, the next d_{k-1} * 26^1, and so on. enumerate() over the
    reversed string yields each digit together with its place index, so
    no explicit pow() call bookkeeping is needed beyond 26 ** place.

    Equivalent to Horner's method in result, but it makes the positional
    structure explicit: character i from the right is the coefficient of
    26^i. O(n) time (26 ** i on ints of <= 7 places is trivial), O(n)
    space for the reversed copy.
    """

    def titleToNumber(self, columnTitle):
        total = 0
        for place, ch in enumerate(reversed(columnTitle)):
            total += (ord(ch) - ord("A") + 1) * 26**place
        return total


class ReduceSolution:
    """One-line fold with functools.reduce — Horner's method, terser.

    Same left-to-right accumulation as HornerSolution, expressed as a
    fold: start from 0 and repeatedly fold in each character's digit via
    acc * 26 + digit. Included to show the idiomatic functional form;
    the explicit loop above stays easier to read and debug.

    Time complexity:  O(n).
    Space complexity: O(1).
    """

    def titleToNumber(self, columnTitle):
        return reduce(
            lambda acc, ch: acc * 26 + (ord(ch) - ord("A") + 1), columnTitle, 0
        )


# --- Tests ---


def encode_number(n):
    """Inverse mapping (problem 168): number -> column title.

    Used as the oracle for randomized round-trip tests. Bijective
    base-26 encoding: subtract 1 before each mod so that digits run
    1..26 and wrap A..Z without a zero digit (e.g. 26 -> "Z" not "10").
    """
    digits = []
    while n > 0:
        n, rem = divmod(n - 1, 26)
        digits.append(ascii_uppercase[rem])
    return "".join(reversed(digits))


class TestExcelSheetColumnNumber(unittest.TestCase):
    def setUp(self):
        self.solutions = [
            HornerSolution(),
            PositionalSolution(),
            ReduceSolution(),
        ]

    def test_example_1(self):
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.titleToNumber("A"), 1)

    def test_example_2(self):
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.titleToNumber("AB"), 28)

    def test_example_3(self):
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.titleToNumber("ZY"), 701)

    def test_all_single_letters(self):
        # A..Z must map to 1..26 in order — the digit alphabet itself.
        for index, letter in enumerate(ascii_uppercase, start=1):
            for sol in self.solutions:
                with self.subTest(sol=type(sol).__name__, letter=letter):
                    self.assertEqual(sol.titleToNumber(letter), index)

    def test_two_letter_boundaries(self):
        # Carry boundaries of the bijective system: AA is the first
        # title after Z, AZ the last starting with A, BA the first
        # after AZ, ZZ the last two-letter title (26 + 26^2 = 702).
        cases = {"AA": 27, "AZ": 52, "BA": 53, "ZZ": 702}
        for title, expected in cases.items():
            for sol in self.solutions:
                with self.subTest(sol=type(sol).__name__, title=title):
                    self.assertEqual(sol.titleToNumber(title), expected)

    def test_max_input_is_int32_max(self):
        # Constraint ceiling "FXSHRXW" decodes to 2,147,483,647 —
        # exactly 2^31 - 1, the largest 32-bit signed integer.
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.titleToNumber("FXSHRXW"), 2**31 - 1)

    def test_against_encode_oracle_randomized(self):
        # Oracle: build titles from random numbers with the inverse
        # mapping (the problem-168 encoder) and check the decode
        # round-trips: titleToNumber(encode(n)) == n. Range covers the
        # full legal input space: 1 .. 2^31 - 1 ("FXSHRXW" inclusive).
        import random

        rng = random.Random(171)
        for _ in range(500):
            n = rng.randint(1, 2**31 - 1)
            title = encode_number(n)
            # The generated title must itself be a legal input:
            # uppercase letters only, length <= 7.
            self.assertLessEqual(len(title), 7)
            for sol in self.solutions:
                with self.subTest(sol=type(sol).__name__, n=n):
                    self.assertEqual(sol.titleToNumber(title), n)

    def test_full_dense_sweep_A_to_ZZ(self):
        # Every title from A to ZZ decodes to consecutive numbers 1..702
        # — a dense sweep exercising the base-26 carries at every roll-
        # over: Z->AA (26->27), AZ->BA (52->53), and ZZ->(next) 702.
        # Titles enumerate consecutively only when the MOST significant
        # position is the outer loop (like digits: tens before units).
        # The consecutive enumeration itself is the oracle here: it is
        # exactly how Excel titles are defined (A, B, ... Z, AA, ...).
        expected = 0
        for first in [""] + list(ascii_uppercase):
            for second in ascii_uppercase:
                expected += 1
                title = first + second
                results = {
                    type(sol).__name__: sol.titleToNumber(title)
                    for sol in self.solutions
                }
                with self.subTest(title=title):
                    self.assertEqual(set(results.values()), {expected})


if __name__ == "__main__":
    unittest.main()
