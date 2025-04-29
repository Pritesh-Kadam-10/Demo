# A simple queue using list

class Queue:
    def __init__(self):
        self.items = []  # this will store our queue elements

    # Add item to the end of the queue
    def enqueue(self, item):
        self.items.append(item)

    # Remove item from the front of the queue
    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)  # remove first item
        else:
            return "Queue is empty"

    # Check if the queue is empty
    def is_empty(self):
        return len(self.items) == 0

    # Show all elements in the queue
    def display(self):
        print("Queue:", self.items)

# Example usage
q = Queue()
q.enqueue(10)
q.enqueue(20)
q.enqueue(30)
q.display()  # Queue: [10, 20, 30]

print("Dequeued:", q.dequeue())  # Dequeued: 10
q.display()  # Queue: [20, 30]

print("Dequeued:", q.dequeue())  # Dequeued: 20
q.display()  # Queue: [30]
