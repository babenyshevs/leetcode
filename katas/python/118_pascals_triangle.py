"""
LeetCode #118 - Pascal's Triangle (Easy)

Given an integer numRows, return the first numRows of Pascal's triangle.

In Pascal's triangle, each number is the sum of the two numbers directly
above it. Row i (0-indexed) has i + 1 entries; the first and last entry
of every row is 1.

Example 1:
    Input: numRows = 5
    Output: [[1],[1,1],[1,2,1],[1,3,3,1],[1,4,6,4,1]]

Example 2:
    Input: numRows = 1
    Output: [[1]]

Constraints:
    1 <= numRows <= 30

Follow-up: could you optimize your algorithm to use only O(k) extra
space? (See the second solution and the bonus row generator below.)
"""

import unittest


class Solution:
    """Build the triangle row by row — O(numRows^2) time, O(numRows^2) space
    for the output (which is required, so auxiliary space is O(1)).

    Each row starts and ends with 1. Every interior entry of row i is
    row[i - 1][j - 1] + row[i - 1][j]: the two numbers directly above it
    in the previous row. That is the whole recurrence — no factorials,
    no binomial coefficients needed.

    Time complexity:  O(numRows^2) — row i costs O(i) work, summed.
    Space complexity: O(numRows^2) — the returned triangle itself.
    """

    def generate(self, numRows):
        triangle = []

        for i in range(numRows):
            # Every row begins with 1...
            row = [1] * (i + 1)
            # ...and interior slots are the sum of the two parents above.
            for j in range(1, i):
                row[j] = triangle[i - 1][j - 1] + triangle[i - 1][j]
            triangle.append(row)

        return triangle


class SpaceOptimizedSolution:
    """Follow-up answer: generate only the final row with O(numRows) space.

    Updating a single row IN PLACE from right to left is the classic 1-D
    DP trick (same idea as LC #119, Pascal's Triangle II). Scanning right
    to left matters: row[j] += row[j - 1] reads row[j - 1] before it is
    updated, so each slot still sees its "previous row" value. A left to
    right pass would clobber row[j - 1] first and compute garbage.
    """

    def generate_last_row(self, numRows):
        row = [1] * numRows
        for i in range(2, numRows):
            for j in range(i - 1, 0, -1):
                row[j] += row[j - 1]
        return row


# --- Tests ---


class TestPascalsTriangle(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()
        self.opt = SpaceOptimizedSolution()

    def test_example_1(self):
        self.assertEqual(
            self.sol.generate(5),
            [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]],
        )

    def test_example_2_single_row(self):
        self.assertEqual(self.sol.generate(1), [[1]])

    def test_two_rows(self):
        self.assertEqual(self.sol.generate(2), [[1], [1, 1]])

    def test_row_shape(self):
        # Row i (0-indexed) has exactly i + 1 entries.
        triangle = self.sol.generate(10)
        self.assertEqual([len(row) for row in triangle], list(range(1, 11)))

    def test_known_row_values(self):
        # Spot-check a deeper row: row 6 of the triangle.
        self.assertEqual(
            self.sol.generate(7)[6], [1, 6, 15, 20, 15, 6, 1]
        )

    def test_symmetry_of_every_row(self):
        # Pascal's rows are palindromes: row[j] == row[-1 - j].
        triangle = self.sol.generate(15)
        for row in triangle:
            self.assertEqual(row, row[::-1])

    def test_binomial_coefficients(self):
        # Entry j of row n equals C(n, j). Verify via the multiplicative
        # recurrence C(n, j) = C(n, j - 1) * (n - j + 1) // j.
        triangle = self.sol.generate(20)
        for n, row in enumerate(triangle):
            expected = [1] * (n + 1)
            for j in range(1, n + 1):
                expected[j] = expected[j - 1] * (n - j + 1) // j
            self.assertEqual(row, expected)

    def test_interior_sums_of_parents(self):
        # Each interior entry is the sum of the two entries above it.
        triangle = self.sol.generate(12)
        for i in range(2, len(triangle)):
            for j in range(1, i):
                self.assertEqual(
                    triangle[i][j],
                    triangle[i - 1][j - 1] + triangle[i - 1][j],
                    f"row {i}, col {j} violates the Pascal recurrence",
                )

    def test_large_numrows_runs(self):
        # Upper constraint: numRows = 30. Row 29's middle entry is
        # C(29, 14) = 77558760 — big but well within int range.
        triangle = self.sol.generate(30)
        self.assertEqual(len(triangle), 30)
        self.assertEqual(triangle[29][14], 77558760)

    def test_space_optimized_matches_full_triangle(self):
        # The O(k) last-row generator must agree with the full triangle.
        for n in range(1, 25):
            with self.subTest(numRows=n):
                self.assertEqual(
                    self.opt.generate_last_row(n), self.sol.generate(n)[-1]
                )


if __name__ == "__main__":
    unittest.main()
