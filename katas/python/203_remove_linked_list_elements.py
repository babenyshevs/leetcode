"""
LeetCode #203 - Remove Linked List Elements (Easy)

Given the head of a linked list and an integer val, remove all the nodes
of the linked list that have Node.val == val, and return the new head.

Example 1:
    Input:  head = [1,2,6,3,4,5,6], val = 6
    Output: [1,2,3,4,5]

Example 2:
    Input:  head = [], val = 1
    Output: []

Example 3:
    Input:  head = [7,7,7,7], val = 7
    Output: []

Constraints:
    The number of nodes in the list is in the range [0, 10**4].
    1 <= Node.val <= 50
    0 <= val <= 50

Key insight: deleting a node requires rewiring its *predecessor*, but the
head has no predecessor — the classic edge case (val at the front, several
vals at the front, or an all-val list). The sentinel (dummy) node trick
removes the special case: prepend a fake node before head and walk the
list with `prev` pointers; afterwards the answer is simply
`sentinel.next`. The recursive variant delegates the same rewiring to the
call stack: fix up the rest of the list first, then decide whether the
current node survives.
"""

import unittest


class ListNode:
    """Singly linked list node as defined by LeetCode."""

    def __init__(self, val=0, next=None):  # noqa: A002 - LeetCode signature
        self.val = val
        self.next = next


def _build(values):
    """Helper: build a linked list from a Python list, return its head."""
    dummy = ListNode()
    tail = dummy
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def _to_list(head):
    """Helper: convert a linked list back to a Python list for assertions."""
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


class SentinelSolution:
    """Dummy-head iteration — the standard, allocation-free approach.

    Attach a sentinel node in front of head. Now every real node has a
    predecessor, so deletion is uniform: whenever `prev.next` holds the
    target value, bypass it with `prev.next = prev.next.next` (do NOT
    advance prev — the new prev.next may also be a target); otherwise
    advance prev. The rewired list starts at sentinel.next, and the
    original head reference is untouched.

    Time complexity:  O(n) — each node is examined exactly once.
    Space complexity: O(1) — one sentinel node, no recursion.
    """

    def removeElements(self, head, val):
        sentinel = ListNode(0)
        sentinel.next = head
        prev = sentinel
        while prev.next:
            if prev.next.val == val:
                prev.next = prev.next.next
            else:
                prev = prev.next
        return sentinel.next


class HeadFirstSolution:
    """Strip leading matches, then iterate — explicit edge-case handling.

    The no-sentinel textbook approach: first advance head past every
    leading node equal to val (head itself may change several times),
    then walk with a `curr` pointer knowing curr itself never needs
    deletion, so only curr.next is inspected. Works, but the two-phase
    structure exists purely to handle the missing-predecessor case that
    the sentinel dissolves — a good illustration of why the dummy node
    idiom exists.

    Time complexity:  O(n) — leading strip plus one pass.
    Space complexity: O(1).
    """

    def removeElements(self, head, val):
        while head and head.val == val:
            head = head.next
        curr = head
        while curr and curr.next:
            if curr.next.val == val:
                curr.next = curr.next.next
            else:
                curr = curr.next
        return head


class RecursiveSolution:
    """Recursion — solve for the tail, then keep or drop the head.

    Base case: an empty list stays empty. Recursive case: first obtain
    the fully filtered rest of the list (rec on head.next), then keep
    the current node only if its value differs from val, pointing it at
    the filtered rest either way. Concise, but each of the up to 10**4
    nodes costs a stack frame — fine for the given constraint, yet the
    iterative solutions are strictly safer in production Python.

    Time complexity:  O(n) — one call per node.
    Space complexity: O(n) — call stack depth equals list length.
    """

    def removeElements(self, head, val):
        if head is None:
            return None
        head.next = self.removeElements(head.next, val)
        return head.next if head.val == val else head


# --- Tests ---


class TestRemoveElements(unittest.TestCase):
    def setUp(self):
        self.solutions = [
            SentinelSolution(),
            HeadFirstSolution(),
            RecursiveSolution(),
        ]

    def test_example_1(self):
        # [1,2,6,3,4,5,6], val=6 -> [1,2,3,4,5]
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                head = _build([1, 2, 6, 3, 4, 5, 6])
                self.assertEqual(_to_list(sol.removeElements(head, 6)),
                                 [1, 2, 3, 4, 5])

    def test_example_2_empty_list(self):
        # [] stays [] for any val.
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(_to_list(sol.removeElements(None, 1)), [])

    def test_example_3_all_match(self):
        # [7,7,7,7], val=7 -> [] — head must end up None.
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                head = _build([7, 7, 7, 7])
                self.assertIs(sol.removeElements(head, 7), None)

    def test_delete_head(self):
        # Only the first node matches; the rest must survive.
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                head = _build([1, 2, 2])
                self.assertEqual(_to_list(sol.removeElements(head, 1)),
                                 [2, 2])

    def test_leading_run_of_matches(self):
        # Multiple consecutive matches at the front — the case the
        # HeadFirstSolution strip loop exists for.
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                head = _build([6, 6, 6, 1, 2])
                self.assertEqual(_to_list(sol.removeElements(head, 6)),
                                 [1, 2])

    def test_no_match(self):
        # val absent from the list: structure must come back unchanged.
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                head = _build([1, 2, 3])
                self.assertEqual(_to_list(sol.removeElements(head, 9)),
                                 [1, 2, 3])

    def test_single_node_match_and_no_match(self):
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                self.assertIs(sol.removeElements(_build([1]), 1), None)
                self.assertEqual(_to_list(sol.removeElements(_build([1]), 2)),
                                 [1])

    def test_alternating_matches(self):
        # Deletions at both ends and in the middle of every pair.
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                head = _build([1, 6, 2, 6, 3, 6])
                self.assertEqual(_to_list(sol.removeElements(head, 6)),
                                 [1, 2, 3])

    def test_boundary_values(self):
        # Node values run 1..50 and val may be 0 (never present) or 50.
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                head = _build([50, 1, 50, 49])
                self.assertEqual(_to_list(sol.removeElements(head, 50)),
                                 [1, 49])
                fresh = _build([50, 1, 50, 49])
                self.assertEqual(_to_list(sol.removeElements(fresh, 0)),
                                 [50, 1, 50, 49])

    def test_large_input(self):
        # Upper constraint size (10**4 nodes): every third node matches,
        # and the result must interleave survivors correctly.
        n = 10**4
        values = [i % 50 + 1 for i in range(n)]  # vals within 1..50
        head = _build(values)
        kept = SentinelSolution().removeElements(head, values[0])
        expected = [v for v in values if v != values[0]]
        self.assertEqual(_to_list(kept), expected)

    def test_agree_with_oracle_randomized(self):
        # All solutions must agree with an independent list-comprehension
        # oracle on random lists drawn from the constraint space.
        import random

        rng = random.Random(203)
        for _ in range(200):
            length = rng.randint(0, 60)
            values = [rng.randint(1, 50) for _ in range(length)]
            val = rng.randint(0, 50)
            expected = [v for v in values if v != val]
            for sol in self.solutions:
                with self.subTest(sol=type(sol).__name__, val=val):
                    head = _build(values)
                    self.assertEqual(_to_list(sol.removeElements(head, val)),
                                     expected)


if __name__ == "__main__":
    unittest.main()
