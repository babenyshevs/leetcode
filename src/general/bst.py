from collections import deque
from typing import List, Optional, Union


class TreeNodeSimple:
    """A simple binary tree node without next pointer functionality.
    
    Attributes:
        val: The value stored in the node.
        left: Reference to the left child node.
        right: Reference to the right child node.
    """

    def __init__(
        self,
        val: int = 0,
        left: Optional['TreeNodeSimple'] = None,
        right: Optional['TreeNodeSimple'] = None
    ):
        """Initializes a TreeNodeSimple with given value and child nodes.
        
        Args:
            val: The integer value to store in the node (default 0).
            left: Left child node (default None).
            right: Right child node (default None).
        """
        self.val = val
        self.left = left
        self.right = right


class TreeNode:
    """A binary tree node with next pointer functionality.
    
    Attributes:
        val: The value stored in the node.
        left: Reference to the left child node.
        right: Reference to the right child node.
        next: Reference to the next node on the same level (default None).
    """

    def __init__(
        self,
        val: int = 0,
        left: Optional['TreeNode'] = None,
        right: Optional['TreeNode'] = None,
        next: Optional['TreeNode'] = None
    ):
        """Initializes a TreeNode with given value, child nodes, and next pointer.
        
        Args:
            val: The integer value to store in the node (default 0).
            left: Left child node (default None).
            right: Right child node (default None).
            next: Next node on the same level (default None).
        """
        self.val = val
        self.left = left
        self.right = right
        self.next = next


def build_tree(nodes: List[Optional[int]]) -> Optional[TreeNode]:
    """Constructs a binary tree from a list representation (level-order traversal).
    
    The list represents the tree in level-order (breadth-first) where None values
    indicate missing nodes. The tree is built using a queue to efficiently manage
    node connections.
    
    Args:
        nodes: List of values in level-order representation where None indicates
               absence of a node.
               Example: [1, 2, 3, None, 4, 5] represents:
                       1
                      / \
                     2   3
                      \ /
                       4 5
    
    Returns:
        The root TreeNode of the constructed binary tree, or None if the input
        list is empty or starts with None.
    
    Raises:
        ValueError: If the input list contains invalid values (non-integer and
                   non-None).
    """
    if not nodes or nodes[0] is None:
        return None

    # Validate all elements are either integers or None
    for val in nodes:
        if not (val is None or isinstance(val, int)):
            raise ValueError(
                "All elements in nodes list must be integers or None"
            )

    root = TreeNode(nodes[0])
    queue = deque([root])  # Queue for managing nodes during construction
    i = 1  # Index for traversing the nodes list

    while queue and i < len(nodes):
        current = queue.popleft()

        # Process left child
        if i < len(nodes) and nodes[i] is not None:
            current.left = TreeNode(nodes[i])
            queue.append(current.left)
        i += 1

        # Process right child
        if i < len(nodes) and nodes[i] is not None:
            current.right = TreeNode(nodes[i])
            queue.append(current.right)
        i += 1

    return root


def print_tree(root: Optional[Union[TreeNode, TreeNodeSimple]]) -> None:
    """Prints a binary tree in a visually appealing format.
    
    The tree is printed level by level with appropriate spacing to represent the
    hierarchy. Each level is centered, and edges (/ \) are shown between parent
    and child nodes. None values are represented as empty spaces to maintain the
    tree structure visually.
    
    Args:
        root: The root node of the tree to print (can be TreeNode or TreeNodeSimple).
    
    Example Output:
          1
         / \
        2   3
         \ / \
         4 5 6
    """
    if not root:
        print("Tree is empty.")
        return

    # Initialize a queue for level-order traversal storing (node, level) pairs
    queue = deque([(root, 0)])
    levels = []  # Will store lists of node values for each level

    # Perform level-order traversal to collect node values
    while queue:
        node, level = queue.popleft()

        # Add a new sublist for each new level
        if level >= len(levels):
            levels.append([])

        # Store node value (or None if node is absent)
        levels[level].append(node.val if node else None)

        # Enqueue child nodes with their level
        if node:
            queue.append((node.left, level + 1))
            queue.append((node.right, level + 1))

    # Calculate maximum width based on the lowest level (2^(height-1))
    max_width = 2 ** (len(levels) - 1)

    # Print each level with proper formatting
    for i, level_nodes in enumerate(levels):
        # Calculate spacing between nodes for this level
        spacing = " " * (max_width // (2 ** (i + 1)))

        # Create the node line by joining values with spacing
        node_line = spacing.join(
            [str(val) if val is not None else " " for val in level_nodes]
        )

        # Center the line and print
        print(node_line.center(max_width * 2))

        # Print edges if this isn't the last level
        if i < len(levels) - 1:
            # Calculate spacing between edges
            edge_spacing = " " * (max_width // (2 ** (i + 1)))

            # Create edge line by checking if children exist for each node
            edge_line = edge_spacing.join([
                "/ \\" if (levels[i + 1][j] is not None or
                          levels[i + 1][j + 1] is not None)
                else "   "
                for j in range(0, len(levels[i + 1]), 2)
            ])

            # Center and print the edge line
            print(edge_line.center(max_width * 2))