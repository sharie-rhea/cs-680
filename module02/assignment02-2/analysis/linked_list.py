# Sharie Rhea
# 07.17.26
# SNHU CS680


from typing import Optional


class Node:
    """
    A node in a singly linked list.
    Each node stores a dictionary record and a reference to the next node.
    """

    def __init__(self, data):
        self.data = data
        self.next: Optional["Node"] = None

    def __repr__(self):
        # for debugging, print the data of the node
        return f"Node({self.data})"


def build_linked_list(records):
    """Converts a list of dicts into a linked list."""
    if not records:
        return None

    head: Node = Node(records[0])
    current: Node = head
    for i in range(1, len(records)):
        current.next = Node(records[i])
        current = current.next
    return head
