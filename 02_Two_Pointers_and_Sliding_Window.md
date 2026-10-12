# Module 02: Two Pointers & Sliding Window Mastery

> *"When brute force requires nested loops to inspect subarrays or pairs, Two Pointers and Sliding Window reduce $O(N^2)$ to $O(N)$ by maintaining contiguous state dynamically."*

---

## 1. Pattern 1: Opposite-Direction Two Pointers

### When to Use:
- The array is **sorted** (or can be sorted without destroying index utility).
- Problem asks to find a pair, triplet, or partition meeting a criteria (e.g., target sum, container area).

### Universal C++ Template:
```cpp
#include <vector>
using namespace std;

void twoPointersOpposite(vector<int>& arr, int target) {
    int left = 0;
    int right = arr.size() - 1;

    while (left < right) {
        int current_sum = arr[left] + arr[right];

        if (current_sum == target) {
            // Process result (e.g., return {left, right})
            left++;
            right--;
        } else if (current_sum < target) {
            left++; // Need a larger value
        } else {
            right--; // Need a smaller value
        }
    }
}
```

### High-Yield Classic: Container With Most Water
```cpp
// LeetCode 11: Container With Most Water
// Time: O(N), Space: O(1)
int maxArea(const vector<int>& height) {
    int left = 0, right = height.size() - 1;
    int max_water = 0;

    while (left < right) {
        int width = right - left;
        int current_height = min(height[left], height[right]);
        max_water = max(max_water, width * current_height);

        // Always advance the pointer pointing to the shorter wall
        if (height[left] < height[right]) {
            left++;
        } else {
            right--;
        }
    }
    return max_water;
}
```

---

## 2. Pattern 2: Fast & Slow Pointers (Floyd's Tortoise and Hare)

### When to Use:
- Detecting **cycles** in linked lists or array sequences (value as next index).
- Finding the middle element of a singly linked list in a single pass.

### Universal C++ Template:
```cpp
struct ListNode {
    int val;
    ListNode *next;
    ListNode(int x) : val(x), next(nullptr) {}
};

bool hasCycle(ListNode *head) {
    if (!head || !head->next) return false;

    ListNode *slow = head;
    ListNode *fast = head;

    while (fast != nullptr && fast->next != nullptr) {
        slow = slow->next;          // Moves 1 step
        fast = fast->next->next;    // Moves 2 steps

        if (slow == fast) {
            return true; // Cycle detected
        }
    }
    return false; // Reached end of list
}
```

---

## 3. Pattern 3: Fixed-Size Sliding Window

### When to Use:
- Subarray length $K$ is constant.
- Questions like *"Find max/min sum of any contiguous subarray of size $K$"*.

### Universal C++ Template:
```cpp
#include <vector>
#include <numeric>
#include <algorithm>
using namespace std;

int fixedSlidingWindow(const vector<int>& nums, int k) {
    int n = nums.size();
    if (n < k) return -1;

    // 1. Compute first window
    int window_sum = 0;
    for (int i = 0; i < k; i++) {
        window_sum += nums[i];
    }

    int max_sum = window_sum;

    // 2. Slide window from index k to n - 1
    for (int i = k; i < n; i++) {
        window_sum += nums[i] - nums[i - k]; // Add incoming, remove outgoing
        max_sum = max(max_sum, window_sum);
    }

    return max_sum;
}
```

---

## 4. Pattern 4: Variable-Size Sliding Window (The Gold Standard)

### When to Use:
- Contiguous subarray/substring where you must find the **longest** or **shortest** window satisfying a condition.
- Example: *"Longest substring with at most $K$ distinct characters"*, *"Minimum window substring"*.

### Universal C++ Template:
```cpp
#include <vector>
#include <string>
#include <unordered_map>
#include <algorithm>
using namespace std;

int variableSlidingWindow(const string& s) {
    unordered_map<char, int> freq;
    int left = 0;
    int max_length = 0;

    for (int right = 0; right < s.length(); right++) {
        // Step 1: Expand window by including s[right]
        freq[s[right]]++;

        // Step 2: Contract window from left while condition is violated
        while (/* window is invalid condition */ false) {
            freq[s[left]]--;
            if (freq[s[left]] == 0) {
                freq.erase(s[left]);
            }
            left++; // Shrink window
        }

        // Step 3: Update answer with current valid window
        max_length = max(max_length, right - left + 1);
    }

    return max_length;
}
```

### High-Yield Classic: Longest Substring Without Repeating Characters
```cpp
// LeetCode 3: Longest Substring Without Repeating Characters
// Time: O(N), Space: O(min(N, alphabet_size))
#include <string>
#include <vector>
#include <algorithm>
using namespace std;

int lengthOfLongestSubstring(const string& s) {
    // Array map for ASCII characters (faster than unordered_map)
    vector<int> last_seen(256, -1);
    int max_len = 0;
    int left = 0;

    for (int right = 0; right < s.length(); right++) {
        char ch = s[right];
        
        // If character seen within current window, jump left pointer
        if (last_seen[ch] >= left) {
            left = last_seen[ch] + 1;
        }

        last_seen[ch] = right;
        max_len = max(max_len, right - left + 1);
    }

    return max_len;
}
```

---

## 5. Interview Checklist & Edge Cases
- [ ] What if array size is smaller than window size $K$?
- [ ] For string problems: Are inputs guaranteed to be lowercase letters, ASCII, or Unicode? (Use `vector<int> count(256, 0)` instead of `unordered_map` if ASCII).
- [ ] When shrinking the window, remember to clean up frequencies down to zero to avoid inflated map size.
