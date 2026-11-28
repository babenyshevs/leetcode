"""
LeetCode #205 - Isomorphic Strings (Easy)

Given two strings s and t, determine if they are isomorphic.

Two strings s and t are isomorphic if the characters in s can be
replaced to get t.

All occurrences of a character must be replaced with another character
while preserving the order of characters. No two characters may map to
the same character, but a character may map to itself.

Example 1:
    Input:  s = "egg", t = "add"
    Output: true
    Explanation: 'e' -> 'a' and 'g' -> 'd' is a consistent replacement.

Example 2:
    Input:  s = "foo", t = "bar"
    Output: false
    Explanation: 'o' would need to map to both 'a' and 'r'.

Example 3:
    Input:  s = "paper", t = "title"
    Output: true
    Explanation: 'p'->'t', 'a'->'i', 'e'->'l', 'r'->'e' works; note the
    mapping is not injective in the familiar sense ('p'->'t' and
    'r'->'e' with 'e'->'l') — what matters is that it is a valid
    function s->t AND a valid function t->s (a bijection between the
    distinct characters actually used).

Constraints:
    1 <= s.length <= 5 * 10**4
    t.length == s.length
    s and t consist of any valid ascii character.

Key insight: "isomorphic" means the replacement rule is a bijection
between the distinct characters of s and the distinct characters of t.
A one-directional map s -> t is not enough: it would wrongly accept
("ab", "aa") because 'a' and 'b' both collapse onto 'a' — but a
replacement must be invertible, so two different source characters can
never share a target. Every correct solution therefore enforces both
directions. The classic trap is the reverse check: s = "badc" and
t = "baba" pass a forward-only map ('b'->'b', 'a'->'a', 'd'->'b',
'c'->'a' is never contradicted) yet fail because 'b' and 'd' both map
to 'b'.
"""

import unittest


class TwoDictionarySolution:
    """Track the bijection explicitly in both directions.

    Walk both strings in lockstep. forward maps each character of s to
    the character of t it was first aligned with; backward maps each
    character of t to the character of s that produced it. At every
    position, if either dictionary already holds a *different* value
    for the current character, the bijection is broken and the answer
    is False. Otherwise record the (consistent) pair and continue. If
    we survive to the end, both directions were never contradicted,
    which is exactly the definition of an isomorphism.

    Time complexity:  O(n) — one pass, O(1) dict work per character.
    Space complexity: O(k) — k = alphabet size (at most 128 for ASCII,
                      bounded by min(n, 128)); both dicts hold at most
                      one entry per distinct character.
    """

    def isIsomorphic(self, s, t):
        if len(s) != len(t):
            return False
        forward, backward = {}, {}
        for cs, ct in zip(s, t):
            if forward.setdefault(cs, ct) != ct:
                return False
            if backward.setdefault(ct, cs) != cs:
                return False
        return True


class FirstOccurrencePatternSolution:
    """Compare canonical fingerprints instead of mappings.

    Two strings are isomorphic iff they have the same "shape": replace
    every character by the index (0-based) of its first occurrence and
    both strings must become identical integer sequences. E.g.
    'p'->0, 'a'->1, 'p'->0, 'e'->2, 'r'->3 gives [0,1,0,2,3] for
    "paper", and 't'->0, 'i'->1, 't'->0, 'l'->2, 'e'->3 gives
    [0,1,0,2,3] for "title" — equal, so isomorphic.
    Equal fingerprints mean there is an order-preserving bijection
    between first occurrences — which is exactly isomorphism — and it
    sidesteps the reverse-map trap entirely because two different
    source characters can never produce the same fingerprint position
    unless their targets also matched.

    The implementation builds the fingerprint lazily: `seen` maps a
    character to the next unused pattern id, so `map[c]` is both a
    lookup and an assignment in one expression.

    Time complexity:  O(n) — one fingerprint pass per string, one
                      equality check.
    Space complexity: O(k + n) for the two fingerprints (O(k) for the
                      dictionary; the lists are unavoidable in this
                      formulation).
    """

    def isIsomorphic(self, s, t):
        def fingerprint(string):
            seen = {}
            pattern = []
            for ch in string:
                # setdefault: first sight assigns the next id, later
                # sights return the id assigned at first occurrence.
                pattern.append(seen.setdefault(ch, len(seen)))
            return pattern

        if len(s) != len(t):
            return False
        return fingerprint(s) == fingerprint(t)


