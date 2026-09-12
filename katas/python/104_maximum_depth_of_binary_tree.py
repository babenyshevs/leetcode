"""
LeetCode #104 - Maximum Depth of Binary Tree (Easy)

Given the root of a binary tree, return its maximum depth.

A binary tree's maximum depth is the number of nodes along the
longest path from the root node down to the farthest leaf node.

Example 1:
    Input: root = [3,9,20,null,null,15,7]
    Output: 3

Example 2:
    Input: root = [1,null,2]
    Output: 2

Constraints:
    The number of nodes in the tree is in the range [0, 10^4].
    -100 <= Node.val <= 100
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
    """Iterative BFS level count — O(n) time, O(w) space.

    Key insight: the maximum depth equals the number of levels the
    tree has. Breadth-first search naturally visits the tree one
    level at a time, so we keep a queue of the current level's nodes
    and increment a depth counter once per level until the queue
    drains. An empty tree yields depth 0.

    Time complexity:  O(n) — every node enters the queue exactly once.
    Space complexity: O(w) — the queue holds at most one level of
                       nodes, where w is the maximum width (worst case
                       O(n) for a perfectly balanced tree).
    """

    def maxDepth(self, root):
        if root is None:
            return 0

        depth = 0
        queue = [root]

        while queue:
            depth += 1  # entering one more level
            # Dequeue this whole level, enqueue the next one.
            next_level = []
            for node in queue:
                if node.left:
                    next_level.append(node.left)
                if node.right:
                    next_level.append(node.right)
            queue = next_level

        return depth


class SimpleSolution:
    """Recursive depth-first height computation — O(n) time, O(h) space.

    The straightforward approach: the depth of a tree rooted at a node
    is 1 plus the larger of the depths of its two subtrees. The depth
    of an empty subtree is 0, so a lone leaf gets depth 1 and an empty
    tree gets depth 0.
    """

    def maxDepth(self, root):
        if root is None:
            return 0
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))


# --- Tests ---


class TestMaximumDepth(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()
        self.simple = SimpleSolution()

    def _depth(self, sol, values):
        return sol.maxDepth(build_tree(values))

    def test_example_1(self):
        #        3
        #       / \
        #      9  20
        #        /  \
        #       15   7
        self.assertEqual(self._depth(self.sol, [3, 9, 20, None, None, 15, 7]), 3)

    def test_example_2(self):
        #     1
        #      \
        #       2
        self.assertEqual(self._depth(self.sol, [1, None, 2]), 2)

    def test_empty_tree(self):
        self.assertEqual(self._depth(self.sol, []), 0)

    def test_single_node(self):
        self.assertEqual(self._depth(self.sol, [0]), 1)

    def test_two_nodes_left_child(self):
        self.assertEqual(self._depth(self.sol, [1, 2]), 2)

    def test_left_skewed_chain(self):
        #   1 -> 2 -> 3 -> 4 all down the left
        self.assertEqual(self._depth(self.sol, [1, 2, None, 3, None, 4]), 4)

    def test_full_binary_tree(self):
        #           1
        #         /   \
        #        2     3
        #       / \   / \
        #      4   5 6   7
        self.assertEqual(self._depth(self.sol, [1, 2, 3, 4, 5, 6, 7]), 3)

    def test_unbalanced_deep_right(self):
        #     1
        #    / \
        #   2   3
        #        \
        #         4
        #          \
        #           5
        self.assertEqual(self._depth(self.sol, [1, 2, 3, None, None, None, 4, None, 5]), 4)

    def test_negative_values(self):
        self.assertEqual(self._depth(self.sol, [-10, -20, -30, None, None, -40]), 3)

    def test_bfs_matches_recursive(self):
        """Verify both solutions produce the same depth on all cases."""
        cases = [
            [3, 9, 20, None, None, 15, 7],
            [1, None, 2],
            [],
            [0],
            [1, 2],
            [1, 2, None, 3, None, 4],
            [1, 2, 3, 4, 5, 6, 7],
            [1, 2, 3, None, None, None, 4, None, 5],
            [-10, -20, -30, None, None, -40],
        ]
        for values in cases:
            self.assertEqual(
                self._depth(self.sol, values),
                self._depth(self.simple, values),
                f"Mismatch between solutions for {values}",
            )


if __name__ == "__main__":
    unittest.main()
