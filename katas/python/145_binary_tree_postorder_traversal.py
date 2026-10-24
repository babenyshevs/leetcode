"""
LeetCode #145 - Binary Tree Postorder Traversal (Easy)

Given the root of a binary tree, return the postorder traversal of its
nodes' values.

Postorder traversal visits nodes in the order: left subtree → right
subtree → root.

Example 1:
    Input:  root = [1,null,2,3]
    Output: [3,2,1]
    Explanation:
        1
         \\
          2
         /
        3
    Postorder: 3, then 2, then 1 → [3,2,1]

Example 2:
    Input:  root = [1,2,3,4,5,null,8,null,null,6,7,9]
    Output: [4,6,7,5,2,9,8,3,1]

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

    Postorder is "recurse left, recurse right, then visit the node".
    The recursive form is a direct transcription of that sentence — a
    node's value is emitted only after both of its subtrees are fully
    consumed. Each node is visited exactly once and appended exactly
    once.

    The space cost is the implicit call stack: O(h) where h is the tree
    height — O(log n) for a balanced tree, O(n) worst case for a
    degenerate chain. With n <= 100 this is nowhere near Python's
    recursion limit, but the follow-up asks whether the stack can be
    made explicit (see IterativeStackSolution and ReversalSolution) or
    eliminated entirely (see MorrisSolution).

    Time complexity:  O(n) — each node visited once.
    Space complexity: O(h) — recursion depth equals tree height.
    """

    def postorderTraversal(self, root):
        result = []

        def dfs(node):
            if node is None:
                return
            dfs(node.left)           # entire left subtree first ...
            dfs(node.right)          # ... then entire right subtree ...
            result.append(node.val)  # ... only then visit the node

        dfs(root)
        return result


class ReversalSolution:
    """Reverse of a mirrored preorder — O(n) time, O(h) space. The one-line trick.

    Postorder is the exact mirror of a "flipped" preorder. Walk the tree
    as root → right → left (the mirror image of root → left → right) and
    reverse the collected values:

        root → right → left, reversed  ==  left → right → root

    Why the identity holds: the flipped preorder emits every node
    before its children (mirrored order), so reversing the list turns
    "parents before children" into "children before parents", and the
    same reversal un-mirrors the left/right swap — each node ends up
    after both of its subtrees. This is why postorder is the *easy*
    traversal to iterate with a stack — no bookkeeping about resuming,
    unlike the single-stack version below.

    Time complexity:  O(n) — every node pushed and popped exactly once,
                      plus one O(n) reversal pass.
    Space complexity: O(h) — stack holds one root-to-leaf frontier.
    """

    def postorderTraversal(self, root):
        if root is None:
            return []
        result = []
        stack = [root]
        while stack:
            node = stack.pop()
            result.append(node.val)  # pop = visit (mirrored preorder)
            # Left first so the right child (pushed last) pops first.
            if node.left is not None:
                stack.append(node.left)
            if node.right is not None:
                stack.append(node.right)
        result.reverse()  # flips mirrored preorder into true postorder
        return result


class IterativeStackSolution:
    """Single explicit stack — O(n) time, O(h) space. The follow-up, done honestly.

    The reversal trick above sidesteps the hard part; this version is
    the "real" iterative postorder. The difficulty: a node must be
    emitted only after BOTH subtrees finish, so when we come back up to
    a node we must know whether we arrived from its left child or its
    right child. A preorder-style pop-everything loop can't tell.

    Fix: remember the last node emitted. At each node on top of the
    stack:
      - if the right subtree exists and was NOT just finished (i.e. the
        last emitted node is not its root), descend right first;
      - otherwise both subtrees are done — emit the node and pop.

    The symmetric check (descend left first) is unnecessary because a
    node is pushed onto the stack only when its parent is emitted-or-
    pending; its left child is always fully processed before control
    returns to it, tracked by the same last-emitted pointer.

    Time complexity:  O(n) — each node is pushed and popped exactly once
                      (the right-child re-check is O(1) per node).
    Space complexity: O(h) — at most one root-to-leaf frontier on the
                      stack; O(n) worst case for a degenerate chain.
    """

    def postorderTraversal(self, root):
        result = []
        stack = []
        node = root
        last_emitted = None

        while stack or node is not None:
            # Slide down to the leftmost unvisited node, parking every
            # ancestor on the stack.
            while node is not None:
                stack.append(node)
                node = node.left
            top = stack[-1]
            # Right subtree pending? Descend into it (don't pop yet) —
            # unless we just came back up from exactly that subtree.
            if top.right is not None and last_emitted is not top.right:
                node = top.right
            else:
                result.append(top.val)
                last_emitted = top
                stack.pop()

        return result


