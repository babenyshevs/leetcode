"""
LeetCode #83 - Remove Duplicates from Sorted List (Easy)

Given the head of a sorted linked list, delete all duplicates such
that each element appears only once. Return the linked list sorted
as well.

Example 1:
    Input: head = [1,1,2]
    Output: [1,2]

Example 2:
    Input: head = [1,1,2,3,3]
    Output: [1,2,3]

Constraints:
    The number of nodes in the list is in the range [0, 300].
    -100 <= Node.val <= 100
    The list is guaranteed to be sorted in ascending order.
"""

import unittest


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __repr__(self):
        return f"ListNode({self.val})"

    def __eq__(self, other):
        if not isinstance(other, ListNode):
            return False
        a, b = self, other
        while a and b:
            if a.val != b.val:
                return False
            a, b = a.next, b.next
        return a is None and b is None

    @staticmethod
    def from_list(values):
        """Create a linked list from a Python list of values."""
        dummy = ListNode()
        curr = dummy
        for v in values:
            curr.next = ListNode(v)
            curr = curr.next
        return dummy.next

    def to_list(self):
        """Convert linked list to a Python list."""
        result = []
        curr = self
        while curr:
            result.append(curr.val)
            curr = curr.next
        return result


class Solution:
    """Two-pointer iteration — O(n) time, O(1) space.

    Since the list is sorted, all duplicates are adjacent. We use a
    single `current` pointer and compare each node with the next:
    - If current.val == next.val, skip next by relinking:
        current.next = current.next.next
    - Otherwise, advance current.

    This is done in-place with no extra memory.
    """

    def deleteDuplicates(self, head):
        if not head:
            return None

        current = head
        while current and current.next:
            if current.val == current.next.val:
                # Skip the duplicate node
                current.next = current.next.next
            else:
                # Only advance when no duplicate was found
                current = current.next

        return head


class RecursiveSolution:
    """Recursive approach — O(n) time, O(n) space (call stack).

    Recursively deduplicate the rest of the list, then compare
    head.val with head.next.val. If equal, skip head.next.

    Elegant but uses O(n) stack space, so the iterative solution
    is preferred for production.
    """

    def deleteDuplicates(self, head):
        if not head or not head.next:
            return head

        # Deduplicate the tail first
        head.next = self.deleteDuplicates(head.next)

        if head.val == head.next.val:
            return head.next

        return head


# --- Tests ---


class TestRemoveDuplicatesFromSortedList(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()
        self.recursive = RecursiveSolution()

    def test_example_1(self):
        head = ListNode.from_list([1, 1, 2])
        result = self.sol.deleteDuplicates(head)
        self.assertEqual(result.to_list(), [1, 2])

    def test_example_2(self):
        head = ListNode.from_list([1, 1, 2, 3, 3])
        result = self.sol.deleteDuplicates(head)
        self.assertEqual(result.to_list(), [1, 2, 3])

    def test_empty_list(self):
        result = self.sol.deleteDuplicates(None)
        self.assertIsNone(result)

    def test_single_node(self):
        head = ListNode.from_list([1])
        result = self.sol.deleteDuplicates(head)
        self.assertEqual(result.to_list(), [1])

    def test_all_duplicates(self):
        head = ListNode.from_list([1, 1, 1, 1])
        result = self.sol.deleteDuplicates(head)
        self.assertEqual(result.to_list(), [1])

    def test_no_duplicates(self):
        head = ListNode.from_list([1, 2, 3, 4, 5])
        result = self.sol.deleteDuplicates(head)
        self.assertEqual(result.to_list(), [1, 2, 3, 4, 5])

    def test_negative_values(self):
        head = ListNode.from_list([-3, -3, -1, 0, 0, 1])
        result = self.sol.deleteDuplicates(head)
        self.assertEqual(result.to_list(), [-3, -1, 0, 1])

    def test_recursive_matches_iterative(self):
        for values in [
            [1, 1, 2],
            [1, 1, 2, 3, 3],
            [1, 2, 3, 4, 5],
            [1, 1, 1, 1],
            [],
            [5],
            [-3, -3, -1, 0, 0, 1],
        ]:
            h1 = ListNode.from_list(values)
            h2 = ListNode.from_list(values)
            r1 = self.sol.deleteDuplicates(h1)
            r2 = self.recursive.deleteDuplicates(h2)
            list1 = r1.to_list() if r1 else []
            list2 = r2.to_list() if r2 else []
            self.assertEqual(list1, list2, f"Mismatch for input {values}")


if __name__ == "__main__":
    unittest.main()
