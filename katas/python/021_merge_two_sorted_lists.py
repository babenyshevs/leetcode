"""
LeetCode #21 - Merge Two Sorted Lists (Easy)

You are given the heads of two sorted linked lists list1 and list2.
Merge the two lists into one sorted list. The list should be made by
splicing together the nodes of the first two lists.

Return the head of the merged linked list.

Example 1:
    Input: list1 = [1,2,4], list2 = [1,3,4]
    Output: [1,1,2,3,4,4]

Example 2:
    Input: list1 = [], list2 = []
    Output: []

Example 3:
    Input: list1 = [], list2 = [0]
    Output: [0]

Constraints:
    The number of nodes in both lists is in the range [0, 50].
    -100 <= Node.val <= 100
    Both list1 and list2 are sorted in non-decreasing order.
"""

import unittest
from typing import List, Optional


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val: int = 0, next: Optional["ListNode"] = None):
        self.val = val
        self.next = next

    def __repr__(self):
        return f"ListNode(val={self.val}, next={self.next})"


class Solution:
    """Iterative merge — O(m+n) time, O(1) extra space.

    Use a dummy sentinel node so we don't have to special-case the head.
    Walk both lists with two pointers, always appending the smaller node
    to the merged tail, and advancing that list's pointer.
    After one list is exhausted, attach the remainder of the other.
    """

    def mergeTwoLists(
        self, list1: Optional[ListNode], list2: Optional[ListNode]
    ) -> Optional[ListNode]:
        dummy = ListNode()  # sentinel node
        tail = dummy

        while list1 and list2:
            if list1.val <= list2.val:
                tail.next = list1
                list1 = list1.next
            else:
                tail.next = list2
                list2 = list2.next
            tail = tail.next

        # Attach whatever remains (one of them is None)
        tail.next = list1 or list2

        return dummy.next


class SolutionRecursive:
    """Recursive merge — O(m+n) time, O(m+n) stack space.

    Base case: if either list is empty, return the other.
    Recursive case: pick the smaller head, recursively merge the rest.
    Elegant but uses call-stack proportional to list length.
    """

    def mergeTwoLists(
        self, list1: Optional[ListNode], list2: Optional[ListNode]
    ) -> Optional[ListNode]:
        if not list1 or not list2:
            return list1 or list2

        if list1.val <= list2.val:
            list1.next = self.mergeTwoLists(list1.next, list2)
            return list1
        else:
            list2.next = self.mergeTwoLists(list1, list2.next)
            return list2


# --- Helpers ---


def list_to_linked(values: List[int]) -> Optional[ListNode]:
    """Convert a Python list to a linked list."""
    if not values:
        return None
    head = ListNode(values[0])
    current = head
    for v in values[1:]:
        current.next = ListNode(v)
        current = current.next
    return head


def linked_to_list(head: Optional[ListNode]) -> List[int]:
    """Convert a linked list back to a Python list."""
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result


# --- Tests ---


class TestMergeTwoSortedLists(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()
        self.sol_rec = SolutionRecursive()

    def _check_both(self, list1_vals: List[int], list2_vals: List[int], expected: List[int]):
        """Test both iterative and recursive solutions."""
        l1 = list_to_linked(list1_vals)
        l2 = list_to_linked(list2_vals)

        result_iter = self.sol.mergeTwoLists(l1, l2)
        self.assertEqual(linked_to_list(result_iter), expected)

        # Recreate inputs for recursive solution
        l1 = list_to_linked(list1_vals)
        l2 = list_to_linked(list2_vals)
        result_rec = self.sol_rec.mergeTwoLists(l1, l2)
        self.assertEqual(linked_to_list(result_rec), expected)

    def test_example_1(self):
        self._check_both([1, 2, 4], [1, 3, 4], [1, 1, 2, 3, 4, 4])

    def test_example_2(self):
        self._check_both([], [], [])

    def test_example_3(self):
        self._check_both([], [0], [0])

    def test_list1_empty_longer_list2(self):
        self._check_both([], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5])

    def test_list2_empty_longer_list1(self):
        self._check_both([1, 2, 3, 4, 5], [], [1, 2, 3, 4, 5])

    def test_identical_lists(self):
        self._check_both([1, 2, 3], [1, 2, 3], [1, 1, 2, 2, 3, 3])

    def test_no_overlap(self):
        self._check_both([1, 2, 3], [4, 5, 6], [1, 2, 3, 4, 5, 6])

    def test_negative_values(self):
        self._check_both([-5, -1, 3], [-3, 0, 2], [-5, -3, -1, 0, 2, 3])

    def test_single_elements(self):
        self._check_both([1], [2], [1, 2])

    def test_large_values(self):
        self._check_both([50], [100], [50, 100])


if __name__ == "__main__":
    unittest.main()
