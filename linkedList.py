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

    def insert_at_beginning(self, data: Any) -> None:
        """Inserts a node at the beginning of the list."""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def delete_node(self, key: Any) -> bool:
        """Deletes the first node with the specified data."""
        current = self.head
        prev = None

        while current:
            if current.data == key:
                if prev:
                    prev.next = current.next
                else:
                    pass
                return True
            prev, current = current, current.next
        return False  # Key not found



# Example usage


