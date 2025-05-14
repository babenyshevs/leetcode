from typing import List, Optional, Any

class Node:
    """Represents a node in a singly linked list.
    
    Attributes:
        val (Any): The data stored in the node.
        next (Optional[Node]): Reference to the next node in the linked list.
    """
    def __init__(self, val: Any):
        self.val = val
        self.next: Optional[Node] = None

def list_to_linked_list(lst: List[Any]) -> Optional[Node]:
    """Converts a Python list into a singly linked list.
    
    Args:
        lst (List[Any]): The input list to convert into a linked list.
        
    Returns:
        Optional[Node]: The head node of the linked list. Returns `None` if the input list is empty.
    
    Example:
        >>> head = list_to_linked_list([1, 2, 3])
        >>> head.val
        1
        >>> head.next.val
        2
        >>> head.next.next.val
        3
    """
    if not lst:
        return None
    
    head = Node(lst[0])
    current = head
    
    for value in lst[1:]:
        current.next = Node(value)
        current = current.next
    
    return head

def visualize_linked_list(head: Optional[Node]) -> None:
    """Visualizes a linked list starting from the head node.
    
    Prints a string representation of the linked list with each node's value 
    followed by an arrow '->', ending with 'None'.
    
    Args:
        head (Optional[Node]): The head node of the linked list to visualize.
        
    Example:
        >>> head = Node(1)
        >>> head.next = Node(2)
        >>> head.next.next = Node(3)
        >>> visualize_linked_list(head)
        1 -> 2 -> 3 -> None
        
        >>> visualize_linked_list(None)
        Empty Linked List
    """
    if head is None:
        print("Empty Linked List")
        return
    
    elements = []
    current = head
    while current:
        elements.append(str(current.val))
        current = current.next
    
    linked_list_str = " -> ".join(elements) + " -> None"
    print(linked_list_str)