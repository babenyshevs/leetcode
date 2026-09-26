"""
LeetCode #112 - Path Sum (Easy)

Given the root of a binary tree and an integer targetSum, return true
if the tree has a root-to-leaf path such that adding up all the values
along the path equals targetSum.

A leaf is a node with no children.

Example 1:
    Input: root = [5,4,8,11,null,13,4,7,2,null,null,null,1], targetSum = 22
    Output: true

        5
       / \\
      4   8
     /   / \\
    11  13  4
   /  \\    / \\
  7    2  1   1
    (path 5 -> 4 -> 11 -> 2 sums to 22)

Example 2:
    Input: root = [1,2,3], targetSum = 5
    Output: false
    (paths 1->2 = 3 and 1->3 = 4; neither hits 5)

Example 3:
    Input: root = [], targetSum = 0
    Output: false
    (an empty tree has no root-to-leaf paths at all — even for 0)

Constraints:
    The number of nodes in the tree is in the range [0, 5000].
    -1000 <= Node.val <= 1000
    -1000 <= targetSum <= 1000
"""

import unittest
from collections import deque


class TreeNode:
    """Definition for a binary tree node."""

    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(values):
    """Build a binary tree from a level-order list representation.

    None values represent absent nodes. Returns None for an empty list.
    """
    if not values:
        return None

    root = TreeNode(values[0])
    queue = [root]
    i = 1

    while queue and i < len(values):
        node = queue.pop(0)
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1

    return root


class Solution:
    """Recursive DFS carrying the remaining sum — O(n) time, O(h) space.

    Subtract each node's value from targetSum on the way down. A node is
    a match iff it is a LEAF and its value equals the remaining target.
    Checking "remaining == 0" early at internal nodes would be WRONG:
    a partial sum of 0 mid-path says nothing about the final leaf sum.

    Negative values are perfectly legal (values go down to -1000), so
    pruning the moment the remaining sum drops below zero is also wrong —
    the sum can dip and climb back to the target later. Only the leaf
    check can decide.

    Time complexity:  O(n) — each node visited once.
    Space complexity: O(h) recursion stack, h = tree height
                      (O(n) worst case for a skewed tree).
    """

    def hasPathSum(self, root, targetSum):
        # Empty tree: no root-to-leaf paths exist, so no sum is possible.
        if root is None:
            return False

        remaining = targetSum - root.val

        # Leaf: the path must end here — does it hit the target exactly?
        if root.left is None and root.right is None:
            return remaining == 0

        # Internal node: the path must continue through an existing child.
        return self.hasPathSum(root.left, remaining) or self.hasPathSum(
            root.right, remaining
        )


class IterativeSolution:
    """DFS with an explicit stack of (node, remaining) pairs — O(n)/O(h).

    Same logic as the recursion, but without the call stack, which keeps
    it safe on deeply skewed trees. BFS over (node, remaining) pairs
    works identically; the stack version is the classic iterative DFS.
    """

    def hasPathSum(self, root, targetSum):
        if root is None:
            return False

        stack = [(root, targetSum)]

        while stack:
            node, remaining = stack.pop()
            remaining -= node.val

            # Leaf check — the only place a verdict can be issued.
            if node.left is None and node.right is None:
                if remaining == 0:
                    return True
                continue  # dead end, keep searching

            if node.left is not None:
                stack.append((node.left, remaining))
            if node.right is not None:
                stack.append((node.right, remaining))

        return False


# --- Tests ---


