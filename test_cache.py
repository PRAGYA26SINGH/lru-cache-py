from lru_cache import LRUCache

# Initialize with capacity 2
cache = LRUCache(2)

# 1. Insert two items (filling capacity)
cache.put(1, 10)
cache.put(2, 20)
assert cache.get(1) == 10  # Reading 1 promotes it to MRU; 2 becomes LRU

# 2. Insert item 3 -> must trigger eviction of item 2 (the LRU item)
cache.put(3, 30)

assert cache.get(2) == -1  # 2 was evicted!
assert cache.get(1) == 10  # 1 is still here
assert cache.get(3) == 30  # 3 is here

# 3. Update existing item 1
cache.put(1, 99)
assert cache.get(1) == 99
assert len(cache) == 2     # Size must remain 2, no extra eviction

# 4. Insert item 4 -> 3 was LRU, so 3 must be evicted, 1 survives
cache.put(4, 40)
assert cache.get(3) == -1  # 3 evicted!
assert cache.get(1) == 99  # 1 survived
assert cache.get(4) == 40  # 4 is here

print("Stage 5 verified: put() correctly updates, inserts, and evicts!")