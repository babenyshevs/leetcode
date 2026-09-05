"""
LeetCode #100 - Same Tree (Easy)

Given the roots of two binary trees p and q, write a function to check
if they are the same or not.

Two binary trees are considered the same if they are structurally
identical, and the nodes have the same value.

Example 1:
    Input: p = [1,2,3], q = [1,2,3]
    Output: true

Example 2:
    Input: p = [1,2], q = [1,null,2]
    Output: false

Example 3:
    Input: p = [1,2,1], q = [1,1,2]
    Output: false

Constraints:
    The number of nodes in both trees is in the range [0, 100].
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
    """Iterative same-tree check using two stacks (preorder DFS) — O(n) time, O(h) space.

    Key insight: walk both trees in lockstep with an explicit stack of
    node pairs. At each step the popped pair must either both be None
    (nothing to compare) or both be real nodes with equal values. Any
    mismatch — one side missing, or values differing — proves the trees
    are not the same. Children are pushed right-first so the left
    subtrees are compared before the right ones.

    Time complexity:  O(n) — each node of each tree is visited once.
    Space complexity: O(h) — stack holds at most one root-to-leaf path
                       pair, where h is the taller tree's height
                       (worst case O(n) for a skewed tree).
    """

    def isSameTree(self, p, q):
        stack = [(p, q)]

        while stack:
            a, b = stack.pop()

            if a is None and b is None:
                continue  # both sides empty — this branch matches
            if a is None or b is None:
                return False  # structural mismatch: only one side exists
            if a.val != b.val:
                return False  # same position, different values

            # Compare children in lockstep (right pushed first so left is processed first)
            stack.append((a.right, b.right))
            stack.append((a.left, b.left))

        return True


class SimpleSolution:
    """Recursive same-tree check — O(n) time, O(h) space.

    The straightforward recursive approach: two trees are the same iff
    their roots hold equal values (or are both empty) and their left
    subtrees are the same and their right subtrees are the same.
    """

    def isSameTree(self, p, q):
        if p is None and q is None:
            return True
        if p is None or q is None:
            return False
        return (
            p.val == q.val
            and self.isSameTree(p.left, q.left)
            and self.isSameTree(p.right, q.right)
        )


# --- Tests ---


class TestSameTree(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()
        self.simple = SimpleSolution()

    def _same(self, sol, p_values, q_values):
        return sol.isSameTree(build_tree(p_values), build_tree(q_values))

    def test_example_1_identical(self):
        self.assertTrue(self._same(self.sol, [1, 2, 3], [1, 2, 3]))

    def test_example_2_structure_differs(self):
        # [1,2] vs [1,null,2]: 2 is a left child in p, right child in q
        self.assertFalse(self._same(self.sol, [1, 2], [1, None, 2]))

    def test_example_3_values_differ(self):
        self.assertFalse(self._same(self.sol, [1, 2, 1], [1, 1, 2]))

    def test_both_empty(self):
        self.assertTrue(self._same(self.sol, [], []))

    def test_one_empty(self):
        self.assertFalse(self._same(self.sol, [], [1]))
        self.assertFalse(self._same(self.sol, [1], []))

    def test_single_node_match(self):
        self.assertTrue(self._same(self.sol, [1], [1]))

    def test_single_node_mismatch(self):
        self.assertFalse(self._same(self.sol, [1], [2]))

    def test_negative_values(self):
        #       -10                    -10
        #       /  \                   /  \
        #    -20    3               -20    3
        #      \                       \
        #       4                       4
        self.assertTrue(self._same(self.sol, [-10, -20, 3, None, 4], [-10, -20, 3, None, 4]))
        # Swap 3 and 4's parents so structures diverge
        self.assertFalse(self._same(self.sol, [-10, -20, 3, None, 4], [-10, 3, -20, None, 4]))

    def test_deep_left_skewed(self):
        # Two identical left chains of length 5
        chain = [1, 2, None, 3, None, 4, None, 5]
        self.assertTrue(self._same(self.sol, chain, chain))
        # Same chain but last value differs
        other = [1, 2, None, 3, None, 4, None, 9]
        self.assertFalse(self._same(self.sol, chain, other))

    def test_iterative_matches_recursive(self):
        """Verify both solutions produce the same result on all cases."""
        cases = [
            ([1, 2, 3], [1, 2, 3]),
            ([1, 2], [1, None, 2]),
            ([1, 2, 1], [1, 1, 2]),
            ([], []),
            ([], [1]),
            ([1], []),
            ([1], [1]),
            ([1], [2]),
            ([-10, -20, 3, None, 4], [-10, -20, 3, None, 4]),
            ([-10, -20, 3, None, 4], [-10, 3, -20, None, 4]),
            ([1, 2, None, 3, None, 4, None, 5], [1, 2, None, 3, None, 4, None, 5]),
            ([1, 2, None, 3, None, 4, None, 5], [1, 2, None, 3, None, 4, None, 9]),
        ]
        for p_vals, q_vals in cases:
            self.assertEqual(
                self._same(self.sol, p_vals, q_vals),
                self._same(self.simple, p_vals, q_vals),
                f"Mismatch between solutions for {p_vals} vs {q_vals}",
            )


if __name__ == "__main__":
    unittest.main()