class TestPathSum(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()
        self.iter = IterativeSolution()

    def _has_path(self, sol, values, target):
        return sol.hasPathSum(build_tree(values), target)

    def test_example_1_true(self):
        #          5
        #         / \\
        #        4   8
        #       /   / \\
        #      11  13   4
        #     /  \\     / \\
        #    7    2   1    1
        # 5+4+11+2 = 22
        self.assertTrue(
            self._has_path(
                self.sol, [5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1], 22
            )
        )

    def test_example_2_false(self):
        #    1
        #   / \\
        #  2   3     sums 3 and 4, not 5
        self.assertFalse(self._has_path(self.sol, [1, 2, 3], 5))

    def test_example_3_empty_tree(self):
        # The empty tree has NO root-to-leaf paths — even target 0 is false.
        self.assertFalse(self._has_path(self.sol, [], 0))

    def test_single_node_hit(self):
        self.assertTrue(self._has_path(self.sol, [5], 5))

    def test_single_node_miss(self):
        self.assertFalse(self._has_path(self.sol, [5], 0))
        self.assertFalse(self._has_path(self.sol, [5], 10))

    def test_root_only_is_leaf_not_internal(self):
        # [1,2] with target 1: root 1 has a child, so it is NOT a leaf.
        # The only path is 1->2 = 2. A naive "remaining == 0 at any node"
        # check would wrongly return True.
        self.assertFalse(self._has_path(self.sol, [1, 2], 1))
        self.assertTrue(self._has_path(self.sol, [1, 2], 3))

    def test_target_zero_with_zero_valued_leaf(self):
        #   0
        #  /
        # 0          path 0->0 = 0
        self.assertTrue(self._has_path(self.sol, [0, 0], 0))

    def test_negative_values_reach_target(self):
        #     -1
        #    /  \\
        #  -2    -3
        #  /
        # -4          path -1 -> -2 -> -4 = -7
        self.assertTrue(self._has_path(self.sol, [-1, -2, -3, -4], -7))
        self.assertFalse(self._has_path(self.sol, [-1, -2, -3, -4], -6))

    def test_negative_dip_then_climb(self):
        #      1
        #     / \\
        #   -2   3
        #   /
        #  4             path 1 -> -2 -> 4 = 3
        # The running sum dips to -1 mid-path; pruning on "sum < target"
        # would lose the branch that climbs back to 3.
        self.assertTrue(self._has_path(self.sol, [1, -2, 3, 4], 3))

    def test_left_only_chain(self):
        # 1 -> 2 -> 3 down the left: sums 3, 6.
        self.assertTrue(self._has_path(self.sol, [1, 2], 3))
        self.assertFalse(self._has_path(self.sol, [1, 2, None, 3], 3))
        self.assertTrue(self._has_path(self.sol, [1, 2, None, 3], 6))

    def test_right_branch_carries_the_sum(self):
        #      1
        #     / \\
        #    2   3
        #       / \\
        #      4   5     path 1 -> 3 -> 5 = 9
        self.assertTrue(self._has_path(self.sol, [1, 2, 3, None, None, 4, 5], 9))
        self.assertFalse(self._has_path(self.sol, [1, 2, 3, None, None, 4, 5], 7))

    def test_same_total_on_different_paths(self):
        #      1
        #     / \\
        #    2   2          both paths sum to 3
        self.assertTrue(self._has_path(self.sol, [1, 2, 2], 3))
        self.assertFalse(self._has_path(self.sol, [1, 2, 2], 4))

    def test_iterative_solution_matches_recursive(self):
        """Both solutions agree on every case."""
        cases = [
            ([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1], 22),
            ([1, 2, 3], 5),
            ([], 0),
            ([5], 5),
            ([5], 0),
            ([1, 2], 1),
            ([1, 2], 3),
            ([0, 0], 0),
            ([-1, -2, -3, -4], -7),
            ([-1, -2, -3, -4], -6),
            ([1, -2, 3, 4], 3),
            ([1, 2], 3),
            ([1, 2, None, 3], 3),
            ([1, 2, None, 3], 6),
            ([1, 2, 3, None, None, 4, 5], 9),
            ([1, 2, 3, None, None, 4, 5], 7),
            ([1, 2, 2], 3),
            ([1, 2, 2], 4),
        ]
        for values, target in cases:
            with self.subTest(values=values, target=target):
                expected = self._has_path(self.iter, values, target)
                self.assertEqual(
                    self._has_path(self.sol, values, target),
                    expected,
                    f"Solutions disagree for {values}, target {target}",
                )


if __name__ == "__main__":
    unittest.main()
