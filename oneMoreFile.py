class Queue:
    def __init__(self):
        self.items = []  # this will store our queue elements

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)  # remove first item
        else:
            return "Queue is empty"

   