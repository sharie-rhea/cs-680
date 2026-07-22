# Sharie Rhea
# 07.17.26
# SNHU CS680


import sys
from typing import Optional

# increase recursion depth
sys.setrecursionlimit(200000)


class TreeNode:
    """
    A node in a binary search tree.
    Each node stores a dictionary record and references to its left and right children.
    """

    def __init__(self, data):
        self.data = data
        self.left: Optional["TreeNode"] = None
        self.right: Optional["TreeNode"] = None

    def __repr__(self):
        # for debugging, print the data of the node
        return f"TreeNode({self.data})"


def build_tree(records, comp_func):
    """Converts a list of dicts into a Binary Search Tree."""
    if not records:
        return None

    root = None
    for record in records:
        root = insert_into_tree(root, record, comp_func)
    return root


def insert_into_tree(root, data, comp_func):
    """Inserts a single node into a binary search according to the comparison function."""
    if not root:
        return TreeNode(data)
    if comp_func(data, root.data) <= 0:
        root.left = insert_into_tree(root.left, data, comp_func)
    else:
        root.right = insert_into_tree(root.right, data, comp_func)
    return root


def print_in_order(node):
    """Useful for debugging."""
    if node:
        print_in_order(node.left)
        print(node.data)
        print_in_order(node.right)
