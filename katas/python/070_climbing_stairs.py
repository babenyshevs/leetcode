"""
LeetCode #70 - Climbing Stairs (Easy)

You are climbing a staircase. It takes n steps to reach the top.
Each time you can either climb 1 or 2 steps. In how many distinct
ways can you climb to the top?

Example 1:
    Input: n = 2
    Output: 2
    Explanation: There are two ways to climb to the top.
                 1. 1 step + 1 step
                 2. 2 steps

Example 2:
    Input: n = 3
    Output: 3
    Explanation: There are three ways to climb to the top.
                 1. 1 step + 1 step + 1 step
                 2. 1 step + 2 steps
                 3. 2 steps + 1 step

Constraints:
    1 <= n <= 45
"""

import unittest


class Solution:
    """Dynamic programming (bottom-up) — O(n) time, O(1) space.

    Let dp[i] = number of distinct ways to reach step i.
    To reach step i, you could have come from step i-1 (1 step)
    or step i-2 (2 steps), so:
        dp[i] = dp[i-1] + dp[i-2]

    Base cases: dp[1] = 1, dp[2] = 2.

    This is the Fibonacci sequence shifted by one index.
    We only need the two previous values, so we use two variables
    instead of a full array to achieve O(1) space.
    """

    def climbStairs(self, n: int) -> int:
        if n <= 2:
            return n

        prev2, prev1 = 1, 2  # dp[1], dp[2]

        for _ in range(3, n + 1):
            current = prev1 + prev2
            prev2, prev1 = prev1, current

        return prev1


class MatrixSolution:
    """Matrix exponentiation — O(log n) time, O(1) space.

    The recurrence dp[i] = dp[i-1] + dp[i-2] can be expressed as
    a matrix multiplication:
        [dp[i]  ]   [1 1] ^ (i-1)   [dp[1]]
        [dp[i-1]] = [1 0]           [dp[0]]

    By exponentiating the 2x2 matrix using fast power, we compute
    the nth Fibonacci-like number in O(log n) time.

    This is overkill for n <= 45 but demonstrates an important
    technique for linear recurrences at scale.
    """

    def climbStairs(self, n: int) -> int:
        if n <= 2:
            return n

        def mat_mult(A, B):
            return [
                [A[0][0] * B[0][0] + A[0][1] * B[1][0],
                 A[0][0] * B[0][1] + A[0][1] * B[1][1]],
                [A[1][0] * B[0][0] + A[1][1] * B[1][0],
                 A[1][0] * B[0][1] + A[1][1] * B[1][1]],
            ]

        def mat_pow(M, power):
            # Start with identity matrix
            result = [[1, 0], [0, 1]]
            while power > 0:
                if power % 2 == 1:
                    result = mat_mult(result, M)
                M = mat_mult(M, M)
                power //= 2
            return result

        # [F(n+1), F(n)] = [[1,1],[1,0]]^n * [F(1), F(0)]
        # where F(0)=0, F(1)=1. Our dp[1]=1=F(2), dp[2]=2=F(3).
        # So dp[n] = F(n+1) = mat_pow(base, n)[0][0]
        base = [[1, 1], [1, 0]]
        result = mat_pow(base, n)
        return result[0][0]


class DPDictSolution:
    """Dynamic programming with dictionary — O(n) time, O(n) space.

    Same recurrence as Solution but stores all intermediate values
    in a dictionary. Useful for understanding the recurrence relation,
    though less space-efficient than the two-variable approach.
    """

    def climbStairs(self, n: int) -> int:
        dp = {1: 1, 2: 2}
        for i in range(3, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]
        return dp[n]


# --- Tests ---


class TestClimbingStairs(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()
        self.matrix = MatrixSolution()
        self.dp_dict = DPDictSolution()

    def test_example_1(self):
        self.assertEqual(self.sol.climbStairs(2), 2)

    def test_example_2(self):
        self.assertEqual(self.sol.climbStairs(3), 3)

    def test_n_equals_1(self):
        self.assertEqual(self.sol.climbStairs(1), 1)

    def test_n_equals_4(self):
        self.assertEqual(self.sol.climbStairs(4), 5)

    def test_n_equals_5(self):
        self.assertEqual(self.sol.climbStairs(5), 8)

    def test_fibonacci_values(self):
        # dp(n) follows Fibonacci: 1, 2, 3, 5, 8, 13, 21, 34, 55, 89
        expected = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
        for i, val in enumerate(expected, start=1):
            self.assertEqual(self.sol.climbStairs(i), val, f"Failed for n={i}")

    def test_n_equals_10(self):
        self.assertEqual(self.sol.climbStairs(10), 89)

    def test_max_constraint(self):
        # n=45: Fib(46) in 1-indexed = 1836311903
        self.assertEqual(self.sol.climbStairs(45), 1836311903)

    def test_matrix_matches_dp(self):
        for n in [1, 2, 3, 4, 5, 10, 20, 30, 45]:
            self.assertEqual(
                self.sol.climbStairs(n),
                self.matrix.climbStairs(n),
                f"Matrix solution mismatch for n={n}",
            )

    def test_dp_dict_matches_dp(self):
        for n in [1, 2, 3, 4, 5, 10, 20, 30, 45]:
            self.assertEqual(
                self.sol.climbStairs(n),
                self.dp_dict.climbStairs(n),
                f"DP dict solution mismatch for n={n}",
            )


if __name__ == "__main__":
    unittest.main()
