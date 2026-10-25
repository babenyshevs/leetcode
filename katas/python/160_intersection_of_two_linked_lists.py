"""
LeetCode #160 - Intersection of Two Linked Lists (Easy)

Given the heads of two singly linked-lists headA and headB, return the
node at which the two lists intersect. If the two lists have no
intersection at all, return null.

For example, the following two lists begin to intersect at node c1:

    A:          a1 → a2
                        ↘
                          c1 → c2 → c3
                        ↗
    B:     b1 → b2 → b3

Notes from the problem:
    - The linked structure is guaranteed cycle-free.
    - The lists must RETAIN THEIR ORIGINAL STRUCTURE after the function
      returns (no cutting, splicing, or re-linking).
    - The function must return the NODE ITSELF (identity), not a node
      with an equal value — see Example 1, where the two `1`s are
      distinct nodes but the two `8`s are one shared node.

Custom judge inputs:
    intersectVal - value at the intersection node (0 = no intersection)
    listA, listB - the two lists as read from their heads
    skipA, skipB - nodes to skip in A / B to reach the intersection

Example 1:
    Input:  intersectVal = 8, listA = [4,1,8,4,5],
            listB = [5,6,1,8,4,5], skipA = 2, skipB = 3
    Output: Intersected at '8'
    The shared part is the single node 8 and everything after it; the
    `1`s before it are different nodes that merely hold equal values.

Example 2:
    Input:  intersectVal = 2, listA = [1,9,1,2,4],
            listB = [3,2,4], skipA = 3, skipB = 1
    Output: Intersected at '2'

Example 3:
    Input:  intersectVal = 0, listA = [2,6,4], listB = [1,5],
            skipA = 3, skipB = 2
    Output: No intersection

Constraints:
    The number of nodes of listA is in the range [1, 3 * 10^4].
    The number of nodes of listB is in the range [1, 3 * 10^4].
    1 <= Node.val <= 10^5
    0 <= skipA <= m
    0 <= skipB <= n
    intersectVal is 0 if the lists do not intersect, otherwise
    listA[skipA] == listB[skipB].

Follow up: Could you write a solution that runs in O(m + n) time and
uses only O(1) memory?  →  See LengthAlignSolution and the classic
TwoPointerSolution, which both meet it.
"""

import unittest


class ListNode:
    """Definition for singly-linked list node."""

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def build_judge_lists(list_a, list_b, skip_a, skip_b):
    """Recreate the custom judge's linked structure.

    The first `skip_a` nodes of A and the first `skip_b` nodes of B are
    private prefixes; from index skip_a / skip_b onward both lists SHARE
    the very same node objects (one common suffix chain). With
    skip_a == len(listA) there is no intersection at all.

    Returns (headA, headB, intersection_node_or_None).
    """
    def build_prefix(values):
        dummy = ListNode()
        tail = dummy
        for v in values:
            tail.next = ListNode(v)
            tail = tail.next
        return dummy.next, tail

    head_a, _ = build_prefix(list_a[:skip_a])
    head_b, _ = build_prefix(list_b[:skip_b])
    shared, _ = build_prefix(list_a[skip_a:])

    # Splice the shared chain onto both prefixes (by reference, not copy).
    tail_a = head_a
    if tail_a is None:
        head_a = shared
    else:
        while tail_a.next is not None:
            tail_a = tail_a.next
        tail_a.next = shared

    tail_b = head_b
    if tail_b is None:
        head_b = shared
    else:
        while tail_b.next is not None:
            tail_b = tail_b.next
        tail_b.next = shared

    return head_a, head_b, shared


def to_values(head):
    """Snapshot a list's values (also used to verify structure intactness)."""
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
    return out


class HashTableSolution:
    """Hash set of visited nodes — O(m + n) time, O(m) space. The baseline.

    Intersection is a question of node IDENTITY, so the obvious first
    move: remember every node of A in a set (objects are hashable by
    identity by default), then scan B; the first node already in the
    set is the junction. If B ends first, the lists never met.

    Why the FIRST such node of B is *the* intersection: the shared
    suffix (if any) is one contiguous run of identical objects, so the
    earliest B-node that appears in A is exactly where the runs merge.

    Time complexity:  O(m + n) — one pass over each list.
    Space complexity: O(m) — the set holds A's nodes.

    Fails the follow-up's O(1)-memory bar, but it is the reference
    (oracle) implementation the tests check the other solutions
    against, and it shows why identity — not value — is the pivot of
    the problem.
    """

    def getIntersectionNode(self, headA, headB):
        seen = set()
        node = headA
        while node is not None:
            seen.add(node)
            node = node.next
        node = headB
        while node is not None:
            if node in seen:
                return node
            node = node.next
        return None


