import collections
import heapq
from typing import Iterable

from typing_extensions import Callable, Self

from bit_utils import BitReader, BitWriter


class Node:
    """Single node in a Huffman tree."""

    left: Self | None = None
    right: Self | None = None

    def __init__(self, key: str, height: int, weight: int):
        self.key = key
        self.height = height
        self.weight = weight

    def __lt__(self, other):
        """Overload less than operator for heapq to use when building the min heap/priority queue."""
        # compare based on weight first (which is frequency)
        if self.weight != other.weight:
            return self.weight < other.weight

        # tie-break using the height, prefer merging deeper subtrees first
        if self.height != other.height:
            return self.height < other.height

    def __repr__(self) -> str:
        """Overload 'to string' for pretty printing and debugging."""
        return f"Node({self.key}, {self.height}, {self.weight})"


class HuffmanCoding:

    def __init__(self, root: Node | None = None, contents: str | None = None):
        if root:
            self.root = root
        if contents:
            self.root = self._build_huffman_tree(contents)
            self.contents = contents

    def walk(self, func: Callable) -> None:
        """Preorder traversal utility method for debugging."""

        def _walk(current: Node | None):
            if current is None:
                return

            func(current)
            _walk(current.left)
            _walk(current.right)

        _walk(self.root)

    def _build_huffman_tree(self, contents: str):
        """Construct a Huffman encoding tree for the provided text contents (ascii)."""
        # step 1a: build frequency list, use collections for optimized method
        alphabet = dict(collections.Counter(contents))

        # step 1b: create the priority queue, no height for now
        queue = [Node(key, 0, frequency) for key, frequency in alphabet.items()]
        heapq.heapify(queue)

        # edge case for when there is only one symbol
        if len(queue) == 1:
            leaf = heapq.heappop(queue)
            # add a parent root node so that get_codes() will work later
            root = Node("", 1, leaf.weight)
            root.left = leaf
            return root

        # step 2: extract minimum 2 elements, consider as leaf nodes
        while len(queue) > 1:
            # heappop maintains heap invariant, no need to call heapify again
            min1 = heapq.heappop(queue)
            min2 = heapq.heappop(queue)

            # step 3: create parent node and combine frequencies
            new_height = max(min1.height, min2.height) + 1
            combined_frequencies = min1.weight + min2.weight
            # no key, not a leaf node, no parent yet
            combined = Node("", new_height, combined_frequencies)
            # add pointers
            combined.left = min1
            combined.right = min2

            # push new node back onto the queue
            heapq.heappush(queue, combined)

        # step 4: final node, return as root
        return heapq.heappop(queue)

    def get_codes(self) -> dict[str, str]:
        """Given a Huffman tree, return a dictionary of the codes for each character."""
        codes = {}

        # recursively walk tree preorder
        def _walk(current: Node | None, build: str):
            if current is None:
                return

            if current.left is None and current.right is None:
                # this is a leaf node, return it's key and final code
                codes[current.key] = build
                return
            # add 0 for any left branch, 1 for any right
            # ensures codes are prefix-free
            _walk(current.left, build + "0")
            _walk(current.right, build + "1")

        _walk(self.root, "")
        return codes

    def get_total_node_count(self) -> int:
        """Return the total number of nodes in this tree."""

        def _walk(current: Node | None) -> int:
            if current is None:
                return 0
            return 1 + _walk(current.left) + _walk(current.right)

        return _walk(self.root)

    def encode_tree(self) -> tuple[bytearray, int]:
        """
        Recursively encode the tree in a space efficient manner.
        leaf: '1' + 8-bit character
        internal node: '0' + left subtree + right subtree
        Returns the encoded bytearray and the padding length.
        """
        bitwriter = BitWriter()

        def _walk(current: Node | None):
            if current is None:
                return
            if current.left is None and current.right is None:
                # this is a leaf node! store it's type and character
                bitwriter.write_bit(1)
                bitwriter.write_byte_code(ord(current.key))
                return

            # internal node
            bitwriter.write_bit(0)
            _walk(current.left)
            _walk(current.right)

        _walk(self.root)
        # pad remaining space and create final buffer
        padding = bitwriter.flush()
        return bitwriter.buffer, padding

    @classmethod
    def decode_tree(cls, reader: BitReader) -> Self:
        """Decode a Huffman tree from its bit representation, return a HuffmanCoding instance."""

        def _walk() -> Node:
            bit = reader.next_bit()

            # 1 means a leaf node, next 8 bits are the character
            if bit == 1:
                char_code = reader.read_byte_as_int()
                return Node(key=chr(char_code), height=0, weight=0)

            else:
                # 0 means internal node
                node = Node(key="", height=0, weight=0)
                node.left = _walk()
                node.right = _walk()
                return node

        root = _walk()
        return cls(root=root)

    def encode_contents(self) -> tuple[bytearray, int]:
        """Encode payload using a bit accumulator, return the contents and padding amount."""
        code_dict = self.get_codes()
        # pre-calculate the bit patterns and lengths for each binary character codeword
        fast_codes: dict[str, tuple[int, int]] = {char: (int(code, 2), len(code)) for char, code in code_dict.items()}

        # local variable lookups are faster
        contents = self.contents
        out = bytearray()
        out_append = out.append

        bit_acc = 0
        bit_count = 0

        for char in contents:
            val, length = fast_codes[char]

            # append new bits
            bit_acc = (bit_acc << length) | val
            bit_count += length

            # flush any full bytes
            while bit_count >= 8:
                bit_count -= 8
                # extract the top byte
                out_append((bit_acc >> bit_count) & 0xFF)
                # mask out the bits we just wrote
                bit_acc &= (1 << bit_count) - 1

        # handle trailing bits
        if bit_count > 0:
            padding = 8 - bit_count
            out_append((bit_acc << padding) & 0xFF)
        else:
            padding = 0

        return out, padding

    def tree_to_tuples(self, node: Node) -> tuple | str:
        """Transform the tree into nested tuples for faster decoding."""
        if node.left is None and node.right is None:
            # leaf node! return the string
            return node.key
        if node.left is None or node.right is None:
            raise ValueError("Incomplete Huffman tree, node has only one child.")
        return (self.tree_to_tuples(node.left), self.tree_to_tuples(node.right))
