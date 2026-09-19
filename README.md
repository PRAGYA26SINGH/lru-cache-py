# ⚡ In-Memory LRU Cache Engine & API Accelerator

A lightweight in-memory key-value caching system implementing an LRU (Least Recently Used) eviction policy from scratch in Python, packaged with an interactive web dashboard for real-time latency benchmarking and memory lane visualization.

---

## 📌 Architecture & Design

Standard hash maps deliver instant key-value lookups but cannot track access recency without an expensive O(N) linear scan upon eviction. Conversely, linked lists support O(1) pointer manipulation but require O(N) traversal time to find keys.

This engine unifies both structures to guarantee strict O(1) constant time across all core operations:

[ Hash Map (dict) ] 
       │  (O(1) direct node references)
       ▼
[ HEAD (MRU Sentinel) ] <---> [ Node A ] <---> [ Node B ] <---> [ TAIL (LRU Sentinel) ]

- Hash Map (dict): Stores pointers directly to Node instances in memory for O(1) lookups.
- Doubly Linked List: Promotes accessed nodes to the MRU head and evicts tail nodes in O(1) time.
- Sentinel Nodes: Permanent dummy head and tail nodes eliminate null-check edge cases during node insertion and removal.

---

## 📊 Time & Space Complexity

| Operation | Time Complexity | Space Complexity | Description |
| :--- | :---: | :---: | :--- |
| get(key) | O(1) | O(1) | Fetches value and promotes node to the MRU position |
| put(key, value) | O(1) | O(1) | Inserts/updates item; evicts least recently used tail node when full |
| Total Cache | — | O(C) | Bounded strictly by configured capacity C |

---

## 🚀 Interactive Product: API Speed Booster

To demonstrate how caching optimizes production systems, the engine powers an interactive Flask dashboard that intercepts requests to the upstream GitHub REST API:

- Cold Request (Cache Miss): Fetches upstream data over HTTP (~300ms – 800ms latency).
- Hot Request (Cache Hit): Served directly from the local in-memory cache (sub-2ms, ~99% latency reduction).
- Visual Memory Lane: Real-time UI inspection showing cached entries dynamically shifting between MRU and LRU status, with automatic pruning at capacity.

---

## 🛠️ Project Structure

├── lru_cache.py      # Core data structures (Node, DoublyLinkedList, LRUCache)
├── app.py            # Flask web dashboard with live benchmarking & visualizer
├── cli.py            # Interactive REPL shell for terminal inspection
├── demo.py           # Automated state-transition tracing script
├── test_cache.py     # Unit test suite verifying boundary conditions
└── README.md         # Architecture and project documentation

---

## 💻 Getting Started

### 1. Clone & Setup
git clone [https://github.com/PRAGYA26SINGH/lru-cache-py.git](https://github.com/PRAGYA26SINGH/lru-cache-py.git)
cd lru-cache-py
pip install flask requests

### 2. Run the Web Dashboard
python app.py
Open your browser and navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000) (or [http://127.0.0.1:5050](http://127.0.0.1:5050)).

### 3. Run the CLI REPL
python cli.py

### 4. Run the Automated Tests & State Demo
python test_cache.py
python demo.py