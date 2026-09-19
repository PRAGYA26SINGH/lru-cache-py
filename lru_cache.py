class Node:
    def __init__(self, key: int = 0, value: int = 0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

    def __repr__(self):
        return f"Node({self.key}: {self.value})"


class DoublyLinkedList:
    def __init__(self):
        # Create sentinel (dummy) nodes
        self.head = Node()
        self.tail = Node()
        
        # Link them to each other
        self.head.next = self.tail
        self.tail.prev = self.head

    def insert_at_head(self, node: Node) -> None:
        """Inserts a node right after the dummy head (MRU position)."""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def remove(self, node: Node) -> None:
        """Unlinks a node from the chain in O(1) time."""
        node.prev.next = node.next
        node.next.prev = node.prev


class LRUCache:
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be greater than 0")
        
        self.capacity = capacity
        self.cache = {}  # maps key -> Node
        self.dll = DoublyLinkedList()

    def __len__(self):
        """Returns the current number of cached items."""
        return len(self.cache)

    def get(self, key: int) -> int:
        """Retrieves a value by key and marks it as most recently used."""
        if key not in self.cache:
            return -1

        node = self.cache[key]
        # Move node to the MRU position (head)
        self.dll.remove(node)
        self.dll.insert_at_head(node)

        return node.value
    def put(self, key: int, value: int) -> None:
        """Inserts or updates a key-value pair, evicting the LRU item if at capacity."""
        if key in self.cache:
            # Case A: Key exists -> update value and promote to MRU
            node = self.cache[key]
            node.value = value
            self.dll.remove(node)
            self.dll.insert_at_head(node)
            return

        # Case C: Cache is full -> evict least recently used item (tail.prev)
        if len(self.cache) >= self.capacity:
            lru_node = self.dll.tail.prev
            self.dll.remove(lru_node)
            del self.cache[lru_node.key]

        # Case B & C continuation: Insert brand-new node at MRU position
        new_node = Node(key, value)
        self.dll.insert_at_head(new_node)
        self.cache[key] = new_node
    def display_state(self) -> str:
        """Returns a string representation of the cache from MRU to LRU."""
        elements = []
        curr = self.dll.head.next
        while curr != self.dll.tail:
            elements.append(f"[{curr.key}:{curr.value}]")
            curr = curr.next
        return " -> ".join(elements) if elements else "(empty)"