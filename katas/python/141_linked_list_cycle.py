"""
LeetCode #141 - Linked List Cycle (Easy)

Given head, the head of a linked list, determine if the linked list
has a cycle in it.

There is a cycle in a linked list if there is some node in the list
that can be reached again by continuously following the next pointer.
Internally, pos is used to denote the index of the node that tail's
next pointer is connected to. Note that pos is not passed as a parameter.

Return true if there is a cycle in the linked list. Otherwise, return false.

Example 1:
    Input:  head = [3,2,0,-4], pos = 1
    Output: true
    Explanation: There is a cycle in the linked list, where the tail
    connects to the 1st node (0-indexed).

Example 2:
    Input:  head = [1,2], pos = 0
    Output: true
    Explanation: There is a cycle in the linked list, where the tail
    connects to the 0th node.

Example 3:
    Input:  head = [1], pos = -1
    Output: false
    Explanation: There is no cycle in the linked list.

Constraints:
    The number of the nodes in the list is in the range [0, 10^4].
    -10^5 <= Node.val <= 10^5
    pos is -1 or a valid index in the linked-list.

Follow up: Can you solve it using O(1) (i.e. constant) memory?
"""

import unittest


class ListNode:
    """Singly-linked list node (LeetCode's standard definition)."""

    def __init__(self, val=0, next=None):  # noqa: A002 - matches LeetCode signature
        self.val = val
        self.next = next


def build_list(values, pos):
    """Test helper: build a linked list from `values`.

    If pos >= 0, the tail's next pointer is wired back to the node at
    index `pos`, creating a cycle exactly like LeetCode's internal
    representation. pos == -1 means no cycle. Returns the head node
    (or None for an empty list).
    """
    nodes = [ListNode(v) for v in values]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    if pos >= 0 and nodes:
        nodes[-1].next = nodes[pos]
    return nodes[0] if nodes else None


class FloydSolution:
    """Floyd's tortoise-and-hare — O(n) time, O(1) space. The canonical one.

    Two pointers traverse the list at different speeds: slow moves one
    step per iteration, fast moves two. If the list is acyclic, fast
    hits the end (None) and we return False. If there is a cycle, both
    pointers eventually enter it — and once both are inside a loop of
    length L, the gap between them shrinks by exactly 1 every iteration
    (fast gains one step on slow per round). A gap that shrinks by one
    in a finite loop must reach 0, so slow and fast necessarily meet —
    they can never "jump over" each other, because meeting happens on
    a node, not on an edge.

    This satisfies the follow-up's constant-memory requirement with no
    mutation of the list and no reliance on node values (duplicate
    values are legal; identity comparison `is` is what matters).

    Time complexity:  O(n) — slow walks at most n steps before meeting.
    Space complexity: O(1) — two pointers.
    """

    def hasCycle(self, head):
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                return True
        return False


class BrentSolution:
    """Brent's cycle-detection variant — O(n) time, O(1) space.

    A lesser-known sibling of Floyd's algorithm (the oneTelecom-Olympiad
    style answer to "can you do it without two fixed speeds?"). The hare
    moves one step at a time; the tortoise is teleported to the hare's
    position whenever the hare has traveled a power-of-two number of
    steps since the last teleport. Inside a cycle of length L, once the
    tortoise is parked somewhere on the loop, the hare must return to
    that exact node within L steps — and L is always <= the largest
    power of two the hare has already traveled, so a meeting is
    guaranteed while the schedule keeps doubling. Brent's variant does
    fewer `next` hops than Floyd on average (roughly up to ~3x fewer).

    Time complexity:  O(n) — at most ~2x n single steps total.
    Space complexity: O(1) — two pointers and two counters.
    """

    def hasCycle(self, head):
        if head is None:
            return False
        power = 1   # current power of two driving the teleport schedule
        lam = 0     # steps the hare has taken since the last teleport
        tortoise = head
        hare = head.next
        while tortoise is not hare:
            if hare is None:            # ran off the end: no cycle
                return False
            if power == lam:            # hare traveled 2^k steps: teleport
                tortoise = hare
                power *= 2
                lam = 0
            hare = hare.next
            lam += 1
        return True                     # hare landed back on the tortoise


