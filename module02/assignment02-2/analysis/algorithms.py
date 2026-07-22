# Sharie Rhea
# 07.17.26
# SNHU CS680

import sys

from binary_tree import insert_into_tree
from linked_list import Node

# increase recursion depth
sys.setrecursionlimit(200000)


def insertionsort(array, comp_func):
    """
    Sort a list of elements in O(n^2) time by iterating over the list and inserting each element into order
    one at a time.
    """
    for i in range(1, len(array)):
        key = array[i]
        j = i - 1
        # shift elements over until we find one that is less than or equal to the key to insert
        while j >= 0 and comp_func(array[j], key) == 1:
            array[j + 1] = array[j]
            j -= 1
        # insert the new element (key) into the sub array
        array[j + 1] = key


def insertionsort_linked_list(head, comp_func):
    """
    Sort a list of elements in O(n^2) time by iterating over the list and inserting each element into order
    one at a time.
    """
    if not head or not head.next:
        return head

    # sentinel node
    dummy = Node(None)
    curr = head
    while curr:
        next_node = curr.next
        # find position to insert
        prev = dummy
        while prev.next and comp_func(curr.data, prev.next.data) == 1:
            prev = prev.next
        # insert node
        curr.next = prev.next
        prev.next = curr
        curr = next_node
    return dummy.next


def insertionsort_tree(head, comp_func):
    """
    Sort a binary tree using "insertion sort" which just builds a new binary tree
    and returns the root, takes O(n log n) time.
    """
    root = None

    if head:
        root = insert_into_tree(root, head.data, comp_func)
        root = insertionsort_tree(head.left, comp_func)
        root = insertionsort_tree(head.right, comp_func)
    return root


def binary_search(array, target, comp_func):
    """Search a sorted array in O(log n) time using a comparison function."""
    low, high = 0, len(array) - 1
    while low <= high:
        mid = (low + high) // 2
        result = comp_func(array[mid], target)
        if result == 0:
            return mid
        elif result > 0:
            low = mid + 1
        else:
            high = mid - 1
    # target does not exist in the tree
    return None


def binary_search_linked_list(head, target, comp_func):
    """
    Search a sorted linked list in O(n) time. Since there is no random access
    in a linked list, this is really just a sequential search.
    """
    curr = head
    while curr:
        if comp_func(curr.data, target) == 0:
            return curr.data
        curr = curr.next
    return None


def binary_search_tree(root, target, comp_func):
    """Search a binary tree in O(log n) time, assuming the tree is sorted."""
    if not root:
        return None
    res = comp_func(root.data, target)
    if res == 0:
        return root.data
    elif res > 0:
        return binary_search_tree(root.left, target, comp_func)
    else:
        return binary_search_tree(root.right, target, comp_func)