class LengthAlignSolution:
    """Align the tails — O(m + n) time, O(1) space. The follow-up, deterministically.

    Key fact: once two lists intersect, they share the ENTIRE suffix —
    one chain, two entry points. So any intersection node is at the
    same distance d from BOTH tails. Walk each list to measure its
    length; the longer list's head is then advanced by |m - n| so both
    pointers stand equally far from the end. From there the pointers
    move in lockstep: they are at the same node exactly when they have
    reached the junction (or they both fall off the end — no
    intersection).

    Correctness of the lockstep: after alignment, the pointers are at
    positions with equal remaining distance. The first position where
    they coincide is the start of the shared suffix — any earlier
    coincidence would mean a shared node before the suffix, which
    (cycle-free lists) would drag the whole suffix forward and
    contradict the suffix-start definition.

    Time complexity:  O(m + n) — two length passes plus one joint walk.
    Space complexity: O(1) — two pointers, two counters.
    """

    def getIntersectionNode(self, headA, headB):
        def length(head):
            n = 0
            while head is not None:
                n += 1
                head = head.next
            return n

        len_a, len_b = length(headA), length(headB)
        long_head, short_head = (headA, headB) if len_a >= len_b else (headB, headA)

        # Level the playing field: same distance to the tail.
        for _ in range(abs(len_a - len_b)):
            long_head = long_head.next

        while long_head is not short_head:
            long_head = long_head.next
            short_head = short_head.next
        return long_head  # shared node, or None together at the end


class TwoPointerSolution:
    """Pointer swap ("love story") — O(m + n) time, O(1) space. The classic.

    The elegant one-pass form of the alignment idea, no length counting:

        pA walks A; when it hits the end, it continues from B's head.
        pB walks B; when it hits the end, it continues from A's head.

    Each pointer traverses a + shared + b = a + b + shared steps,
    where a / b are the private prefix lengths and `shared` is the
    common suffix (for disjoint lists, shared = 0 and both finish on
    the second None). Equal distances mean the pointers arrive at the
    junction node at the SAME step — the shared suffix they cover in
    lockstep, the prefixes they cover on the swapped legs. If the
    lists never intersect, both pointers hit None simultaneously and
    the loop exits with None: a1 → a2 → c → b3 → b2 → b1 | b3 → … none.

    Edge behaviour: empty A or B immediately yields None (pX falls to
    the other head and both Nones coincide at once; the problem's
    constraints say lists have >= 1 node, but the code survives).

    Time complexity:  O(m + n) — each pointer makes at most two legs.
    Space complexity: O(1) — two pointers, no counting, no set.

    Same asymptotics as LengthAlignSolution, but the "measure, then
    align" bookkeeping is folded into the two-leg walk itself.
    """

    def getIntersectionNode(self, headA, headB):
        if headA is None or headB is None:
            return None

        p_a, p_b = headA, headB
        while p_a is not p_b:
            # Swap heads at each list's end; after both swaps the two
            # pointers have walked equal total distances.
            p_a = headB if p_a is None else p_a.next
            p_b = headA if p_b is None else p_b.next
        return p_a  # junction node, or None (disjoint)


# --- Tests ---


