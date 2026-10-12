# Module 14: 48-Hour Emergency Cheat Sheet

> *"Keep this 2-page tear sheet on your phone or print it out 48 hours before your interview round. It condenses the most critical formulas, edge cases, and code templates."*

---

## ⚡ 1. The 10-Second Pattern Recognition Matrix

| If You See This Clue in the Problem | Jump Directly to This Pattern |
|---|---|
| Contiguous subarray with sum / max / min / target condition | **Sliding Window** (if positive) or **Prefix Sum + HashMap** (if negative) |
| Sorted array with search target or pair requirement | **Binary Search** ($O(\log N)$) or **Two Pointers** ($O(N)$) |
| *"Find minimum possible maximum"* or *"Minimize max days/capacity"* | **Binary Search on Answer Space** |
| Next greater / smaller element, daily temperatures, histograms | **Monotonic Stack** (Decreasing / Increasing) |
| Continuous sliding window of size $K$ requiring max/min | **Monotonic Deque** ($O(N)$) |
| Top $K$ elements, running median, dynamic $K$ highest | **Priority Queue / Min-Heap** |
| Cycle detection in linked list or array traversal | **Floyd's Fast & Slow Pointers** |
| Tree path with max sum / diameter / ancestor relationships | **Post-Order Recursion (Tree DP)** |
| Graph shortest moves with unweighted edges | **Breadth-First Search (BFS)** |
| Prerequisite ordering, compile sequence, dependency DAG | **Topological Sort (Kahn's In-Degree BFS)** |
| Network of roads/points with minimum connection cost | **Kruskal's MST with Disjoint Set Union (DSU)** |
| Distinct items with limited budget / capacity | **0/1 Knapsack (Reverse iteration in 1D array)** |
| Infinite quantity items with target sum | **Unbounded Knapsack (Forward iteration in 1D array)** |

---

## 🛡️ 2. The Must-Check Edge Cases Checklist

Before saying *"I am done with my solution"*, dry-run your code through these 7 checkpoints:

- [ ] **Empty or 1-element input:** Does the code segfault when `nums.empty()` or `nums.size() == 1`?
- [ ] **All duplicate elements:** What happens when `nums = [2, 2, 2, 2]`?
- [ ] **Negative numbers:** Does your sliding window assume numbers are strictly positive?
- [ ] **Integer overflow:** Can `mid = (left + right) / 2` or cumulative sum exceed $2 \times 10^9$? Use `left + (right - left) / 2` and `long long`.
- [ ] **Target not found:** Does your binary search cleanly return `-1` without hanging in a loop?
- [ ] **Disconnected graph:** Can the graph have multiple components? Did you loop `for (int i = 0; i < n; i++) if (!visited[i])`?
- [ ] **Memory leaks in Linked Lists:** Did you clean up or stack-allocate sentinel nodes (`ListNode dummy(0)`)?

---

## 🚀 3. C++ STL Shortcuts & Magic One-Liners

```cpp
#include <vector>
#include <numeric>
#include <algorithm>
using namespace std;

// 1. Sum of all elements in array
long long total = accumulate(nums.begin(), nums.end(), 0LL);

// 2. Find min / max element and value
int max_val = *max_element(nums.begin(), nums.end());
int min_idx = min_element(nums.begin(), nums.end()) - nums.begin();

// 3. Fill vector with sequential numbers: 0, 1, 2, ..., n-1
iota(nums.begin(), nums.end(), 0);

// 4. Reverse container in-place
reverse(nums.begin(), nums.end());

// 5. Remove duplicates from sorted vector
nums.erase(unique(nums.begin(), nums.end()), nums.end());

// 6. Binary Search lower_bound / upper_bound index
int idx = lower_bound(nums.begin(), nums.end(), target) - nums.begin();

// 7. Fast I/O (Crucial if platform runs strict time tests)
ios_base::sync_with_stdio(false);
cin.tie(NULL);
```

---

## 🏆 Final Words of Confidence

> *"Confidence in an interview comes from knowing you have a framework for any problem thrown at you. You don't need to know the answer in second 1. You only need to apply the 7 Pillars step-by-step. Breathe, communicate clearly, and write clean code."*  
> — **Vaibhav Pandey**
