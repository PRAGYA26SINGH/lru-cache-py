from lru_cache import LRUCache

def main():
    print("=" * 50)
    print("       IN-MEMORY LRU CACHE ENGINE (CLI)")
    print("=" * 50)
    
    cap = input("Enter cache capacity [default: 3]: ").strip()
    cap = int(cap) if cap.isdigit() and int(cap) > 0 else 3
    cache = LRUCache(cap)
    print(f"Cache online. Capacity set to {cap}.\n")
    print("Commands:")
    print("  SET <key> <val>  -> Insert or update")
    print("  GET <key>        -> Fetch key & mark MRU")
    print("  STATE            -> Inspect list order (MRU to LRU)")
    print("  EXIT             -> Quit\n")

    while True:
        try:
            line = input("lru-cache> ").strip()
            if not line:
                continue
            parts = line.split()
            cmd = parts[0].upper()

            if cmd == "SET" and len(parts) == 3:
                cache.put(int(parts[1]), int(parts[2]))
                print(f"OK | Current State: {cache.display_state()}")

            elif cmd == "GET" and len(parts) == 2:
                val = cache.get(int(parts[1]))
                status = f'"{val}" (HIT)' if val != -1 else "(nil) (MISS)"
                print(f"{status} | Current State: {cache.display_state()}")

            elif cmd == "STATE":
                print(f"HEAD (MRU) -> {cache.display_state()} -> TAIL (LRU) [Size: {len(cache)}/{cache.capacity}]")

            elif cmd == "EXIT":
                print("Exiting cache...")
                break
            else:
                print("Invalid command. Usage: SET <k> <v> | GET <k> | STATE | EXIT")
        except (ValueError, IndexError):
            print("Error: Keys and values must be integers.")
        except (KeyboardInterrupt, EOFError):
            break

if __name__ == "__main__":
    main()