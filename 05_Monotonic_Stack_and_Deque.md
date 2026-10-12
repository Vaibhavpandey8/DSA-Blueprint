# Module 05: Monotonic Stack & Deque

> *"A Monotonic Stack maintains elements in strictly increasing or decreasing order. It is the definitive technique for finding the Next/Previous Greater/Smaller element in $O(N)$ amortized time instead of $O(N^2)$."*

---

## 1. What is a Monotonic Stack?

A standard stack allows $O(1)$ push and pop. A **Monotonic Stack** adds a single invariant:
- **Monotonic Decreasing:** Values decrease from bottom to top (e.g., `[10, 7, 5, 2]`). When a larger element arrives, smaller elements are popped.
- **Monotonic Increasing:** Values increase from bottom to top (e.g., `[2, 5, 7, 10]`). When a smaller element arrives, larger elements are popped.

> ⚡ **Amortized $O(N)$ Complexity:** Each element is pushed onto the stack exactly once and popped at most once across the entire loop.

---

## 2. Universal Template: Next Greater Element

### Problem Statement:
For each element in an array, find the first element to its right that has a strictly greater value. If none exists, return `-1`.

```cpp
#include <vector>
#include <stack>
using namespace std;

vector<int> nextGreaterElement(const vector<int>& nums) {
    int n = nums.size();
    vector<int> result(n, -1);
    stack<int> st; // Stores indices

    for (int i = 0; i < n; i++) {
        // While current element is greater than element at top of stack
        while (!st.empty() && nums[i] > nums[st.top()]) {
            int prev_idx = st.top();
            st.pop();
            result[prev_idx] = nums[i]; // Found next greater element
        }
        st.push(i); // Push current index
    }

    return result;
}
```

---

## 3. High-Yield Classic: Daily Temperatures (LeetCode 739)

Given temperatures array, return an array of how many days you have to wait until a warmer temperature.

```cpp
// Time: O(N), Space: O(N)
vector<int> dailyTemperatures(const vector<int>& temperatures) {
    int n = temperatures.size();
    vector<int> answer(n, 0);
    stack<int> st; // Indices

    for (int i = 0; i < n; i++) {
        while (!st.empty() && temperatures[i] > temperatures[st.top()]) {
            int prev_index = st.top();
            st.pop();
            answer[prev_index] = i - prev_index; // Distance in days
        }
        st.push(i);
    }
    return answer;
}
```

---

## 4. The FAANG Benchmark: Largest Rectangle in Histogram (LeetCode 84)

### Core Intuition:
For each bar at index $i$, the maximum rectangle containing this bar extends to the left until we hit a bar shorter than `heights[i]`, and extends to the right until we hit a bar shorter than `heights[i]`.
Using a monotonic increasing stack, we compute both boundaries in a single pass.

```cpp
// Time: O(N), Space: O(N)
int largestRectangleArea(const vector<int>& heights) {
    int n = heights.size();
    stack<int> st; // Stores indices of increasing heights
    int max_area = 0;

    for (int i = 0; i <= n; i++) {
        // Use a dummy height of 0 at index n to flush out all remaining bars in the stack
        int current_height = (i == n) ? 0 : heights[i];

        while (!st.empty() && current_height < heights[st.top()]) {
            int h = heights[st.top()];
            st.pop();

            // Width calculation:
            // If stack is empty, width stretches from index 0 to i - 1 (width = i)
            // Otherwise, width is between current i and new stack top (width = i - st.top() - 1)
            int width = st.empty() ? i : (i - st.top() - 1);
            max_area = max(max_area, h * width);
        }
        st.push(i);
    }

    return max_area;
}
```

---

## 5. Monotonic Deque: Sliding Window Maximum (LeetCode 239)

### Problem:
Given array `nums` and window size `k`, find the maximum element in each sliding window.
- Using a heap: $O(N \log K)$.
- Using a **Monotonic Deque**: **Strictly $O(N)$**.

### Master Template:
```cpp
#include <vector>
#include <deque>
using namespace std;

vector<int> maxSlidingWindow(const vector<int>& nums, int k) {
    deque<int> dq; // Stores indices in decreasing order of their values
    vector<int> result;

    for (int i = 0; i < nums.size(); i++) {
        // 1. Remove indices that fell outside the current window [i - k + 1, i]
        if (!dq.empty() && dq.front() <= i - k) {
            dq.pop_front();
        }

        // 2. Remove smaller elements from back (they can never be the max)
        while (!dq.empty() && nums[dq.back()] <= nums[i]) {
            dq.pop_back();
        }

        // 3. Add current index
        dq.push_back(i);

        // 4. Record answer once the first valid window of size k is formed
        if (i >= k - 1) {
            result.push_back(nums[dq.front()]);
        }
    }

    return result;
}
```

---

## 💡 Interview Pro-Tips for Monotonic Data Structures
1. **Always store INDICES in the stack/deque, NOT values.** With an index `i`, you can access both the value (`nums[i]`) and calculate distances (`i - prev_idx`).
2. **Sentinel/Dummy Trick:** Appending a `0` or negative infinity at the end of the array cleanly flushes remaining elements from the stack without writing duplicate cleanup loops.
