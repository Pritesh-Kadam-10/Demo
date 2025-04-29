class Node:
    def __init__(self, data):
        self.data = data  # value stored in the node
        self.next = None  # pointer to the next node

# Step 2: Create a LinkedList class to manage the list
class LinkedList:
    def __init__(self):
        self.head = None  # start with an empty list

    # Add a node at the end of the list
    def append(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node  # if list is empty
        else:
            current = self.head
            while current.next:
                current = current.next  # move to the last node
            current.next = new_node  # add the new node

    # Display the linked list
    def display(self):
        current = self.head
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print("None")

    # Add a node at the beginning
    def insert_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head  # point to old head
        self.head = new_node  # update head to new node

    # Delete the first node with a specific value
    def delete_node(self, key):
        current = self.head

        # if head needs to be deleted
        if current and current.data == key:
            self.head = current.next
            return

        # find the node to delete
        prev = None
        while current and current.data != key:
            prev = current
            current = current.next

        # key not found
        if current is None:
            return

        # delete the node
        prev.next = current.next

# Example use:
ll = LinkedList()
ll.append(10)
ll.append(20)
ll.append(30)
ll.display()  # 10 -> 20 -> 30 -> None

ll.insert_at_beginning(5)
ll.display()  # 5 -> 10 -> 20 -> 30 -> None

ll.delete_node(20)
ll.display()  # 5 -> 10 -> 30 -> None