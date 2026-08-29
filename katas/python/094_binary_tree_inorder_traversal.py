"""
LeetCode #94 - Binary Tree Inorder Traversal (Easy)

Given the root of a binary tree, return the inorder traversal of its nodes'
values.

Inorder traversal visits nodes in the order: left subtree → root → right subtree.

Example 1:
    Input: root = [1,null,2,3]
    Output: [1,3,2]
    Explanation:
        1
         \
          2
         /
        3
    Inorder: 1, then 3, then 2 → [1,3,2]

Example 2:
    Input: root = [1,2,3,4,5,null,8,null,null,6,7,9]
    Output: [4,2,6,5,7,1,3,9,8]

Example 3:
    Input: root = []
    Output: []

Example 4:
    Input: root = [1]
    Output: [1]

Constraints:
    The number of nodes in the tree is in the range [0, 100].
    -100 <= Node.val <= 100

Follow up: Recursive solution is trivial, could you do it iteratively?
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
    """Iterative inorder traversal using an explicit stack — O(n) time, O(h) space.

    Key insight: simulate the call stack that recursion would use.
    Start from the root and keep going left, pushing each node onto the stack.
    When we can't go further left, pop a node, record its value, then explore
    its right subtree (which may have its own left descendants).

    This is the follow-up solution to the "trivial" recursive approach.

    Time complexity:  O(n) — every node is pushed and popped exactly once.
    Space complexity: O(h) — stack holds at most h nodes, where h is the
                       tree height (worst case O(n) for a skewed tree).
    """

    def inorderTraversal(self, root):
        result = []
        stack = []
        current = root

        while current is not None or stack:
            # Go as far left as possible, pushing nodes along the way
            while current is not None:
                stack.append(current)
                current = current.left

            # No more left children — visit this node
            current = stack.pop()
            result.append(current.val)

            # Now explore the right subtree
            current = current.right

        return result


class SimpleSolution:
    """Recursive inorder traversal — O(n) time, O(h) space.

    The straightforward recursive approach: visit left subtree, then root,
    then right subtree. Clean and intuitive but uses implicit call stack.
    """

    def inorderTraversal(self, root):
        result = []

        def inorder(node):
            if node is None:
                return
            inorder(node.left)       # visit left subtree
            result.append(node.val)  # visit current node
            inorder(node.right)      # visit right subtree

        inorder(root)
        return result


# --- Tests ---


class TestBinaryTreeInorderTraversal(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()
        self.simple = SimpleSolution()

    def _traverse(self, sol, values):
        """Build tree from level-order list and return inorder traversal."""
        root = build_tree(values)
        return sol.inorderTraversal(root)

    def test_example_1(self):
        result = self._traverse(self.sol, [1, None, 2, 3])
        self.assertEqual(result, [1, 3, 2])

    def test_example_2(self):
        result = self._traverse(self.sol, [1, 2, 3, 4, 5, None, 8, None, None, 6, 7, 9])
        self.assertEqual(result, [4, 2, 6, 5, 7, 1, 3, 9, 8])

    def test_example_3_empty_tree(self):
        result = self._traverse(self.sol, [])
        self.assertEqual(result, [])

    def test_example_4_single_node(self):
        result = self._traverse(self.sol, [1])
        self.assertEqual(result, [1])

    def test_left_skewed(self):
        """All nodes in a chain to the left: 3 → 2 → 1."""
        # Level-order: [3, 2, null, 1]
        result = self._traverse(self.sol, [3, 2, None, 1])
        self.assertEqual(result, [1, 2, 3])

    def test_right_skewed(self):
        """All nodes in a chain to the right: 1 → 2 → 3."""
        # Level-order: [1, null, 2, null, 3]
        result = self._traverse(self.sol, [1, None, 2, None, 3])
        self.assertEqual(result, [1, 2, 3])

    def test_complete_tree(self):
        """Full binary tree with 3 levels.

              1
            /   \
           2     3
          / \
         4   5
        Inorder: [4, 2, 5, 1, 3]
        """
        result = self._traverse(self.sol, [1, 2, 3, 4, 5])
        self.assertEqual(result, [4, 2, 5, 1, 3])

    def test_negative_values(self):
        """Tree with negative node values."""
        #       -10
        #       /  \
        #     -5    3
        #     /    / \
        #   -20   1   8
        # Inorder: [-20, -5, -10, 1, 3, 8]
        result = self._traverse(self.sol, [-10, -5, 3, -20, None, 1, 8])
        self.assertEqual(result, [-20, -5, -10, 1, 3, 8])

    def test_iterative_matches_recursive(self):
        """Verify both solutions produce the same result on all cases."""
        cases = [
            [1, None, 2, 3],
            [1, 2, 3, 4, 5, None, 8, None, None, 6, 7, 9],
            [],
            [1],
            [3, 2, None, 1],
            [1, None, 2, None, 3],
            [1, 2, 3, 4, 5],
            [-10, -5, 3, -20, None, 1, 8],
        ]
        for values in cases:
            r1 = self._traverse(self.sol, values)
            r2 = self._traverse(self.simple, values)
            self.assertEqual(r1, r2, f"Mismatch for input {values}")


if __name__ == "__main__":
    unittest.main()
