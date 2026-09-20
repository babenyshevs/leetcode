"""
LeetCode #111 - Minimum Depth of Binary Tree (Easy)

Given a binary tree, find its minimum depth.

The minimum depth is the number of nodes along the shortest path
from the root node down to the nearest leaf node.

A leaf node is a node with no children.

Example 1:
    Input: root = [3,9,20,null,null,15,7]
    Output: 2

        3
       / \\
      9  20
        /  \\
       15   7
    (shortest path is 3 -> 9)

Example 2:
    Input: root = [2,null,3,null,4,null,5,null,6]
    Output: 5

    2
     \\
      3
       \\
        4
         \\
          5
           \\
            6
    (the only leaf is 6, so the path must run through every node)

Constraints:
    The number of nodes in the tree is in the range [0, 10^5].
    -1000 <= Node.val <= 1000
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
    """DFS with the one-child subtlety handled — O(n) time, O(h) space.

    The naive "return 1 + min(depth(left), depth(right))" is WRONG when
    a node has exactly one child: min() would pick the empty side
    (depth 0) and report a "path to a leaf" that doesn't exist. A node
    with a single child is not a leaf, so the search is forced down the
    existing branch.

    Rules per node:
      - None           -> 0 (no path at all)
      - leaf           -> 1
      - one child only -> 1 + depth(existing child)
      - two children   -> 1 + min(depth(left), depth(right))

    Time complexity:  O(n) — each node visited once.
    Space complexity: O(h) recursion stack, h = tree height
                      (O(n) worst case for the skewed example above —
                      this is why it matters here, unlike balanced trees).
    """

    def minDepth(self, root):
        if root is None:
            return 0

        # Leaf node: path ends here.
        if root.left is None and root.right is None:
            return 1

        # Only one child: the shortest path is forced through it.
        if root.left is None:
            return 1 + self.minDepth(root.right)
        if root.right is None:
            return 1 + self.minDepth(root.left)

        # Both children exist: take the shallower branch.
        return 1 + min(self.minDepth(root.left), self.minDepth(root.right))


class BFSSolution:
    """Level-order traversal — O(n) time, O(w) space.

    BFS explores the tree level by level, so the FIRST leaf it meets
    sits on the shortest path — return its depth immediately without
    looking at any deeper nodes. For deep, lopsided trees this visits
    far fewer nodes than the full DFS (which must see every leaf before
    deciding). Best-fit algorithm for a "shortest depth" question.
    """

    def minDepth(self, root):
        if root is None:
            return 0

        depth = 1
        queue = deque([root])

        while queue:
            for _ in range(len(queue)):  # process one full level
                node = queue.popleft()
                if node.left is None and node.right is None:
                    return depth  # first leaf reached = minimum depth
                if node.left is not None:
                    queue.append(node.left)
                if node.right is not None:
                    queue.append(node.right)
            depth += 1

        return depth  # unreachable: a non-empty tree always has a leaf


# --- Tests ---


class TestMinimumDepthOfBinaryTree(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()
        self.bfs = BFSSolution()

    def _min_depth(self, sol, values):
        return sol.minDepth(build_tree(values))

    def test_example_1_short_side_wins(self):
        #        3
        #       / \\
        #      9  20
        #        /  \\
        #       15   7
        self.assertEqual(self._min_depth(self.sol, [3, 9, 20, None, None, 15, 7]), 2)

    def test_example_2_single_skewed_chain(self):
        # 2 -> 3 -> 4 -> 5 -> 6 all down the right: only leaf is 6.
        self.assertEqual(
            self._min_depth(self.sol, [2, None, 3, None, 4, None, 5, None, 6]), 5
        )

    def test_empty_tree(self):
        self.assertEqual(self._min_depth(self.sol, []), 0)

    def test_single_node_is_leaf(self):
        self.assertEqual(self._min_depth(self.sol, [1]), 1)

    def test_left_child_only(self):
        #     1
        #    /
        #   2          <- leaf 2, forced down the left branch
        self.assertEqual(self._min_depth(self.sol, [1, 2]), 2)

    def test_right_child_only(self):
        #     1
        #      \\
        #       2        <- leaf 2, forced down the right branch
        self.assertEqual(self._min_depth(self.sol, [1, None, 2]), 2)

    def test_one_child_forces_long_path(self):
        # Classic min() trap: naive answer would be 2 via the "empty" side.
        #       1
        #      / \\
        #     2   3
        #    /     \\
        #   4       5  <- leaves are 4 and 5, both at depth 3
        self.assertEqual(self._min_depth(self.sol, [1, 2, 3, 4, None, None, 5]), 3)

    def test_leaf_on_left_beats_deep_right(self):
        #       1
        #      / \
        #     2   3
        #    /     \
        #   4       5
        #     \
        #      6      <- leaf 5 (depth 3) beats leaf 6 (depth 4)
        self.assertEqual(
            self._min_depth(self.sol, [1, 2, 3, 4, None, None, 5, None, 6]), 3
        )

    def test_perfect_tree_depth_three(self):
        #           1
        #         /   \
        #        2     3
        #       / \   / \
        #      4   5 6   7
        # Even in a perfect tree the minimum depth counts NODES along
        # one root-to-leaf path: 1 -> 2 -> 4 = three nodes.
        self.assertEqual(self._min_depth(self.sol, [1, 2, 3, 4, 5, 6, 7]), 3)

    def test_negative_values(self):
        #     -1
        #    /
        #  -2
        #  /
        # -3        <- a single chain of three nodes, only leaf is -3
        self.assertEqual(self._min_depth(self.sol, [-1, -2, None, -3]), 3)

    def test_long_chain_left_skewed(self):
        # 1 -> 2 -> 3 -> 4 down the left: depth equals node count.
        self.assertEqual(self._min_depth(self.sol, [1, 2, None, 3, None, 4]), 4)

    def test_bfs_solution_matches_dfs(self):
        """Both solutions agree on every case."""
        cases = [
            [3, 9, 20, None, None, 15, 7],
            [2, None, 3, None, 4, None, 5, None, 6],
            [],
            [1],
            [1, 2],
            [1, None, 2],
            [1, 2, 3, 4, None, None, 5],
            [1, 2, 3, 4, None, None, 5, None, 6],
            [1, 2, 3, 4, 5, 6, 7],
            [-1, -2, None, -3],
            [1, 2, None, 3, None, 4],
        ]
        for values in cases:
            expected = self.bfs.minDepth(build_tree(values))
            self.assertEqual(
                self._min_depth(self.sol, values),
                expected,
                f"Solutions disagree for {values}",
            )


if __name__ == "__main__":
    unittest.main()