class TestIntersectionOfTwoLinkedLists(unittest.TestCase):
    def setUp(self):
        # The hash-set solution is an obviously-correct transcription of
        # the identity-based definition, so it doubles as the oracle for
        # the two O(1)-space variants.
        self.solutions = [
            HashTableSolution(),
            LengthAlignSolution(),
            TwoPointerSolution(),
        ]
        self.oracle = HashTableSolution()

    def _check(self, list_a, list_b, skip_a, skip_b):
        """Each solution gets a FRESH judge-built structure (the identity
        answer is position-dependent, so structures must not be reused
        across solutions). Checks the returned node's identity against
        the expected shared node and that the lists keep their shape."""
        for sol in self.solutions:
            with self.subTest(sol=type(sol).__name__):
                head_a, head_b, expected = build_judge_lists(
                    list_a, list_b, skip_a, skip_b
                )
                vals_a, vals_b = to_values(head_a), to_values(head_b)

                result = sol.getIntersectionNode(headA=head_a, headB=head_b)

                self.assertIs(result, expected)
                # Original structure must be retained after the call.
                self.assertEqual(to_values(head_a), vals_a)
                self.assertEqual(to_values(head_b), vals_b)

    def test_example_1(self):
        # The `1`s are distinct nodes with equal values — only node 8
        # (index 2 in A, index 3 in B) is shared.
        self._check([4, 1, 8, 4, 5], [5, 6, 1, 8, 4, 5], skip_a=2, skip_b=3)

    def test_example_2(self):
        self._check([1, 9, 1, 2, 4], [3, 2, 4], skip_a=3, skip_b=1)

    def test_example_3_no_intersection(self):
        self._check([2, 6, 4], [1, 5], skip_a=3, skip_b=2)

    def test_value_collision_without_sharing(self):
        # Every value matches pairwise, yet no node object is shared:
        # identity must win over equality.
        self._check([2, 2, 4], [2, 2, 4], skip_a=3, skip_b=3)

    def test_intersect_at_head_of_a(self):
        # A's head IS the shared chain (skipA = 0).
        self._check([1, 2, 3], [5, 6], skip_a=0, skip_b=2)

    def test_intersect_at_head_of_b(self):
        # B's head IS the shared chain (skipB = 0).
        self._check([7, 8], [7, 8, 9], skip_a=1, skip_b=0)

    def test_whole_lists_identical(self):
        # Both heads are the same node: intersection found immediately.
        self._check([1, 2, 3], [1, 2, 3], skip_a=0, skip_b=0)

    def test_single_shared_node(self):
        self._check([5], [5], skip_a=0, skip_b=0)

    def test_single_node_lists_disjoint(self):
        self._check([1], [2], skip_a=1, skip_b=1)

    def test_long_prefixes_equal_lengths(self):
        # Equal total lengths but different private prefixes (3+1 vs
        # 3+1): length alignment is a no-op, so correctness here leans
        # entirely on the lockstep identity check.
        self._check([1, 2, 3, 4], [9, 8, 7, 4], skip_a=3, skip_b=3)

    def test_structure_intact_after_oracle_run(self):
        # Re-walk lists after the oracle: traversal must not mutate links.
        head_a, head_b, _ = build_judge_lists([4, 1, 8, 4, 5], [5, 6, 1, 8, 4, 5], 2, 3)
        self.oracle.getIntersectionNode(headA=head_a, headB=head_b)
        self.assertEqual(to_values(head_a), [4, 1, 8, 4, 5])
        self.assertEqual(to_values(head_b), [5, 6, 1, 8, 4, 5])

    def test_against_oracle_on_random_structures(self):
        # Oracle test: build many random intersecting / disjoint judge
        # structures honoring the constraints and require all solutions
        # to return the exact same node object as the hash-set oracle.
        import random

        rng = random.Random(160)  # fixed seed -> deterministic tests
        for _ in range(300):
            m = rng.randint(1, 30)
            n = rng.randint(1, 30)
            shared_len = rng.randint(0, 15)
            skip_a = rng.randint(0, m)
            skip_b = rng.randint(0, n)

            list_a = [rng.randint(1, 10**5) for _ in range(m)]
            list_b = [rng.randint(1, 10**5) for _ in range(n)]

            if shared_len == 0:
                # No intersection: judge sets intersectVal = 0 and lets
                # the private prefixes run the full lists.
                skip_a, skip_b = m, n
            else:
                # Shared suffix with values drawn from the same range
                # (frequent value collisions put the identity/equality
                # distinction under pressure).
                list_a += [rng.randint(1, 10**5) for _ in range(shared_len)]
                list_b += [rng.randint(1, 10**5) for _ in range(shared_len)]

            head_a, head_b, junction = build_judge_lists(
                list_a, list_b, skip_a, skip_b
            )

            # Harness sanity: on this exact structure, the identity-based
            # oracle must land on the junction the builder spliced in.
            self.assertIs(self.oracle.getIntersectionNode(head_a, head_b), junction)

            # All solutions run on the SAME structure (node identity is
            # the assertion target, so structures must not be rebuilt).
            for sol in self.solutions:
                with self.subTest(sol=type(sol).__name__, m=m, n=n, shared=shared_len):
                    self.assertIs(sol.getIntersectionNode(head_a, head_b), junction)


if __name__ == "__main__":
    unittest.main()
