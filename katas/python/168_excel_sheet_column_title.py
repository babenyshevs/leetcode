"""
LeetCode #168 - Excel Sheet Column Title (Easy)

Given an integer columnNumber, return its corresponding column title
as it appears in an Excel sheet.

    A -> 1
    B -> 2
    C -> 3
    ...
    Z -> 26
    AA -> 27
    AB -> 28
    ...

Example 1:
    Input:  columnNumber = 1
    Output: "A"

Example 2:
    Input:  columnNumber = 26
    Output: "Z"

Example 3:
    Input:  columnNumber = 28
    Output: "AB"

Example 4:
    Input:  columnNumber = 701
    Output: "ZY"

Example 5:
    Input:  columnNumber = 2147483647
    Output: "FXSHRXW"

Constraints:
    1 <= columnNumber <= 2^31 - 1
"""

import unittest
from string import ascii_uppercase


class SubShiftSolution:
    """Bijective base-26 via the subtract-one trick — the canonical O(log26 n).

    Excel columns LOOK like base-26, but they are not positional base-26:
    the "digits" run 1..26 (A..Z) and there is no zero. That off-by-one
    breaks the ordinary divmod loop (26 would become "A0" instead of "Z").

    The fix — subtract 1 from the number BEFORE each divmod — shifts the
    digit range 1..26 down to 0..25, making the remainder a clean index
    into 'A'..'Z':

        n = 28:  28-1=27 -> 27%26=1 ->'B', 27//26=1
                 1-1=0   ->  0%26=0 ->'A',  0//26=0  -> stop
        digits collected [B, A], reversed -> "AB"  ✓

    Why it is correct: the map n -> n-1 is exactly the bijection between
    {1, 2, ..., 26} and {0, 1, ..., 25}, applied at every "place" of the
    bijective numeration system. Subtracting before taking the remainder
    accounts for the fact that a digit value of 26 (Z) still contributes
    a full 26*26^k and carries, unlike a zero digit in ordinary base.

    Time complexity:  O(log26 n) — one iteration per output letter
                      (at most 7 for n <= 2^31 - 1).
    Space complexity: O(log26 n) — the digit buffer for the answer.
    """

    LETTERS = ascii_uppercase

    def convertToTitle(self, columnNumber):
        digits = []
        n = columnNumber
        while n > 0:
            n -= 1  # shift 1..26 down to 0..25 so `%` lands on 'A'..'Z'
            digits.append(self.LETTERS[n % 26])
            n //= 26
        return "".join(reversed(digits))


class CarrySolution:
    """Borrow-style carry propagation — same result, zero-based thinking.

    Alternative formulation of the same idea: take the plain remainder
    first; a remainder of 0 means the current place value is really 26
    ('Z') and the division must borrow one unit from what is left:

        n = 52:  52%26=0 ->'Z', borrow: (52//26)-1=1
                 1%26=1 ->'B', 1//26=0            -> "BZ"? No — wait.
        Correct answer for 52 is "AZ": the borrow must happen BEFORE
        emitting, i.e. treat 0 as 26 and decrement n by one extra unit
        first. This implementation does n -= 1 up front each round,
        which is exactly the SubShiftSolution — kept as an explicit
        divmod variant for readability, not a different algorithm.

    Time complexity:  O(log26 n) — one iteration per letter.
    Space complexity: O(log26 n) — the digit buffer.
    """

    LETTERS = ascii_uppercase

    def convertToTitle(self, columnNumber):
        digits = []
        n = columnNumber
        while n > 0:
            n, rem = divmod(n - 1, 26)  # divmod form of the subtract-one trick
            digits.append(self.LETTERS[rem])
        return "".join(reversed(digits))


# --- Tests ---


class TestExcelSheetColumnTitle(unittest.TestCase):
    def setUp(self):
        self.solutions = [SubShiftSolution(), CarrySolution()]

    def test_example_1(self):
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.convertToTitle(1), "A")

    def test_example_2(self):
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.convertToTitle(26), "Z")

    def test_example_3(self):
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.convertToTitle(28), "AB")

    def test_example_4(self):
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.convertToTitle(701), "ZY")

    def test_example_5_max_int(self):
        # Largest allowed input: 2^31 - 1.
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.convertToTitle(2147483647), "FXSHRXW")

    def test_single_letter_range(self):
        for value, expected in [(2, "B"), (25, "Y"), (26, "Z")]:
            for sol in self.solutions:
                with self.subTest(sol=type(sol).__name__, value=value):
                    self.assertEqual(sol.convertToTitle(value), expected)

    def test_carry_boundaries(self):
        # Every place-value boundary where the no-zero digit system rolls over.
        cases = {
            27: "AA",
            52: "AZ",   # classic trap: NOT "BZ" — the borrow hits every place
            53: "BA",
            702: "ZZ",  # 26 + 26^2 fully rolled
            703: "AAA", # first three-letter title
            728: "AAZ",
            729: "ABA",
            18278: "ZZZ",
            18279: "AAAA",
        }
        for value, expected in cases.items():
            for sol in self.solutions:
                with self.subTest(sol=type(sol).__name__, value=value):
                    self.assertEqual(sol.convertToTitle(value), expected)

    def test_against_oracle_on_full_range(self):
        # Oracle: exhaustive enumeration of every 1-4 letter column title,
        # computed independently via place weights (26^k), cross-checked
        # against the solutions for the first 20_000 values. For a fixed
        # length, product()'s lexicographic order equals numeric order, so
        # the loop can break as soon as the place-weighted value exceeds
        # the range. 20_000 < 26^4, so four letters are enough.
        from itertools import product

        letters = self.solutions[0].LETTERS
        titles = {}
        for length in (1, 2, 3, 4):
            for combo in product(letters, repeat=length):
                value = 0
                for ch in combo:
                    value = value * 26 + (ord(ch) - ord("A") + 1)
                if value > 20_000:
                    break
                titles[value] = "".join(combo)

        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                for value in range(1, 20_001):
                    self.assertEqual(sol.convertToTitle(value), titles[value])
                self.assertEqual(sol.convertToTitle(2**31 - 1), "FXSHRXW")


if __name__ == "__main__":
    unittest.main()