class SetZipOneLinerSolution:
    """Count distinct pairings three ways with sets.

    The bijection condition has a slick set-theoretic form. Build the
    set of aligned pairs P = {(s[i], t[i])}. If |set(s)| == |set(t)|
    == |P| then:
      * |set(s)| == |P|: no character of s appears in two different
        pairs, so forward mapping is a function;
      * |set(t)| == |P|: no character of t appears in two different
        pairs, so the mapping is injective from t's side too.
    Both together mean the pairs form a bijection between the distinct
    characters — exactly isomorphism. Any violation (one-to-many or
    many-to-one) collapses one of the three set sizes below |P|.

    Time complexity:  O(n) — building each set is a linear scan.
    Space complexity: O(k) — the sets hold distinct characters/pairs
                      only, bounded by the alphabet size.
    """

    def isIsomorphic(self, s, t):
        return len(set(s)) == len(set(t)) == len(set(zip(s, t)))


# --- Tests ---


class TestIsomorphicStrings(unittest.TestCase):
    def setUp(self):
        self.solutions = [
            TwoDictionarySolution(),
            FirstOccurrencePatternSolution(),
            SetZipOneLinerSolution(),
        ]

    def _check(self, s, t, expected):
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__, s=s, t=t):
                self.assertEqual(sol.isIsomorphic(s, t), expected)

    def test_example_1(self):
        self._check("egg", "add", True)

    def test_example_2(self):
        # 'o' would need two different targets.
        self._check("foo", "bar", False)

    def test_example_3(self):
        self._check("paper", "title", True)

    def test_identity_mapping(self):
        # A character may map to itself.
        self._check("abcabc", "abcabc", True)

    def test_forward_only_trap(self):
        # Passes a forward-only map ('d'->'b', 'c'->'a' never
        # contradicted) but 'b' and 'd' both map to 'b': needs the
        # reverse check. Classic discussion-board counterexample.
        self._check("badc", "baba", False)

    def test_many_to_one_trap(self):
        # Forward map is consistent but not injective: 'a' and 'b'
        # both collapse onto 'a'.
        self._check("ab", "aa", False)

    def test_one_to_many_trap(self):
        # Mirror image of the previous trap: 'a' would need to be
        # replaced by both 'b' and 'c'.
        self._check("aa", "bc", False)

    def test_single_character(self):
        # Constraint minimum length 1; any single pair is isomorphic.
        self._check("x", "y", True)
        self._check("x", "x", True)

    def test_distinct_alphabets_same_shape(self):
        # Completely different characters, identical positions of
        # first occurrences.
        self._check("abcdefabcdef", "zyxwvuzyxwvu", True)

    def test_same_alphabet_different_pattern(self):
        # Same alphabet, but no bijection reproduces the target: for
        # "abba" vs "abab" neither the identity (gives "abba") nor the
        # swap a<->b (gives "baab") matches.
        self._check("abba", "abab", False)
        # Same-length rotation IS isomorphic: swap a<->b maps
        # "abab" -> "baba".
        self._check("abab", "baba", True)

    def test_case_sensitivity(self):
        # ASCII constraint: 'A' and 'a' are different characters.
        self._check("Aa", "aa", False)
        self._check("Aa", "Bb", True)

    def test_non_letter_ascii(self):
        # "any valid ascii character" — digits and punctuation too.
        self._check("12 12", "!@ !@", True)
        self._check("12 12", "!@  !", False)

    def test_agree_with_bruteforce_oracle_small_alphabet(self):
        # Exhaustive agreement check over every pair of strings of
        # length 4 from a 3-letter alphabet (3^8 = 6561 pairs) against
        # a definition-level oracle: try ALL injective maps from the
        # distinct characters of s to characters of t and see if any
        # reproduces t. Slow but undeniably correct.
        from itertools import permutations, product

        alphabet = "abc"

        def oracle(s, t):
            distinct_s = set(s)
            for perm in permutations(set(t) | set(alphabet), len(distinct_s)):
                mapping = dict(zip(distinct_s, perm))
                if "".join(mapping[c] for c in s) == t:
                    return True
            return False

        for s in map("".join, product(alphabet, repeat=4)):
            for t in map("".join, product(alphabet, repeat=4)):
                expected = oracle(s, t)
                for sol in self.solutions:
                    with self.subTest(sol=type(sol).__name__, s=s, t=t):
                        self.assertEqual(sol.isIsomorphic(s, t), expected)

    def test_full_constraint_scale(self):
        # 5 * 10^4 characters at maximum constraint scale: all
        # solutions must stay fast and agree on a known-answer input.
        n = 5 * 10 ** 4
        s = ("ab" * (n // 2))[:n]
        t = ("xy" * (n // 2))[:n]
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertTrue(sol.isIsomorphic(s, t))
        # Flip one character near the end to break the bijection.
        bad = t[:-1] + "z"
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertFalse(sol.isIsomorphic(s, bad))


if __name__ == "__main__":
    unittest.main()
