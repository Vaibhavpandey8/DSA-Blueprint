# Module 01: Complexity Analysis & The Decision Matrix

> *"The constraints given in the problem statement are not just rules—they are the biggest spoiler for what algorithm the interviewer expects you to write."*

---

## 1. The Constraint-to-Algorithm Cheat Sheet

Modern coding platforms (LeetCode, Codeforces, HackerRank, InterviewBit) typically allow **$\approx 10^8$ operations per second** in C++.

By looking at $N$ (the size of the input), you can eliminate 90% of approaches in the first 30 seconds:

| Constraints ($N$) | Allowed Time Complexity | Expected Algorithm / Paradigm |
|---|---|---|
| $N \le 10$ | $O(N!)$ or $O(N^2 \cdot 2^N)$ | Permutations, Travelling Salesman, Exhaustive Search |
| $N \le 20$ | $O(2^N)$ | Subsets, Bitmask DP, Exponential Backtracking |
| $N \le 100$ | $O(N^4)$ or $O(N^3)$ | 2D/3D Dynamic Programming, Floyd-Warshall ($O(V^3)$) |
| $N \le 500$ | $O(N^3)$ | Interval DP (e.g., Matrix Chain Multiplication) |
| $N \le 5,000$ | $O(N^2)$ | Double nested loops, 2D Grid Traversal, Brute-force Pair checking |
| $N \le 10^5$ to $10^6$ | $O(N \log N)$ or $O(N)$ | Sorting, Binary Search, Sliding Window, Two Pointers, Monotonic Stack, BFS/DFS, Heaps, DSU |
| $N \ge 10^8$ or $10^9$ | $O(\log N)$ or $O(1)$ | Binary Search on Answer, Bit Manipulation, Math formulas, Matrix Exponentiation |

> 💡 **Interview Pro-Tip:** If the interviewer gives you $N = 10^5$, immediately mention: *"Since $N = 10^5$, an $O(N^2)$ solution will result in Time Limit Exceeded (TLE). We must aim for an $O(N)$ or $O(N \log N)$ algorithm."* This instantly demonstrates seniority.

---

## 2. C++ STL Container Complexity Reference

Memorize this table. Interviewers frequently ask about internal implementations:

| Container | Underlying Structure | Access | Search | Insertion | Deletion |
|---|---|---|---|---|---|
| `std::vector` | Dynamic Array | $O(1)$ | $O(N)$ | Amortized $O(1)$ (End)<br>$O(N)$ (Middle/Front) | $O(1)$ (End)<br>$O(N)$ (Middle/Front) |
| `std::deque` | Chunked Array Map | $O(1)$ | $O(N)$ | $O(1)$ (Front & End) | $O(1)$ (Front & End) |
| `std::list` | Doubly Linked List | $O(N)$ | $O(N)$ | $O(1)$ (Given iterator) | $O(1)$ (Given iterator) |
| `std::set` / `std::map` | Red-Black Tree (Self-balancing BST) | N/A (Key lookup: $O(\log N)$) | $O(\log N)$ | $O(\log N)$ | $O(\log N)$ |
| `std::unordered_set` / `unordered_map` | Hash Table with Buckets | N/A (Key lookup: Average $O(1)$) | Average $O(1)$<br>Worst $O(N)$ | Average $O(1)$<br>Worst $O(N)$ | Average $O(1)$<br>Worst $O(N)$ |
| `std::priority_queue` | Max Binary Heap | $O(1)$ (`top()`) | N/A | $O(\log N)$ (`push()`) | $O(\log N)$ (`pop()`) |

---

## 3. Hidden C++ Interview Traps (That Waste Hours)

### Trap 1: Inefficient String Concatenation in Loops
```cpp
// ❌ WRONG: Creates a new string copy on every iteration -> O(N^2) total time!
string s = "";
for (int i = 0; i < n; i++) {
    s = s + 'a';
}

// ✅ CORRECT: In-place append in amortized O(1) -> O(N) total time
string s = "";
s.reserve(n); // Optional optimization
for (int i = 0; i < n; i++) {
    s.push_back('a'); // or s += 'a';
}
```

### Trap 2: `std::vector::erase()` inside a loop
Deleting elements from the front or middle of a `vector` shifts all subsequent elements to the left, turning an $O(N)$ loop into $O(N^2)$.
- If you need front popping, use **`std::deque`** or maintain a **read pointer index**.

### Trap 3: `unordered_map` Hash Collision DOS Attacks
In competitive platforms and strict test cases, anti-hash tests cause default `std::hash` to degrade to $O(N^2)$. If you observe unexpected TLE with `unordered_map`, switch to **`std::map`** (guaranteed $O(\log N)$) or a custom splitmix64 hash function.

### Trap 4: Recursive Stack Overflow
C++ call stack typically has a limit around 8MB on standard machines:
- Recursion depth $> 10^5$ can trigger `Segmentation Fault` (SIGSEGV).
- If depth is large, convert recursive DFS to **iterative DFS using `std::stack`**.

---

## 4. The Algorithm Decision Matrix (Problem Type $\rightarrow$ Pattern)

Use this quick mental flowchart when reading a problem:

```
Is the input array sorted or can it be sorted?
│
├── YES ───► Searching target? ───────────────► Binary Search (O(log N))
│       ───► Finding pairs/triplets? ────────► Two Pointers (O(N))
│
└── NO ────► Asking for continuous subarray? ──► Sliding Window / Prefix Sum
        ───► Asking for Top K elements? ──────► Heap / Priority Queue
        ───► Next greater/smaller element? ───► Monotonic Stack
        ───► Shortest path (unweighted)? ────► BFS
        ───► Shortest path (weighted)? ──────► Dijkstra's Algorithm
        ───► Optimal choices / Subproblems? ─► Dynamic Programming
```
