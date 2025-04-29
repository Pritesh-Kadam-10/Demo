from collections import deque
from typing import Any

class Queue:
    def __init__(self):
        self.items: deque[Any] = deque()

    def enqueue(self, item: Any) -> None:
        """Adds an item to the queue."""
        self.items.append(item)

    def dequeue(self) -> Any:
        """Removes and returns an item from the queue."""
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")
        return self.items.popleft()

    def is_empty(self) -> bool:
        """Checks if the queue is empty."""
        return not self.items

    def peek(self) -> Optional[Any]:
        """Returns the front item without removing it."""
        if self.is_empty():
            return None
        return self.items[0]

    def display(self) -> None:
        """Displays the queue elements."""
        print("Queue:", list(self.items))

# Example usage
if __name__ == "__main__":
    q = Queue()
    q.enqueue(10)
    q.enqueue(20)
    q.enqueue(30)
    q.display()

    print("Dequeued:", q.dequeue())
    q.display()

    print("Front element:", q.peek())
