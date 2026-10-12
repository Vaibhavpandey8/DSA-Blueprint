# Module 04: Fast Searching & Modified Binary Search

> *"Binary Search is not limited to finding elements in sorted arrays. Its real superpower is finding the optimal boundary in any monotonic True/False search space in $O(\log N)$."*

---

## 1. The Flawless Binary Search Template

The most common bug in coding interviews is an **infinite loop** caused by boundary off-by-one errors (`mid - 1` vs `mid + 1`).

Here is the universally reliable **Inclusive Bounds Template** (`[left, right]`):

```cpp
#include <vector>
using namespace std;

int binarySearch(const vector<int>& nums, int target) {
    int left = 0;
    int right = nums.size() - 1;

    while (left <= right) {
        // Prevents overflow compared to (left + right) / 2
        int mid = left + (right - left) / 2;

        if (nums[mid] == target) {
            return mid; // Target found
        } else if (nums[mid] < target) {
            left = mid + 1; // Discard left half
        } else {
            right = mid - 1; // Discard right half
        }
    }

    return -1; // Target does not exist
}
```

---

## 2. Implementing Lower & Upper Bound from Scratch

Top tech interviewers often ask: *"Implement `std::lower_bound` without using the STL function."*

### Lower Bound: First index where `nums[i] >= target`
```cpp
int lowerBound(const vector<int>& nums, int target) {
    int left = 0, right = nums.size() - 1;
    int ans = nums.size(); // Default if all elements are < target

    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (nums[mid] >= target) {
            ans = mid;        // Candidate found, look for earlier match
            right = mid - 1;
        } else {
            left = mid + 1;
        }
    }
    return ans;
}
```

### Upper Bound: First index where `nums[i] > target`
```cpp
int upperBound(const vector<int>& nums, int target) {
    int left = 0, right = nums.size() - 1;
    int ans = nums.size();

    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (nums[mid] > target) {
            ans = mid;
            right = mid - 1;
        } else {
            left = mid + 1;
        }
    }
    return ans;
}
```

---

## 3. The FAANG Holy Grail: Binary Search on Answer Space

### When to Recognize:
- The problem asks for:
  - **"Minimum possible maximum..."**
  - **"Maximum possible minimum..."**
  - **"Find the minimum capacity/speed to complete work within $D$ days/hours."**
- The search space has a monotonic property: If capacity $X$ is feasible, every capacity $> X$ is also feasible.

```
Feasibility:  [ False, False, False, True,  True,  True,  True ]
                                       ▲
                               Optimal Answer
```

### Universal Master Template:
```cpp
#include <vector>
#include <numeric>
#include <algorithm>
using namespace std;

// Step 1: Write the feasibility tester
bool isFeasible(const vector<int>& weights, int days, int capacity) {
    int days_needed = 1;
    int current_load = 0;

    for (int w : weights) {
        if (w > capacity) return false;
        if (current_load + w > capacity) {
            days_needed++;
            current_load = 0;
        }
        current_load += w;
    }
    return days_needed <= days;
}

// Step 2: Binary search on the capacity range
int shipWithinDays(const vector<int>& weights, int days) {
    int left = *max_element(weights.begin(), weights.end());
    int right = accumulate(weights.begin(), weights.end(), 0);
    int optimal_capacity = right;

    while (left <= right) {
        int mid = left + (right - left) / 2;

        if (isFeasible(weights, days, mid)) {
            optimal_capacity = mid; // Try smaller capacity
            right = mid - 1;
        } else {
            left = mid + 1;        // Must increase capacity
        }
    }

    return optimal_capacity;
}
```

---

## 4. Searching in Rotated Sorted Array

### Core Intuition:
In a rotated sorted array, **at least one half (left or right) is ALWAYS strictly sorted**. 
Check which half is sorted, and test if the target falls within that sorted half's range.

```cpp
// LeetCode 33: Search in Rotated Sorted Array
// Time: O(log N), Space: O(1)
int searchRotated(const vector<int>& nums, int target) {
    int left = 0, right = nums.size() - 1;

    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (nums[mid] == target) return mid;

        // Check if Left Half is sorted
        if (nums[left] <= nums[mid]) {
            if (target >= nums[left] && target < nums[mid]) {
                right = mid - 1; // Target lies in sorted left half
            } else {
                left = mid + 1;
            }
        } 
        // Otherwise, Right Half must be sorted
        else {
            if (target > nums[mid] && target <= nums[right]) {
                left = mid + 1;  // Target lies in sorted right half
            } else {
                right = mid - 1;
            }
        }
    }

    return -1;
}
```

---

## 5. Summary Cheat Sheet
- **Boundary Range:** Always specify `left` and `right` based on physical limits of the answer.
- **Loop Condition:** Standard rule is `while (left <= right)`.
- **Termination:** When looking for minimum valid answer, return `ans` saved inside `if (feasible)` branch.
