"""
LeetCode #144 - Binary Tree Preorder Traversal (Easy)

Given the root of a binary tree, return the preorder traversal of its
nodes' values.

Preorder traversal visits nodes in the order: root → left subtree →
right subtree.

Example 1:
    Input:  root = [1,null,2,3]
    Output: [1,2,3]
    Explanation:
        1
         \\
          2
         /
        3
    Preorder: 1, then 2, then 3 → [1,2,3]

Example 2:
    Input:  root = [1,2,3,4,5,null,8,null,null,6,7,9]
    Output: [1,2,4,5,6,7,3,8,9]

Example 3:
    Input:  root = []
    Output: []

Example 4:
    Input:  root = [1]
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


class RecursiveSolution:
    """Recursive DFS — O(n) time, O(h) space. The definition, literally.

    Preorder is "visit the node, then recurse left, then recurse right".
    The recursive form is a direct transcription of that sentence, which
    is exactly why the follow-up calls it trivial. Each node is visited
    exactly once and appended exactly once.

    The space cost is the implicit call stack: O(h) where h is the tree
    height — O(log n) for a balanced tree, O(n) worst case for a degenerate
    chain. With n <= 100 this is nowhere near Python's recursion limit,
    but the follow-up asks whether the stack can be made explicit (see
    IterativeStackSolution) or eliminated entirely (see MorrisSolution).

    Time complexity:  O(n) — each node visited once.
    Space complexity: O(h) — recursion depth equals tree height.
    """

    def preorderTraversal(self, root):
        result = []

        def dfs(node):
            if node is None:
                return
            result.append(node.val)  # visit: root ...
            dfs(node.left)           # ... then entire left subtree ...
            dfs(node.right)          # ... then entire right subtree

        dfs(root)
        return result


class IterativeStackSolution:
    """Explicit stack — O(n) time, O(h) space. The follow-up's answer.

    Simulates the recursive call stack with our own stack. The trick that
    makes preorder the *easy* traversal to iterate: push the right child
    first, then the left. The stack is LIFO, so the left child pops before
    the right — matching the root→left→right visit order without any
    bookkeeping about "where to resume", because a node's value is fully
    consumed the moment it is popped. (Inorder/postorder iteration are
    harder precisely because the deferred work must be revisited.)

    Time complexity:  O(n) — every node pushed and popped exactly once.
    Space complexity: O(h) — the stack holds at most one root-to-leaf
                      frontier; O(n) worst case for a degenerate chain.
    """

    def preorderTraversal(self, root):
        if root is None:
            return []
        result = []
        stack = [root]
        while stack:
            node = stack.pop()
            result.append(node.val)   # pop = visit
            # Right first so the left child (pushed last) pops first.
            if node.right is not None:
                stack.append(node.right)
            if node.left is not None:
                stack.append(node.left)
        return result


class MorrisSolution:
    """Morris preorder traversal — O(n) time, O(1) space. No stack at all.

    The trick: a node with a left subtree has no natural way to "return"
    to itself after finishing that subtree — recursion/stacks exist to
    remember exactly that. Morris creates the return path inside the tree
    itself, using right pointers of predecessor nodes as temporary
    "threads".

    For each node with a left child, find its inorder predecessor (the
    rightmost node of the left subtree) and thread pred.right back to the
    current node. Walk down the left side. When we later arrive back at
    the current node via a thread, the thread has served its purpose —
    the left subtree is done — so we erase it and move right.

    Preorder timing detail: the value is emitted when a node is first
    reached — either naturally from above, or via a thread before we dive
    left. Emitting on first touch (rather than on thread-removal, as
    inorder does) is the single-line difference between Morris preorder
    and Morris inorder.

    The traversal temporarily mutates the tree but restores every right
    pointer it changed: each thread is created once and erased once, so
    the tree is structurally identical after the call.

    Amortized analysis: finding a predecessor walks a left subtree's right
    spine, but each edge of the tree is walked at most twice (once to
    create a thread, once to erase it), so the total work is O(n), not
    O(n log n) or worse.

    Time complexity:  O(n) amortized — each edge traversed <= 2 times.
    Space complexity: O(1) — two pointers, satisfies the follow-up fully.
    """

    def preorderTraversal(self, root):
        result = []
        current = root
        while current is not None:
            if current.left is None:
                # No left subtree: visit and move right. Nothing to thread.
                result.append(current.val)
                current = current.right
            else:
                # Find the inorder predecessor: rightmost node of the
                # left subtree (its right pointer is either None or a
                # thread back to us).
                predecessor = current.left
                while predecessor.right is not None and predecessor.right is not current:
                    predecessor = predecessor.right

                if predecessor.right is None:
                    # First visit: emit NOW (preorder = root before subtree),
                    # then thread and descend left.
                    result.append(current.val)
                    predecessor.right = current  # create the thread
                    current = current.left
                else:
                    # Came back via a thread: left subtree is done.
                    predecessor.right = None     # erase the thread
                    current = current.right
        return result


# --- Tests ---


class TestBinaryTreePreorderTraversal(unittest.TestCase):
    def setUp(self):
        # The recursive solution doubles as the oracle: it is a direct
        # transcription of the definition, so agreement with it is a
        # strong independent check for the iterative/Morris variants.
        self.solutions = [
            RecursiveSolution(),
            IterativeStackSolution(),
            MorrisSolution(),
        ]
        self.oracle = RecursiveSolution()

    def _check(self, values, expected):
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.preorderTraversal(build_tree(values)), expected)

    def test_example_1(self):
        self._check([1, None, 2, 3], [1, 2, 3])

    def test_example_2(self):
        self._check(
            [1, 2, 3, 4, 5, None, 8, None, None, 6, 7, 9],
            [1, 2, 4, 5, 6, 7, 3, 8, 9],
        )

    def test_example_3_empty_tree(self):
        self._check([], [])

    def test_example_4_single_node(self):
        self._check([1], [1])

    def test_left_skewed_chain(self):
        # Degenerate tree: every node hangs off the left. Worst case for
        # recursion depth; also exercises Morris's "no right children" path.
        self._check([3, 2, None, 1, None], [3, 2, 1])

    def test_right_skewed_chain(self):
        # Degenerate tree: every node hangs off the right. The Morris
        # "left is None" shortcut fires at every node here.
        self._check([1, None, 2, None, 3], [1, 2, 3])

    def test_negative_values(self):
        # Constraint allows values down to -100; traversal is value-agnostic.
        self._check([0, -100, 100], [0, -100, 100])

    def test_duplicates(self):
        # Equal values must each appear the right number of times.
        self._check([7, 7, 7], [7, 7, 7])

    def test_morris_restores_tree_structure(self):
        # Morris temporarily rewrites right pointers via threads; after a
        # traversal the tree must be structurally intact. Verify by
        # producing identical preorders from two consecutive runs.
        root = build_tree([1, 2, 3, 4, 5, None, 8, None, None, 6, 7, 9])
        sol = MorrisSolution()
        first = sol.preorderTraversal(root)
        second = sol.preorderTraversal(root)
        self.assertEqual(first, second)
        self.assertEqual(first, [1, 2, 4, 5, 6, 7, 3, 8, 9])

    def test_against_oracle_on_random_trees(self):
        # Oracle test: iterative and Morris must agree with the recursive
        # oracle on many random trees honoring the constraints. Also
        # verifies Morris leaves the tree intact: each tree is traversed
        # by Morris first, then re-traversed by the oracle.
        import random

        rng = random.Random(144)  # fixed seed -> deterministic tests
        for _ in range(200):
            n = rng.randint(0, 60)
            values = [rng.randint(-100, 100) for _ in range(n)]

            # Build a random-shape tree directly: node i may skip either
            # child, so depth varies widely, including skewed chains
            # (level-order lists with None would bias toward bushy trees).
            def random_tree(i):
                if i >= n:
                    return None
                node = TreeNode(values[i])
                node.left = random_tree(2 * i + 1) if rng.random() < 0.85 else None
                node.right = random_tree(2 * i + 2) if rng.random() < 0.85 else None
                return node

            def clone(src):
                if src is None:
                    return None
                copy = TreeNode(src.val)
                copy.left = clone(src.left)
                copy.right = clone(src.right)
                return copy

            root = random_tree(0)
            expected = self.oracle.preorderTraversal(root)
            for sol in (IterativeStackSolution(), MorrisSolution()):
                # Rebuild an identical tree for each solution (Morris
                # restores itself, but fresh inputs keep tests independent).
                with self.subTest(sol=type(sol).__name__, n=n):
                    self.assertEqual(sol.preorderTraversal(clone(root)), expected)


if __name__ == "__main__":
    unittest.main()