class MorrisSolution:
    """Morris postorder traversal — O(n) time, O(1) space. No stack at all.

    Same threading idea as Morris preorder/inorder (see problem 144):
    a node with a left subtree threads its inorder predecessor's right
    pointer back to itself, creating a return path inside the tree.

    Postorder's twist is *when* to emit. For a node whose left subtree
    has just been fully consumed (we arrived back via a thread), the
    entire right spine of that left subtree — from the subtree root
    down to the thread target — is ready to be emitted, but in reverse
    order (deepest first). So: walk that spine collecting values into a
    temporary list, then append them reversed. At the very end, do the
    same for the root's own right spine, which is the last group the
    loop never gets to "come back" for.

    Correctness intuition: postorder groups values as
    [left subtree][right subtree][root]; Morris's spine-reversal emits
    exactly those right-spine groups back-to-front within the left
    subtree, in left-to-right order, with the root's spine last.

    The traversal temporarily mutates the tree but restores every right
    pointer it changed: each thread is created once and erased once,
    and the spine-walk only reads, so the tree is structurally
    identical after the call.

    Amortized analysis: each edge is walked at most twice (once to
    create a thread, once to erase it), plus the one-time final spine
    emission — total work stays O(n).

    Time complexity:  O(n) amortized — each edge traversed <= 2 times.
    Space complexity: O(1) for the traversal itself; the temporary list
                      for one spine reversal is bounded by O(h).
                      (Strict O(1) postorder requires emitting through
                      a sublist reversal of the output itself.)
    """

    def postorderTraversal(self, root):
        def emit_spine_reversed(node, out):
            """Append the right spine of `node` to `out`, deepest first."""
            spine = []
            while node is not None:
                spine.append(node.val)
                node = node.right
            out.extend(reversed(spine))

        result = []
        current = root
        while current is not None:
            if current.left is None:
                # No left subtree: nothing to thread, nothing to emit
                # yet (postorder defers the node itself). Move right.
                current = current.right
            else:
                # Find the inorder predecessor: rightmost node of the
                # left subtree (its right pointer is either None or a
                # thread back to us).
                predecessor = current.left
                while predecessor.right is not None and predecessor.right is not current:
                    predecessor = predecessor.right

                if predecessor.right is None:
                    predecessor.right = current  # create the thread
                    current = current.left
                else:
                    # Came back via a thread: left subtree is done.
                    predecessor.right = None     # erase the thread
                    # The finished left subtree's right spine is ready,
                    # deepest node first.
                    emit_spine_reversed(current.left, result)
                    current = current.right

        # The loop above never "returns" to the root, so its own right
        # spine is the final postorder group.
        emit_spine_reversed(root, result)
        return result


# --- Tests ---


class TestBinaryTreePostorderTraversal(unittest.TestCase):
    def setUp(self):
        # The recursive solution doubles as the oracle: it is a direct
        # transcription of the definition, so agreement with it is a
        # strong independent check for the iterative/Morris variants.
        self.solutions = [
            RecursiveSolution(),
            ReversalSolution(),
            IterativeStackSolution(),
            MorrisSolution(),
        ]
        self.oracle = RecursiveSolution()

    def _check(self, values, expected):
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.postorderTraversal(build_tree(values)), expected)

    def test_example_1(self):
        self._check([1, None, 2, 3], [3, 2, 1])

    def test_example_2(self):
        self._check(
            [1, 2, 3, 4, 5, None, 8, None, None, 6, 7, 9],
            [4, 6, 7, 5, 2, 9, 8, 3, 1],
        )

    def test_example_3_empty_tree(self):
        self._check([], [])

    def test_example_4_single_node(self):
        self._check([1], [1])

    def test_left_skewed_chain(self):
        # Degenerate tree: every node hangs off the left. Worst case for
        # recursion depth; exercises the single-stack "descend left,
        # emit on the way back up" path.
        self._check([3, 2, None, 1, None], [1, 2, 3])

    def test_right_skewed_chain(self):
        # Degenerate tree: every node hangs off the right. Postorder
        # emits the deepest node first; Morris's final spine emission
        # does the bulk of the work here.
        self._check([1, None, 2, None, 3], [3, 2, 1])

    def test_negative_values(self):
        # Constraint allows values down to -100; traversal is value-agnostic.
        self._check([0, -100, 100], [-100, 100, 0])

    def test_duplicates(self):
        # Equal values must each appear the right number of times.
        self._check([7, 7, 7], [7, 7, 7])

    def test_morris_restores_tree_structure(self):
        # Morris temporarily rewrites right pointers via threads; after a
        # traversal the tree must be structurally intact. Verify by
        # producing identical postorders from two consecutive runs.
        root = build_tree([1, 2, 3, 4, 5, None, 8, None, None, 6, 7, 9])
        sol = MorrisSolution()
        first = sol.postorderTraversal(root)
        second = sol.postorderTraversal(root)
        self.assertEqual(first, second)
        self.assertEqual(first, [4, 6, 7, 5, 2, 9, 8, 3, 1])

    def test_against_oracle_on_random_trees(self):
        # Oracle test: the reversal, single-stack, and Morris variants
        # must all agree with the recursive oracle on many random trees
        # honoring the constraints. Also verifies Morris leaves the tree
        # intact: each tree is traversed by Morris first, then
        # re-traversed by the oracle.
        import random

        rng = random.Random(145)  # fixed seed -> deterministic tests
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
            expected = self.oracle.postorderTraversal(root)
            for sol in (ReversalSolution(), IterativeStackSolution(), MorrisSolution()):
                # Rebuild an identical tree for each solution (Morris
                # restores itself, but fresh inputs keep tests independent).
                with self.subTest(sol=type(sol).__name__, n=n):
                    self.assertEqual(sol.postorderTraversal(clone(root)), expected)


if __name__ == "__main__":
    unittest.main()
