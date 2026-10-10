"""
LeetCode #125 - Valid Palindrome (Easy)

A phrase is a palindrome if, after converting all uppercase letters
into lowercase letters and removing all non-alphanumeric characters,
it reads the same forward and backward. Alphanumeric characters
include letters and numbers.

Given a string s, return true if it is a palindrome, or false otherwise.

Example 1:
    Input: s = "A man, a plan, a canal: Panama"
    Output: true
    Explanation: "amanaplanacanalpanama" is a palindrome.

Example 2:
    Input: s = "race a car"
    Output: false
    Explanation: "raceacar" is not a palindrome.

Example 3:
    Input: s = " "
    Output: true
    Explanation: s is an empty string "" after removing
    non-alphanumeric characters. Since an empty string reads the same
    forward and backward, it is a palindrome.

Constraints:
    1 <= s.length <= 2 * 10^5
    s consists only of printable ASCII characters.
"""

import string
import unittest


class TwoPointerSolution:
    """Two pointers over the raw string — O(n) time, O(1) space.

    Keep one index at each end and walk them toward the middle:

      - `left` skips forward past any character that is not a letter
        or digit; `right` skips backward likewise.
      - When both pointers sit on alphanumeric characters, compare
        their lowercase forms. A mismatch means the cleaned string
        cannot be a palindrome, so we stop early.
      - If the pointers cross without ever finding a mismatch, every
        surviving character paired up correctly -> palindrome.

    Crossing pointers also handles the empty-after-cleaning case
    (e.g. " ") with no special-casing: an empty string is a palindrome.

    Note the invariants that keep the indices safe: after the skip
    loops we always re-check `left < right` before comparing, so a
    pointer can never run past the other one or off the string.

    Time complexity:  O(n) — each pointer travels at most n steps.
    Space complexity: O(1) — no cleaned copy of the string is built.
    """

    def isPalindrome(self, s):
        left, right = 0, len(s) - 1
        while left < right:
            # Move left to the next alphanumeric character.
            while left < right and not s[left].isalnum():
                left += 1
            # Move right to the previous alphanumeric character.
            while left < right and not s[right].isalnum():
                right -= 1
            # Compare the pair; bail out on the first mismatch.
            if s[left].lower() != s[right].lower():
                return False
            left += 1
            right -= 1
        return True


class FilterSolution:
    """Normalize-then-compare — O(n) time, O(n) space.

    Build the cleaned string once — lowercase letters and digits only —
    then compare it with its reversal. Python's slicing makes the
    reversal a one-liner, and `str.isalnum` + `str.lower` do the
    filtering. Simple and very fast in practice, at the cost of an
    O(n) scratch copy (fine for 2 * 10^5 chars).

    Time complexity:  O(n) — one pass to filter, one to reverse/compare.
    Space complexity: O(n) — the cleaned string and its reverse.
    """

    def isPalindrome(self, s):
        cleaned = [c.lower() for c in s if c.isalnum()]
        return cleaned == cleaned[::-1]


class AsciiOnlyTwoPointerSolution:
    """Two pointers with an explicit ASCII whitelist — O(n) time, O(1).

    Same algorithm as TwoPointerSolution, but membership is decided by
    a precomputed set of ASCII letters/digits instead of `str.isalnum`.
    This pins down the exact character class the constraints promise
    (printable ASCII) and avoids any locale/Unicode subtleties of
    `isalnum` — e.g. 'É'.isalnum() is True, but such characters cannot
    appear in the input anyway. A defensive-explicit variant kept for
    reference and cross-checking.

    Time complexity:  O(n) — each pointer travels at most n steps.
    Space complexity: O(1) — a fixed 62-entry lookup set.
    """

    _ALLOWED = set(string.ascii_letters + string.digits)

    def isPalindrome(self, s):
        left, right = 0, len(s) - 1
        while left < right:
            while left < right and s[left] not in self._ALLOWED:
                left += 1
            while left < right and s[right] not in self._ALLOWED:
                right -= 1
            if s[left].lower() != s[right].lower():
                return False
            left += 1
            right -= 1
        return True


class BruteForceSolution:
    """Reference O(n) extra-space scan with manual filtering — oracle.

    Builds the cleaned string character by character with explicit
    case folding, then compares mirror positions in a loop. Logically
    identical to FilterSolution but spelled out without slicing tricks,
    which makes it a good independent oracle for randomized tests.

    Time complexity:  O(n).
    Space complexity: O(n) — the cleaned list.
    """

    def isPalindrome(self, s):
        cleaned = []
        for c in s:
            if c.isdigit() or ("a" <= c <= "z") or ("A" <= c <= "Z"):
                cleaned.append(c.lower())
        for i in range(len(cleaned) // 2):
            if cleaned[i] != cleaned[-1 - i]:
                return False
        return True


# --- Tests ---


class TestValidPalindrome(unittest.TestCase):
    def setUp(self):
        self.solutions = [
            TwoPointerSolution(),
            FilterSolution(),
            AsciiOnlyTwoPointerSolution(),
        ]

    def test_example_1(self):
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertTrue(sol.isPalindrome("A man, a plan, a canal: Panama"))

    def test_example_2(self):
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertFalse(sol.isPalindrome("race a car"))

    def test_example_3_space_only(self):
        # Cleans to the empty string, which is a palindrome.
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertTrue(sol.isPalindrome(" "))

    def test_single_character(self):
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertTrue(sol.isPalindrome("a"))

    def test_all_punctuation(self):
        # Nothing survives filtering -> empty -> palindrome.
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertTrue(sol.isPalindrome(".,!?;:"))

    def test_mixed_alphanumeric_with_digits(self):
        # "0p" reversed is "p0" — not equal.
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertFalse(sol.isPalindrome("0P"))

    def test_digits_palindrome(self):
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertTrue(sol.isPalindrome("12321"))

    def test_case_insensitivity(self):
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertTrue(sol.isPalindrome("Ab_Ba"))

    def test_odd_length(self):
        # Middle character pairs with itself; "aba" is a palindrome.
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertTrue(sol.isPalindrome("a,b,a"))

    def test_palindrome_broken_by_inner_char(self):
        # "abca" fails at the second pair (b vs c).
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertFalse(sol.isPalindrome("ab1ca"))

    def test_long_alternating_mismatch(self):
        # A big string with exactly one mismatch buried inside.
        base = "a" * 5000
        s = base + "b" + base
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertTrue(sol.isPalindrome(s))
        s_bad = base + "b" + base + "c"
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertFalse(sol.isPalindrome(s_bad))

    def test_against_oracle_on_random_inputs(self):
        # Oracle test: all three solutions must agree with a manually
        # filtered mirror comparison on many random printable-ASCII
        # strings (mirrors the constraint that s is printable ASCII).
        import random

        rng = random.Random(125)  # fixed seed -> deterministic tests
        alphabet = string.printable
        oracle = BruteForceSolution()
        for _ in range(200):
            n = rng.randint(1, 60)
            s = "".join(rng.choice(alphabet) for _ in range(n))
            expected = oracle.isPalindrome(s)
            for sol in self.solutions:
                with self.subTest(sol=type(sol).__name__, s=s):
                    self.assertEqual(sol.isPalindrome(s), expected)


if __name__ == "__main__":
    unittest.main()
