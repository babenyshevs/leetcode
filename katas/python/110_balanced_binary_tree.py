"""
LeetCode #110 - Balanced Binary Tree (Easy)

Given a binary tree, determine if it is height-balanced.

A height-balanced binary tree is a binary tree in which the depth
of the two subtrees of every node never differs by more than one.

Example 1:
    Input: root = [3,9,20,null,null,15,7]
    Output: true

        3
       / \
      9  20
        /  \
       15   7

Example 2:
    Input: root = [1,2,2,3,3,null,null,4,4]
    Output: false

            1
           / \
          2   2
         / \
        3   3
       / \
      4   4

Example 3:
    Input: root = []
    Output: true

Constraints:
    The number of nodes in the tree is in the range [0, 5000].
    -10^4 <= Node.val <= 10^4
"""

import unittest


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
    """Bottom-up DFS: check balance while computing heights — O(n) time.

    Key insight: a naive top-down check (is_balanced(node) =
    balanced(node.left) and balanced(node.right) and |h(l) - h(r)| <= 1)
    recomputes subtree heights at every level, costing O(n^2) in the
    worst case. Instead we compute heights bottom-up in a single
    post-order pass: each recursive call returns the subtree's height,
    or -1 as a sentinel meaning "already unbalanced". The sentinel
    short-circuits, so every node is visited exactly once and an
    unbalanced subtree never gets re-inspected.

    An empty tree (no nodes) is considered balanced, per the examples.

    Time complexity:  O(n) — each node is visited exactly once.
    Space complexity: O(h) — recursion stack, h = tree height
                       (O(n) worst case for a skewed tree).
    """

    def isBalanced(self, root):
        return self._check(root) != -1

    def _check(self, node):
        """Return the node's height, or -1 if the subtree is unbalanced."""
        if node is None:
            return 0

        left = self._check(node.left)
        if left == -1:  # left subtree already unbalanced, bail out early
            return -1

        right = self._check(node.right)
        if right == -1:  # right subtree already unbalanced
            return -1

        if abs(left - right) > 1:
            return -1  # this node violates the balance condition

        return 1 + max(left, right)


class SimpleSolution:
    """Straightforward top-down check — O(n^2) time, O(h) space.

    The most readable formulation of the definition itself: a tree is
    balanced when all three of these hold:
      1. the left subtree is balanced,
      2. the right subtree is balanced,
      3. the two subtree heights differ by at most one.
    Heights are recomputed with a full traversal at every node, which
    duplicates work but mirrors the problem statement one-to-one. Fine
    for the given constraints (n <= 5000); the O(n) Solution above is
    the optimized version.
    """

    def isBalanced(self, root):
        if root is None:
            return True
        return (
            abs(self._height(root.left) - self._height(root.right)) <= 1
            and self.isBalanced(root.left)
            and self.isBalanced(root.right)
        )

    def _height(self, node):
        if node is None:
            return 0
        return 1 + max(self._height(node.left), self._height(node.right))


# --- Tests ---


class TestBalancedBinaryTree(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()
        self.simple = SimpleSolution()

    def _is_balanced(self, sol, values):
        return sol.isBalanced(build_tree(values))

    def test_example_1_balanced(self):
        #        3
        #       / \
        #      9  20
        #        /  \
        #       15   7
        self.assertTrue(self._is_balanced(self.sol, [3, 9, 20, None, None, 15, 7]))

    def test_example_2_unbalanced_at_leaf_level(self):
        # Imbalance appears between node 3's children (heights 1 vs 0)
        # and propagates all the way up to the root.
        self.assertFalse(
            self._is_balanced(self.sol, [1, 2, 2, 3, 3, None, None, 4, 4])
        )

    def test_example_3_empty_tree(self):
        self.assertTrue(self._is_balanced(self.sol, []))

    def test_single_node(self):
        self.assertTrue(self._is_balanced(self.sol, [1]))

    def test_two_nodes_left_child(self):
        self.assertTrue(self._is_balanced(self.sol, [1, 2]))

    def test_left_skewed_chain_unbalanced(self):
        #   1 -> 2 -> 3 -> 4 all down the left: node 2 has heights 2 vs 0.
        self.assertFalse(self._is_balanced(self.sol, [1, 2, None, 3, None, 4]))

    def test_right_skewed_chain_unbalanced(self):
        self.assertFalse(self._is_balanced(self.sol, [1, None, 2, None, 3]))

    def test_full_perfect_tree_balanced(self):
        #           1
        #         /   \
        #        2     3
        #       / \   / \
        #      4   5 6   7
        self.assertTrue(self._is_balanced(self.sol, [1, 2, 3, 4, 5, 6, 7]))

    def test_subtree_imbalance_deep_inside(self):
        #        1
        #       / \
        #      2   3
        #     / \
        #    4   5
        #   / \
        #  6   7     <- left branch is 3 deep, right subtree is 1 deep
        self.assertFalse(
            self._is_balanced(self.sol, [1, 2, 3, 4, 5, None, None, 6, 7])
        )

    def test_height_difference_of_two_at_root_unbalanced(self):
        #       1
        #      / \
        #     2   3
        #    / \
        #   4   5
        #  /
        # 6            <- left subtree height 3, right height 1: diff 2
        self.assertFalse(self._is_balanced(self.sol, [1, 2, 3, 4, 5, None, None, 6]))

    def test_height_difference_of_exactly_one_is_balanced(self):
        #       1
        #      / \
        #     2   3
        #    / \
        #   4   5      <- left subtree height 2, right height 1: diff 1
        self.assertTrue(self._is_balanced(self.sol, [1, 2, 3, 4, 5]))

    def test_sibling_heights_differ_by_one_only(self):
        #     1
        #    / \
        #   2   3
        #  /     \
        # 4       5   <- both leaves at depth 2, perfectly balanced
        self.assertTrue(self._is_balanced(self.sol, [1, 2, 3, 4, None, None, 5]))

    def test_negative_values(self):
        self.assertTrue(self._is_balanced(self.sol, [-1, -2, -3, -4, -5]))

    def test_all_values_equal(self):
        self.assertTrue(self._is_balanced(self.sol, [7, 7, 7, 7, 7, 7, 7]))

    def test_solution_matches_simple_solution(self):
        """Both solutions agree on every case, balanced or not."""
        cases = [
            [3, 9, 20, None, None, 15, 7],
            [1, 2, 2, 3, 3, None, None, 4, 4],
            [],
            [1],
            [1, 2],
            [1, 2, None, 3, None, 4],
            [1, None, 2, None, 3],
            [1, 2, 3, 4, 5, 6, 7],
            [1, 2, 3, 4, 5, None, None, 6, 7],
            [1, 2, 3, 4, 5],
            [1, 2, 3, 4, None, None, 5],
            [-1, -2, -3, -4, -5],
            [7, 7, 7, 7, 7, 7, 7],
        ]
        for values in cases:
            expected = self.simple.isBalanced(build_tree(values))
            self.assertEqual(
                self._is_balanced(self.sol, values),
                expected,
                f"Solutions disagree for {values}",
            )


if __name__ == "__main__":
    unittest.main()
