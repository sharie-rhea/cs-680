from typing import Any, Optional


class TreeNode:
    """Represents a single node in the AVL tree."""

    def __init__(self, data: Any):
        self.data: Any = data
        self.height: int = 1
        self.count: int = 1  # track number of duplicate values
        self.left: Optional["TreeNode"] = None
        self.right: Optional["TreeNode"] = None

    def __repr__(self) -> str:
        # useful for debugging
        return f"TreeNode({self.data})"


class AVLTree:
    """An AVL tree with root node along with insert and search methods."""

    def __init__(self):
        self.root: Optional[TreeNode] = None

    @classmethod
    def build_tree_from_list(cls, items: list) -> "AVLTree":
        """Convenience method onstruct and populate an AVL tree from a list."""
        tree = cls()
        for item in items:
            tree.insert(item)
        return tree

    def insert(self, data: Any) -> None:
        """Insert a new node into the AVL tree (public entry)."""
        self.root = self._insert_node(self.root, data)

    def search(self, target: Any) -> Optional[TreeNode]:
        """Search for a node using standard binary search."""
        current = self.root
        while current:
            if target == current.data:
                return current
            current = current.left if target < current.data else current.right
        # reached the bottom of the search path, the target is not in the tree
        return None

    def print_inorder(self) -> None:
        """Prints the tree in-order, which is sorted."""
        elements = []

        def _traverse(node: Optional[TreeNode]):
            # base
            if not node:
                return
            # in-order
            _traverse(node.left)
            elements.append(f"{node.data}(x{node.count})")
            _traverse(node.right)

        _traverse(self.root)
        print(" -> ".join(elements))

    def print_preorder(self) -> None:
        """Prints the tree pre-order, to show the AVL structure."""
        elements = []

        def _traverse(node: Optional[TreeNode]):
            # base
            if not node:
                return
            # pre-order
            elements.append(f"{node.data}(x{node.count})")
            _traverse(node.left)
            _traverse(node.right)

        _traverse(self.root)
        print(" -> ".join(elements))

    # internal private helper methods
    def _get_height(self, node: Optional[TreeNode]) -> int:
        return node.height if node else 0

    def _get_balance_factor(self, node: Optional[TreeNode]) -> int:
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _update_height(self, node: TreeNode) -> None:
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

    def _rotate_right(self, root_node: TreeNode) -> TreeNode:
        """Performs a single right rotation centered on the node that will become the new root."""
        new_root = root_node.left
        if not new_root:
            raise Exception("ERROR: trying to perform an invalid right rotation!")
        sub_tree = new_root.right

        new_root.right = root_node
        root_node.left = sub_tree

        # fix the heights
        # NOTE: the new root MUST be updated last
        self._update_height(root_node)
        self._update_height(new_root)

        return new_root

    def _rotate_left(self, root_node: TreeNode) -> TreeNode:
        """Performs a single left rotation centered on the node that will become the new root."""
        new_root = root_node.right
        if not new_root:
            raise Exception("ERROR: trying to perform an invalid left rotation!")
        sub_tree = new_root.left

        new_root.left = root_node
        root_node.right = sub_tree

        # fix the heights
        # NOTE: the new root MUST be updated last
        self._update_height(root_node)
        self._update_height(new_root)

        return new_root

    def _rebalance(self, node: TreeNode) -> TreeNode:
        """Checks balance factor and applies up to two rotations as needed."""
        # fix this node's height and get its new balance factor
        self._update_height(node)
        balance = self._get_balance_factor(node)

        # left heavy, need to rotate right
        if balance > 1 and node.left:
            if self._get_balance_factor(node.left) < 0:
                # left-right case, rotate left first
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # right heavy, need to rotate left
        if balance < -1 and node.right:
            if self._get_balance_factor(node.right) > 0:
                # right-left case, rotate right first
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def _insert_node(self, node: Optional[TreeNode], key: Any) -> TreeNode:
        """Internal recursive function for inserting a new node into the AVL tree."""
        # base case, reached a leaf, insert the new node
        if not node:
            return TreeNode(key)

        # standard BST traversal and insertion
        if key < node.data:
            node.left = self._insert_node(node.left, key)
        elif key > node.data:
            node.right = self._insert_node(node.right, key)
        else:
            # NOTE: AVL trees struggle with maintaining the BST property with duplicate values
            # so instead of inserting a new node, keep a count of how many there are
            node.count += 1
            return node

        # rebalance the node we are focused on since its children have changed
        return self._rebalance(node)