class HashSetSolution:
    """Remember every visited node — O(n) time, O(n) space. Oracle.

    Walk the list once, storing each visited node in a set. The first
    time a node is seen twice, a cycle exists; reaching None means the
    list terminates. ListNode has no __hash__/__eq__ override, so the
    set hashes by identity (object id) — which is exactly right, since
    a cycle is a property of node identity, not of values.

    It ignores the follow-up's constant-space goal, but it is logically
    independent of the pointer-running tricks, which makes it a perfect
    oracle for the randomized cross-check test.

    Time complexity:  O(n) — one pass, O(1) average set operations.
    Space complexity: O(n) — the set of visited nodes.
    """

    def hasCycle(self, head):
        seen = set()
        node = head
        while node:
            if node in seen:
                return True
            seen.add(node)
            node = node.next
        return False


# --- Tests ---


class TestLinkedListCycle(unittest.TestCase):
    def setUp(self):
        self.solutions = [
            FloydSolution(),
            BrentSolution(),
        ]
        self.oracle = HashSetSolution()

    def _check(self, head, expected):
        for sol in self.solutions + [self.oracle]:
            with self.subTest(sol=type(sol).__name__):
                self.assertEqual(sol.hasCycle(head), expected)

    def test_example_1(self):
        # tail (-4) links back to index 1 (value 2)
        self._check(build_list([3, 2, 0, -4], 1), True)

    def test_example_2(self):
        # two-node list whose tail links back to the head
        self._check(build_list([1, 2], 0), True)

    def test_example_3(self):
        # single node, no cycle
        self._check(build_list([1], -1), False)

    def test_empty_list(self):
        # constraint allows 0 nodes; an absent head cannot cycle
        self._check(build_list([], -1), False)

    def test_single_node_self_loop(self):
        # the smallest possible cycle: one node pointing at itself
        self._check(build_list([42], 0), True)

    def test_long_acyclic_list(self):
        # upper end of the constraint range with no cycle
        self._check(build_list(list(range(10_000)), -1), False)

    def test_full_length_cycle(self):
        # cycle that wraps the entire list back to the head
        self._check(build_list(list(range(10_000)), 0), True)

    def test_cycle_starting_in_middle(self):
        # 10k nodes; tail links back to the middle node
        self._check(build_list(list(range(10_000)), 5_000), True)

    def test_cycle_of_length_two(self):
        # last pair points at each other
        self._check(build_list([1, 2, 3, 4, 5], 3), True)

    def test_negative_values(self):
        # values are irrelevant to structure; negatives must not matter
        self._check(build_list([-10**5, 10**5, 0], 1), True)
        self._check(build_list([-10**5, 10**5, 0], -1), False)

    def test_duplicate_values_without_cycle(self):
        # equal values are NOT a cycle — identity, not value, matters
        self._check(build_list([7, 7, 7, 7], -1), False)

    def test_against_oracle_on_random_inputs(self):
        # Oracle test: Floyd and Brent must agree with the HashSet
        # oracle on many random lists honoring the constraints.
        import random

        rng = random.Random(141)  # fixed seed -> deterministic tests
        for _ in range(300):
            n = rng.randint(0, 120)
            values = [rng.randint(-10**5, 10**5) for _ in range(n)]
            pos = rng.randint(-1, n - 1) if n else -1
            head = build_list(values, pos)
            expected = self.oracle.hasCycle(head)
            for sol in self.solutions:
                with self.subTest(sol=type(sol).__name__, n=n, pos=pos):
                    self.assertEqual(sol.hasCycle(head), expected)


if __name__ == "__main__":
    unittest.main()
