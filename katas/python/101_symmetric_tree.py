"""
LeetCode #101 - Symmetric Tree (Easy)

Given the root of a binary tree, check whether it is a mirror of
itself (i.e., symmetric around its center).

Example 1:
    Input: root = [1,2,2,3,4,4,3]
    Output: true

Example 2:
    Input: root = [1,2,2,null,3,null,3]
    Output: false

Constraints:
    The number of nodes in the tree is in the range [1, 1000].
    -100 <= Node.val <= 100

Follow up: Could you solve it both recursively and iteratively?
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
    """Iterative symmetry check using a stack of mirror pairs — O(n) time, O(h) space.

    Key insight: a tree is symmetric iff the left subtree is a mirror
    of the right subtree. Two subtrees are mirrors when their roots
    hold equal values and the left child of one is the mirror of the
    right child of the other (and vice versa). We walk the tree with
    an explicit stack of node pairs that must mirror each other:
    (t.left, t.right) to start, then (a.left, b.right) and
    (a.right, b.left) for each matched pair. Any mismatch — one side
    missing, or values differing — proves the tree is not symmetric.

    Time complexity:  O(n) — each node is visited once.
    Space complexity: O(h) — stack holds at most one root-to-leaf
                       level of mirror pairs, where h is the tree
                       height (worst case O(n) for a skewed tree).
    """

    def isSymmetric(self, root):
        if root is None:
            return True

        stack = [(root.left, root.right)]

        while stack:
            a, b = stack.pop()

            if a is None and b is None:
                continue  # both sides empty — this branch matches
            if a is None or b is None:
                return False  # mirror mismatch: only one side exists
            if a.val != b.val:
                return False  # mirrored positions, different values

            # Cross-compare: outer pair and inner pair
            stack.append((a.left, b.right))
            stack.append((a.right, b.left))

        return True


class SimpleSolution:
    """Recursive symmetry check — O(n) time, O(h) space.

    The straightforward recursive approach: a tree is symmetric iff
    its left subtree mirrors its right subtree. Two subtrees mirror
    each other when both are empty, or their roots hold equal values
    and the outer pair (a.left vs b.right) and inner pair
    (a.right vs b.left) mirror each other too.
    """

    def isSymmetric(self, root):
        def is_mirror(a, b):
            if a is None and b is None:
                return True
            if a is None or b is None:
                return False
            return (
                a.val == b.val
                and is_mirror(a.left, b.right)
                and is_mirror(a.right, b.left)
            )

        if root is None:
            return True
        return is_mirror(root.left, root.right)


# --- Tests ---


class TestSymmetricTree(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()
        self.simple = SimpleSolution()

    def _sym(self, sol, values):
        return sol.isSymmetric(build_tree(values))

    def test_example_1_symmetric(self):
        #         1
        #        / \
        #       2   2
        #      / \ / \
        #     3  4 4  3
        self.assertTrue(self._sym(self.sol, [1, 2, 2, 3, 4, 4, 3]))

    def test_example_2_not_symmetric(self):
        #     1
        #    / \
        #   2   2
        #    \    \
        #     3    3
        self.assertFalse(self._sym(self.sol, [1, 2, 2, None, 3, None, 3]))

    def test_single_node(self):
        self.assertTrue(self._sym(self.sol, [1]))

    def test_two_nodes_equal(self):
        # Two roots only: [1, 2] means node 2 is a LEFT child only -> asymmetric
        self.assertFalse(self._sym(self.sol, [1, 2]))

    def test_two_level_values_differ(self):
        #       1
        #      / \
        #     2   3
        self.assertFalse(self._sym(self.sol, [1, 2, 3]))

    def test_negative_values(self):
        #        -10
        #        /  \
        #     -20    -20
        #       \    /
        #        4  4
        self.assertTrue(self._sym(self.sol, [-10, -20, -20, None, 4, 4]))

    def test_asymmetric_deep(self):
        #       1
        #      / \
        #     2   2
        #    /     \
        #   3       3   <- symmetric (outer mirrors)
        # vs 3   None  <- not symmetric
        self.assertTrue(self._sym(self.sol, [1, 2, 2, 3, None, None, 3]))
        self.assertFalse(self._sym(self.sol, [1, 2, 2, None, 3, None, 3]))

    def test_inner_vs_outer_asymmetry(self):
        #       1
        #      / \
        #     2   2
        #      \   \
        #       3   3
        # Both 3s are right children -> mirrored positions are
        # (2.left=None vs 2.right=3) -> asymmetric
        self.assertFalse(self._sym(self.sol, [1, 2, 2, None, 3, None, 3]))
        # Mirror image: both 3s placed so pairs cross correctly
        self.assertTrue(self._sym(self.sol, [1, 2, 2, None, 3, 3]))

    def test_iterative_matches_recursive(self):
        """Verify both solutions produce the same result on all cases."""
        cases = [
            [1, 2, 2, 3, 4, 4, 3],
            [1, 2, 2, None, 3, None, 3],
            [1],
            [],
            [1, 2],
            [1, 2, 3],
            [-10, -20, -20, None, 4, 4],
            [1, 2, 2, 3, None, None, 3],
            [1, 2, 2, None, 3, 3],
            [1, 2, 2, 2, None, 2],
            [1, 2, 2, 3, 4, 4, 3, 5, 6, 6, 5],
        ]
        for values in cases:
            self.assertEqual(
                self._sym(self.sol, values),
                self._sym(self.simple, values),
                f"Mismatch between solutions for {values}",
            )


if __name__ == "__main__":
    unittest.main()
