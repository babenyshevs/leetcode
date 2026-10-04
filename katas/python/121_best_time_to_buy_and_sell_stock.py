"""
LeetCode #121 - Best Time to Buy and Sell Stock (Easy)

You are given an array prices where prices[i] is the price of a given
stock on the i-th day.

You want to maximize your profit by choosing a single day to buy one
stock and choosing a different day in the future to sell that stock.

Return the maximum profit you can achieve from this transaction.
If you cannot achieve any profit, return 0.

Example 1:
    Input: prices = [7,1,5,3,6,4]
    Output: 5
    Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6),
    profit = 6 - 1 = 5. Note that buying on day 2 and selling on day 1 is
    not allowed because you must buy before you sell.

Example 2:
    Input: prices = [7,6,4,3,1]
    Output: 0
    Explanation: In this case, no transactions are done and the max
    profit = 0.

Constraints:
    1 <= prices.length <= 10^5
    0 <= prices[i] <= 10^4
"""

import unittest


class OnePassSolution:
    """Track the running minimum price — O(n) time, O(1) space.

    The best trade selling on day i is always "buy at the cheapest day
    seen so far". So sweep left to right keeping two numbers:

      min_price  — lowest price among days 0..i-1 (strictly before i,
                   which enforces the "buy before sell" rule)
      best       — the largest (prices[i] - min_price) seen anywhere

    Because we compute the profit BEFORE folding day i into min_price,
    the sale day always comes after the purchase day. This is the
    equivalent of the Kadane transformation: the maximum of
    prices[j] - prices[i] (j > i) is the maximum subarray sum of the
    day-to-day deltas.

    Time complexity:  O(n) — one pass.
    Space complexity: O(1) — two scalars.
    """

    def maxProfit(self, prices):
        best = 0
        min_price = float("inf")
        for price in prices:
            # Profit if we sold today after buying at the cheapest
            # earlier day. Computed before updating min_price so the
            # buy day is strictly before the sell day.
            best = max(best, price - min_price)
            # Fold today's price in for future sell days.
            min_price = min(min_price, price)
        return best


class KadaneDeltaSolution:
    """Max-subarray on daily deltas — O(n) time, O(1) space.

    Profit = sell_price - buy_price. Write it as a telescoping sum of
    day-to-day changes: prices[j] - prices[i] =
    (prices[i+1]-prices[i]) + ... + (prices[j]-prices[j-1]).

    So the answer is the maximum subarray sum over the deltas
    (or 0 if every single-delta sum is negative — we simply never
    extend a running sum below zero, which mirrors "do no trade").

    Time complexity:  O(n) — one pass over the deltas.
    Space complexity: O(1) — two scalars.
    """

    def maxProfit(self, prices):
        best = 0          # best profit found; 0 == "no trade"
        running = 0       # max subarray sum of deltas ending today
        for i in range(1, len(prices)):
            delta = prices[i] - prices[i - 1]
            # Either extend the previous run or start fresh at today.
            running = max(delta, running + delta)
            # Never let a losing streak count as a transaction.
            best = max(best, running)
        return best


class BruteForceSolution:
    """Reference O(n^2) pair scan — for tests and sanity checks only.

    Tries every (buy, sell) pair with buy < sell. Far too slow for the
    full constraint (10^5 days -> ~5 * 10^9 pairs) but perfectly fine
    as an oracle on small random inputs.

    Time complexity:  O(n^2).
    Space complexity: O(1).
    """

    def maxProfit(self, prices):
        best = 0
        for i in range(len(prices)):
            for j in range(i + 1, len(prices)):
                best = max(best, prices[j] - prices[i])
        return best


# --- Tests ---


class TestBestTimeToBuyAndSellStock(unittest.TestCase):
    def setUp(self):
        self.solutions = [
            OnePassSolution(),
            KadaneDeltaSolution(),
        ]

    def test_example_1(self):
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.maxProfit([7, 1, 5, 3, 6, 4]), 5)

    def test_example_2_strictly_decreasing(self):
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.maxProfit([7, 6, 4, 3, 1]), 0)

    def test_single_day_no_sale_possible(self):
        # Only one day: you can buy but never sell in the future.
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.maxProfit([5]), 0)

    def test_two_days_profit(self):
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.maxProfit([1, 4]), 3)

    def test_two_days_loss(self):
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.maxProfit([4, 1]), 0)

    def test_equal_prices_zero_profit(self):
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.maxProfit([3, 3, 3, 3]), 0)

    def test_answer_is_not_global_max_minus_global_min(self):
        # A naive "max(prices) - min(prices)" shortcut returns 8 - 1 = 7
        # here, but the 8 comes BEFORE the 1, so that trade is illegal.
        # The true best is buy 5 sell 8 -> 3.
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.maxProfit([5, 8, 1, 3]), 3)

    def test_profit_at_the_end(self):
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.maxProfit([1, 2, 3, 4, 5]), 4)

    def test_multiple_valleys_pick_best(self):
        # Two dips: 1->5 gives 4, 3->8 gives 5. Expect the larger.
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.maxProfit([2, 5, 1, 3, 8]), 7)

    def test_constraint_bounds(self):
        # Minimum size (1 day) and maximum value (10^4) per constraints.
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.maxProfit([10000]), 0)
                self.assertEqual(sol.maxProfit([0, 10000]), 10000)

    def test_against_brute_force_on_random_inputs(self):
        # Oracle test: both O(n) solutions must agree with the O(n^2)
        # pair scan on many small random price series.
        import random

        rng = random.Random(121)  # fixed seed -> deterministic tests
        oracle = BruteForceSolution()
        for _ in range(200):
            n = rng.randint(1, 40)
            prices = [rng.randint(0, 10**4) for _ in range(n)]
            expected = oracle.maxProfit(prices)
            for sol in self.solutions:
                with self.subTest(sol=type(sol).__name__, prices=prices):
                    self.assertEqual(sol.maxProfit(prices), expected)


if __name__ == "__main__":
    unittest.main()
