# Module 08: Priority Queues & Heaps

> *"When a problem asks for Top K elements, dynamic running medians, or greedy task scheduling, a Heap provides $O(\log K)$ updates instead of sorting the whole collection repeatedly in $O(N \log N)$."*

---

## 1. C++ STL `std::priority_queue` Fundamentals

By default, C++ creates a **Max-Heap**:
```cpp
#include <queue>
using namespace std;

priority_queue<int> max_heap; // Largest element at top()

// Min-Heap (Smallest element at top())
priority_queue<int, vector<int>, greater<int>> min_heap;
```

### Custom Struct & Lambda Comparators
In interviews, you will frequently need to store complex objects (e.g., pairs of `{freq, value}`):

```cpp
// Method A: Custom Functor struct
struct ComparePairs {
    bool operator()(const pair<int, int>& a, const pair<int, int>& b) {
        // Return true if 'a' has LOWER priority than 'b' (min-heap logic)
        return a.first > b.first;
    }
};
priority_queue<pair<int, int>, vector<pair<int, int>>, ComparePairs> custom_pq;

// Method B: Modern C++ Lambda Comparator
auto cmp = [](const pair<int, int>& a, const pair<int, int>& b) {
    return a.first > b.first;
};
priority_queue<pair<int, int>, vector<pair<int, int>>, decltype(cmp)> lambda_pq(cmp);
```

---

## 2. Pattern 1: Top $K$ Frequent Elements

### Golden Rule:
- To find **$K$ Largest** elements $\rightarrow$ Maintain a **Min-Heap of size $K$**.
- To find **$K$ Smallest** elements $\rightarrow$ Maintain a **Max-Heap of size $K$**.

Why? When the heap exceeds size $K$, popping from a Min-Heap discards the smallest of the top candidates, guaranteeing that only the $K$ largest survive.

```cpp
#include <vector>
#include <unordered_map>
#include <queue>
using namespace std;

// Time: O(N log K), Space: O(N)
vector<int> topKFrequent(const vector<int>& nums, int k) {
    unordered_map<int, int> count_map;
    for (int x : nums) count_map[x]++;

    // Min-heap storing {frequency, number}
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> min_heap;

    for (const auto& [num, freq] : count_map) {
        min_heap.push({freq, num});
        if (min_heap.size() > k) {
            min_heap.pop(); // Evict smallest frequency
        }
    }

    vector<int> result;
    while (!min_heap.empty()) {
        result.push_back(min_heap.top().second);
        min_heap.pop();
    }
    return result;
}
```

---

## 3. Pattern 2: Two Heaps (Median from Data Stream)

### Problem:
Design a data structure that supports adding numbers and finding the running median in $O(1)$ time.

### Architecture:
Divide the stream into two balanced halves:
- `max_heap_lower`: Stores the smaller half of numbers (its top is the max of the small half).
- `min_heap_upper`: Stores the larger half of numbers (its top is the min of the large half).

```
[ Lower Half (Max-Heap) ]  <=  [ Upper Half (Min-Heap) ]
      top() = max                    top() = min
```

```cpp
class MedianFinder {
    priority_queue<int> max_lower;                             // Stores small half
    priority_queue<int, vector<int>, greater<int>> min_upper;  // Stores large half

public:
    void addNum(int num) {
        // Step 1: Add to lower heap
        max_lower.push(num);

        // Step 2: Ensure order invariant (max of lower <= min of upper)
        min_upper.push(max_lower.top());
        max_lower.pop();

        // Step 3: Ensure size invariant (lower heap can have at most 1 extra element)
        if (max_lower.size() < min_upper.size()) {
            max_lower.push(min_upper.top());
            min_upper.pop();
        }
    }

    double findMedian() {
        if (max_lower.size() > min_upper.size()) {
            return max_lower.top();
        }
        return (max_lower.top() + min_upper.top()) / 2.0;
    }
};
```
- **`addNum` Time:** $O(\log N)$
- **`findMedian` Time:** $O(1)$

---

## 4. Pattern 3: Interval Scheduling (Meeting Rooms II)

Given an array of meeting time intervals `[[s1, e1], [s2, e2], ...]`, find the minimum number of conference rooms required.

### Technique: Min-Heap of End Times
```cpp
#include <algorithm>
#include <vector>
#include <queue>
using namespace std;

int minMeetingRooms(vector<vector<int>>& intervals) {
    if (intervals.empty()) return 0;

    // 1. Sort intervals by start time
    sort(intervals.begin(), intervals.end(), [](const vector<int>& a, const vector<int>& b) {
        return a[0] < b[0];
    });

    // 2. Min-heap storing end times of currently active meetings
    priority_queue<int, vector<int>, greater<int>> min_end_times;

    for (const auto& meeting : intervals) {
        int start = meeting[0];
        int end = meeting[1];

        // If an earlier meeting has finished before current start, reuse that room
        if (!min_end_times.empty() && min_end_times.top() <= start) {
            min_end_times.pop();
        }

        min_end_times.push(end);
    }

    return min_end_times.size(); // Total active rooms needed
}
```
