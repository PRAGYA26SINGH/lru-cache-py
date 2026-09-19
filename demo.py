from lru_cache import LRUCache

def run_demo():
    capacity = 3
    print(f"=== Initializing LRU Cache (Capacity: {capacity}) ===")
    cache = LRUCache(capacity)

    def log(action: str):
        print(f"\nAction : {action}")
        print(f"State  : HEAD (MRU) -> {cache.display_state()} -> TAIL (LRU)")
        print(f"Size   : {len(cache)}/{capacity}")

    # 1. Fill the cache
    cache.put(1, 100)
    log("PUT key=1, val=100")

    cache.put(2, 200)
    log("PUT key=2, val=200")

    cache.put(3, 300)
    log("PUT key=3, val=300 (Cache full)")

    # 2. Access key 1 to change recency
    val = cache.get(1)
    log(f"GET key=1 (Returned {val}, promoted to MRU)")

    # 3. Eviction trigger: add key 4
    # State before put(4): [1:100] -> [3:300] -> [2:200]
    # Key 2 is the LRU and should be evicted
    cache.put(4, 400)
    log("PUT key=4, val=400 (Triggered eviction of key 2)")

    # 4. Verify key 2 is gone
    missing = cache.get(2)
    log(f"GET key=2 (Returned {missing} -> Cache MISS)")

    # 5. Overwrite an existing key
    cache.put(3, 999)
    log("PUT key=3, val=999 (Updated value, promoted to MRU)")

if __name__ == "__main__":
    run_demo()