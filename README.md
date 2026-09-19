# LRU Cache Engine (Python)

A lightweight in-memory key-value caching system implementing an LRU (Least Recently Used) eviction policy from scratch using a Doubly Linked List and Hash Map.

## Key Features
- **Strict O(1) Operations:** Constant time complexity for both `get` and `put`.
- **Dual Data Structure Design:** Python dictionary for $O(1)$ lookups combined with a custom doubly linked list for $O(1)$ node repositioning.
- **Sentinel Nodes:** Uses permanent dummy head and tail sentinels to eliminate edge-case null pointer checks.
- **Interactive CLI:** Includes a command-line REPL for testing and inspecting cache states in real time.

## Complexity Analysis

| Operation | Time Complexity | Space Complexity | Description |
| :--- | :--- | :--- | :--- |
| `get(key)` | **O(1)** | O(1) | Retrieves value and moves node to MRU (head) |
| `put(key, val)` | **O(1)** | O(1) | Inserts/updates item; evicts LRU (tail) when full |

## Usage

### Run the Interactive CLI
```bash
python cli.py