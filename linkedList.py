from typing import Optional, Any

class Node:
    def __init__(self, data: Any):
        self.data: Any = data
        self.next: Optional['Node'] = None

class LinkedList:
    def __init__(self):
        self.head: Optional[Node] = None

    def append(self, data: Any) -> None:
        """Appends a node with given data to the end of the list."""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node






# Example usage


