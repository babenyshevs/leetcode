"""
LeetCode #119 - Pascal's Triangle II (Easy)

Given an integer rowIndex, return the rowIndex-th (0-indexed) row of
Pascal's triangle.

In Pascal's triangle, each number is the sum of the two numbers directly
above it. Row 0 is [1]; row 1 is [1, 1].

Follow-up: Could you optimize your algorithm to use only O(rowIndex)
extra space?

Example 1:
    Input: rowIndex = 3
    Output: [1,3,3,1]

Example 2:
    Input: rowIndex = 0
    Output: [1]

Example 3:
    Input: rowIndex = 1
    Output: [1,1]

Constraints:
    0 <= rowIndex <= 33
"""

import unittest


class InPlaceDPSolution:
    """Build a single row in place — O(rowIndex^2) time, O(rowIndex) space.

    This is the classic 1-D DP trick the follow-up asks for. Row 0 is a
    list of 1s of the right length; to morph row i - 1 into row i we walk
    from RIGHT to LEFT and do row[j] += row[j - 1].

    The direction is the whole trick: updating right to left means
    row[j - 1] still holds its "previous row" value when row[j] reads it.
    A left to right pass would overwrite row[j - 1] first, so row[j]
    would add a value that already belongs to row i — garbage results.

    Time complexity:  O(rowIndex^2) — row i needs O(i) additions.
    Space complexity: O(rowIndex) — one list, updated in place.
    """

    def getRow(self, rowIndex):
        # Start from a row of all 1s: the edges are already correct and
        # stay 1 forever because the recurrence never touches j == 0 or
        # j == len - 1.
        row = [1] * (rowIndex + 1)

        # Morph the current list into row i, starting at i = 2 (rows 0
        # and 1 are all 1s anyway).
        for i in range(2, rowIndex + 1):
            # Right-to-left: each slot consumes its untouched neighbors.
            for j in range(i - 1, 0, -1):
                row[j] += row[j - 1]

        return row


class MultiplicativeSolution:
    """Closed-form row generator — O(rowIndex^2) time, O(rowIndex) space.

    Row n is the binomial coefficients C(n, 0..n). Instead of adding
    Pascal's two parents, use the multiplicative identity

        C(n, j) = C(n, j - 1) * (n - j + 1) // j

    which follows from C(n, j) = n! / (j! (n-j)!). Integer division is
    exact at every step (each prefix is itself a binomial coefficient),
    so there are no rounding surprises.

    Bonus: rows are palindromes (C(n, j) == C(n, n - j)), so we only
    compute the left half and mirror it.

    Time complexity:  O(rowIndex^2) — but with a tiny constant: one
                      multiply, one add-free divide per entry.
    Space complexity: O(rowIndex) — the output row itself.
    """

    def getRow(self, rowIndex):
        n = rowIndex
        row = [1] * (n + 1)

        # Fill the left half (including the middle for odd lengths).
        for j in range(1, n // 2 + 1):
            row[j] = row[j - 1] * (n - j + 1) // j

        # Mirror it: row[j] == row[n - j] by symmetry.
        for j in range((n + 1) // 2, n):
            row[j] = row[n - j]

        return row


# --- Tests ---


class TestPascalsTriangleII(unittest.TestCase):
    def setUp(self):
        self.solutions = [InPlaceDPSolution(), MultiplicativeSolution()]

    def test_example_1(self):
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.getRow(3), [1, 3, 3, 1])

    def test_example_2_row_zero(self):
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.getRow(0), [1])

    def test_example_3_row_one(self):
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.getRow(1), [1, 1])

    def test_row_2(self):
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.getRow(2), [1, 2, 1])

    def test_known_row_4(self):
        self.assertEqual(
            InPlaceDPSolution().getRow(4), [1, 4, 6, 4, 1]
        )

    def test_known_row_5(self):
        self.assertEqual(
            InPlaceDPSolution().getRow(5), [1, 5, 10, 10, 5, 1]
        )

    def test_every_row_is_palindrome(self):
        # C(n, j) == C(n, n - j): every row reads the same both ways.
        for sol in self.solutions:
            for n in range(34):
                with self.subTest(sol=type(sol).__name__, rowIndex=n):
                    row = sol.getRow(n)
                    self.assertEqual(row, row[::-1])

    def test_binomial_coefficients(self):
        # Verify every entry against the exact multiplicative recurrence
        # C(n, j) = C(n, j - 1) * (n - j + 1) // j.
        for n in range(34):
            expected = [1] * (n + 1)
            for j in range(1, n + 1):
                expected[j] = expected[j - 1] * (n - j + 1) // j
            for sol in self.solutions:
                with self.subTest(sol=type(sol).__name__, rowIndex=n):
                    self.assertEqual(sol.getRow(n), expected)

    def test_consecutive_rows_follow_pascal_recurrence(self):
        # row n and row n + 1 must satisfy row_{n+1}[j] =
        # row_n[j - 1] + row_n[j] for interior entries.
        sol = InPlaceDPSolution()
        for n in range(1, 33):
            prev, nxt = sol.getRow(n), sol.getRow(n + 1)
            for j in range(1, n + 1):
                self.assertEqual(
                    nxt[j], prev[j - 1] + prev[j],
                    f"row {n + 1}, col {j} violates the Pascal recurrence",
                )

    def test_upper_constraint_row_33(self):
        # rowIndex = 33 is the stated maximum. Its middle entry is
        # C(33, 16) = 1166803110 — check it exactly.
        self.assertEqual(
            InPlaceDPSolution().getRow(33)[16], 1166803110
        )

    def test_space_optimized_outputs_are_flat_rows(self):
        # Guard against a regression that returns the whole triangle.
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(len(sol.getRow(10)), 11)


if __name__ == "__main__":
    unittest.main()
