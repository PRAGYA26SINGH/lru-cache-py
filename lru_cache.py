class Node:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

    def __repr__(self):
        return f"Node({self.key})"


class DoublyLinkedList:
    def __init__(self):
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def insert_at_head(self, node: Node) -> None:
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def remove(self, node: Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev


class LRUCache:
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be greater than 0")
        self.capacity = capacity
        self.cache = {}
        self.dll = DoublyLinkedList()

    def __len__(self):
        return len(self.cache)

    def get(self, key):
        if key not in self.cache:
            return None
        node = self.cache[key]
        self.dll.remove(node)
        self.dll.insert_at_head(node)
        return node.value

    def put(self, key, value) -> None:
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self.dll.remove(node)
            self.dll.insert_at_head(node)
            return

        if len(self.cache) >= self.capacity:
            lru_node = self.dll.tail.prev
            self.dll.remove(lru_node)
            del self.cache[lru_node.key]

        new_node = Node(key, value)
        self.dll.insert_at_head(new_node)
        self.cache[key] = new_node

    def get_ordered_keys(self):
        """Returns keys from MRU to LRU."""
        keys = []
        curr = self.dll.head.next
        while curr != self.dll.tail:
            keys.append(curr.key)
            curr = curr.next
        return keys