"""
LeetCode #108 - Convert Sorted Array to Binary Search Tree (Easy)

Given an integer array nums where the elements are sorted in
ascending order, convert it to a height-balanced binary search tree.

Example 1:
    Input: nums = [-10,-3,0,5,9]
    Output: [0,-3,9,-10,null,5]
    Explanation: [0,-10,5,null,-3,null,9] is also accepted:

         0          0
        / \        / \
      -3   9    -10   9
      / \        / \
    -10  5     -3   5

Example 2:
    Input: nums = [1,3]
    Output: [3,1]
    Explanation: [1,null,3] and [3,1] are both height-balanced BSTs.

Constraints:
    1 <= nums.length <= 10^4
    -10^4 <= nums[i] <= 10^4
    nums is sorted in a strictly increasing order.
"""

import unittest


class TreeNode:
    """Definition for a binary tree node."""

    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """Recursive middle-element split — O(n) time, O(log n) space.

    Key insight: the middle element of a sorted array is the root of a
    balanced BST. Everything left of it is smaller (becomes the left
    subtree) and everything right of it is larger (becomes the right
    subtree). Recursing on both halves keeps every subtree's node count
    split as evenly as possible, which guarantees the height-balanced
    property. Any valid height-balanced BST is accepted by the judge,
    and the middle-split produces one deterministically.

    Time complexity:  O(n) — every element becomes exactly one node.
    Space complexity: O(log n) — recursion depth equals tree height
                       (output tree not counted).
    """

    def sortedArrayToBST(self, nums):
        def build(left, right):
            if left > right:
                return None
            mid = (left + right + 1) // 2  # upper middle, matches LC examples
            node = TreeNode(nums[mid])
            node.left = build(left, mid - 1)
            node.right = build(mid + 1, right)
            return node

        return build(0, len(nums) - 1)


class SimpleSolution:
    """Slicing variant — O(n log n) time, O(n) space.

    The most readable formulation: copy the middle element, then recurse
    on the two Python slices `nums[:mid]` and `nums[mid+1:]`. Same tree
    shape as Solution (both split at the same midpoints); slicing costs
    extra copying, so it's the simpler-but-slower companion.
    """

    def sortedArrayToBST(self, nums):
        if not nums:
            return None
        # For a slice of length n the upper-middle index is n // 2,
        # which matches the recursive build's midpoint choice.
        mid = len(nums) // 2
        root = TreeNode(nums[mid])
        root.left = self.sortedArrayToBST(nums[:mid])
        root.right = self.sortedArrayToBST(nums[mid + 1:])
        return root


# --- Helpers for tests ---


def tree_to_level_order(root):
    """Serialize a tree to a level-order list with None placeholders.

    Trailing Nones are trimmed, matching LeetCode's list notation.
    """
    if root is None:
        return []

    out = []
    queue = [root]
    while queue:
        node = queue.pop(0)
        if node is None:
            out.append(None)
            continue
        out.append(node.val)
        queue.append(node.left)
        queue.append(node.right)

    while out and out[-1] is None:
        out.pop()
    return out


def is_bst(root, lo=float("-inf"), hi=float("inf")):
    """Return True if the tree is a valid BST (strict ordering)."""
    if root is None:
        return True
    if not (lo < root.val < hi):
        return False
    return is_bst(root.left, lo, root.val) and is_bst(root.right, root.val, hi)


def is_height_balanced(root):
    """Return True if every node's subtrees differ in height by <= 1.

    Returns (balanced, height) internally; the helper raises if any
    node is unbalanced so failures point at the exact case.
    """

    def check(node):
        if node is None:
            return True, 0
        left_ok, left_h = check(node.left)
        if not left_ok:
            return False, 0
        right_ok, right_h = check(node.right)
        if not right_ok or abs(left_h - right_h) > 1:
            return False, 0
        return True, 1 + max(left_h, right_h)

    balanced, _ = check(root)
    return balanced


def collect_inorder(root):
    """In-order traversal values of a tree as a list."""
    if root is None:
        return []
    return collect_inorder(root.left) + [root.val] + collect_inorder(root.right)


# --- Tests ---


class TestConvertSortedArrayToBST(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()
        self.simple = SimpleSolution()

    def _check(self, sol, nums):
        """Common assertions: BST property, balance, and sorted content."""
        root = sol.sortedArrayToBST(list(nums))
        self.assertTrue(is_bst(root), f"not a BST for {nums}")
        self.assertTrue(
            is_height_balanced(root), f"not height-balanced for {nums}"
        )
        self.assertEqual(collect_inorder(root), list(nums), f"wrong contents for {nums}")
        return root

    def test_example_1(self):
        root = self._check(self.sol, [-10, -3, 0, 5, 9])
        # Deterministic middle-split shape: root 0, left child -3, right child 9.
        self.assertEqual(root.val, 0)
        self.assertEqual(root.left.val, -3)
        self.assertEqual(root.right.val, 9)
        self.assertEqual(root.left.left.val, -10)
        self.assertEqual(root.right.left.val, 5)

    def test_example_2(self):
        root = self._check(self.sol, [1, 3])
        self.assertEqual(tree_to_level_order(root), [3, 1])

    def test_single_element(self):
        root = self._check(self.sol, [1])
        self.assertEqual(root.val, 1)
        self.assertIsNone(root.left)
        self.assertIsNone(root.right)

    def test_negative_values(self):
        self._check(self.sol, [-10, -4, -2, 0, 3, 7])

    def test_three_elements(self):
        root = self._check(self.sol, [1, 2, 3])
        self.assertEqual(root.val, 2)
        self.assertEqual(root.left.val, 1)
        self.assertEqual(root.right.val, 3)

    def test_power_of_two_size(self):
        self._check(self.sol, [0, 1, 2, 3, 4, 5, 6, 7])

    def test_large_input(self):
        nums = list(range(-5000, 5001))  # 10001 nodes, max constraint scale
        root = self._check(self.sol, nums)
        # log2(10001) ~= 13.3, so a balanced tree is at most 14 tall.
        _, height = _height(root)
        self.assertLessEqual(height, 14)

    def test_structure_is_deterministic(self):
        """Both solutions must build the exact same tree for a given input."""
        cases = [
            [-10, -3, 0, 5, 9],
            [1, 3],
            [1],
            [1, 2, 3],
            [0, 1, 2, 3, 4, 5, 6, 7],
        ]
        for nums in cases:
            a = tree_to_level_order(self.sol.sortedArrayToBST(list(nums)))
            b = tree_to_level_order(self.simple.sortedArrayToBST(list(nums)))
            self.assertEqual(a, b, f"structure mismatch for {nums}")

    def test_simple_solution_matches(self):
        """The slicing variant satisfies all the same properties."""
        for nums in ([-10, -3, 0, 5, 9], [1, 3], [1], [-5, -3, 0, 2, 8]):
            root = self.simple.sortedArrayToBST(list(nums))
            self.assertTrue(is_bst(root))
            self.assertTrue(is_height_balanced(root))
            self.assertEqual(collect_inorder(root), list(nums))


def _height(root):
    """Return (ok, height) helper reused by the large-input test."""

    def check(node):
        if node is None:
            return True, 0
        left_ok, left_h = check(node.left)
        right_ok, right_h = check(node.right)
        ok = left_ok and right_ok and abs(left_h - right_h) <= 1
        return ok, 1 + max(left_h, right_h)

    return check(root)


if __name__ == "__main__":
    unittest.main()
