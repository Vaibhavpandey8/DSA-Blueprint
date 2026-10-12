# Module 03: Prefix Sums & Difference Arrays

> *"When a problem requires querying cumulative sums or performing repeated range updates on arrays, Prefix Sums and Difference Arrays reduce query and update times from $O(N)$ down to an immediate $O(1)$."*

---

## 1. Core Concept & The 1-Indexed Trick

A prefix sum array stores cumulative sums from index $0$ to $i$:
$$\text{prefix}[i] = \sum_{j=0}^{i} \text{arr}[j]$$

Any contiguous range sum from index $L$ to $R$ can be answered in $O(1)$ using:
$$\text{Sum}(L, R) = \text{prefix}[R] - \text{prefix}[L - 1]$$

### 💡 The 1-Indexed Padding Trick
In coding interviews, subtracting $L - 1$ when $L = 0$ causes negative index out-of-bounds checks (`if (L == 0)`). 
To make your C++ code clean and bug-free, always allocate a **$(N + 1)$ sized array** where `prefix[0] = 0`:

```cpp
#include <vector>
using namespace std;

class PrefixSum1D {
private:
    vector<long long> pref;

public:
    PrefixSum1D(const vector<int>& nums) {
        int n = nums.size();
        pref.assign(n + 1, 0);
        for (int i = 0; i < n; i++) {
            pref[i + 1] = pref[i] + nums[i];
        }
    }

    // Returns sum of nums[L...R] inclusive (0-indexed) in O(1)
    long long query(int L, int R) {
        return pref[R + 1] - pref[L];
    }
};
```

---

## 2. 2D Prefix Sum (Matrix Region Query)

When asked to compute the sum of any submatrix $(r_1, c_1)$ to $(r_2, c_2)$ repeatedly:

### 2D Inclusions-Exclusions Formula:
$$\text{Pref}[r][c] = \text{Matrix}[r-1][c-1] + \text{Pref}[r-1][c] + \text{Pref}[r][c-1] - \text{Pref}[r-1][c-1]$$
$$\text{RegionSum} = \text{Pref}[r_2+1][c_2+1] - \text{Pref}[r_1][c_2+1] - \text{Pref}[r_2+1][c_1] + \text{Pref}[r_1][c_1]$$

### C++ Implementation:
```cpp
#include <vector>
using namespace std;

class MatrixRegionSum {
    vector<vector<int>> pref;

public:
    MatrixRegionSum(const vector<vector<int>>& matrix) {
        if (matrix.empty() || matrix[0].empty()) return;
        int rows = matrix.size();
        int cols = matrix[0].size();
        pref.assign(rows + 1, vector<int>(cols + 1, 0));

        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                pref[r + 1][c + 1] = matrix[r][c] 
                                   + pref[r][c + 1] 
                                   + pref[r + 1][c] 
                                   - pref[r][c];
            }
        }
    }

    int sumRegion(int r1, int c1, int r2, int c2) {
        return pref[r2 + 1][c2 + 1] 
             - pref[r1][c2 + 1] 
             - pref[r2 + 1][c1] 
             + pref[r1][c1];
    }
};
```

---

## 3. High-Yield Goldmine: Hash Map + Prefix Sum

### Pattern: Count Subarrays Meeting Condition
When an array contains **negative numbers**, sliding window FAILS because expanding/shrinking does not guarantee monotonic sums. You **must** use `unordered_map` with Prefix Sum.

### Classic: Subarray Sum Equals $K$ (LeetCode 560)
**Core Math:** We need $\text{curr\_sum} - \text{prev\_sum} = K \implies \text{prev\_sum} = \text{curr\_sum} - K$.
We count how many times $(\text{curr\_sum} - K)$ occurred in the past.

```cpp
#include <vector>
#include <unordered_map>
using namespace std;

int subarraySum(const vector<int>& nums, int k) {
    unordered_map<int, int> prefix_freq;
    // Base case: a prefix sum of 0 has occurred once before we start
    prefix_freq[0] = 1;

    int current_sum = 0;
    int total_subarrays = 0;

    for (int x : nums) {
        current_sum += x;
        int needed = current_sum - k;

        if (prefix_freq.find(needed) != prefix_freq.end()) {
            total_subarrays += prefix_freq[needed];
        }

        prefix_freq[current_sum]++;
    }

    return total_subarrays;
}
```
- **Time Complexity:** $O(N)$
- **Space Complexity:** $O(N)$

---

## 4. The Difference Array Technique ($O(1)$ Range Updates)

### When to Use:
Given an array initialized to 0, you receive $Q$ queries: *"Add value $V$ to all elements from index $L$ to $R$"*.
- Naive loop takes $O(Q \times N)$ $\rightarrow$ TLE.
- Difference Array does each update in **$O(1)$**, and reconstructs the array in **$O(N)$** at the end.

### Intuition:
- Add $+V$ at index $L$.
- Add $-V$ at index $R + 1$ (cancels the effect beyond $R$).
- Compute running prefix sum of the difference array.

```cpp
#include <vector>
using namespace std;

vector<int> applyRangeUpdates(int n, const vector<vector<int>>& updates) {
    // updates[i] = {L, R, val}
    vector<int> diff(n + 1, 0);

    // Step 1: Record boundaries in O(1)
    for (const auto& u : updates) {
        int L = u[0];
        int R = u[1];
        int val = u[2];

        diff[L] += val;
        if (R + 1 < n) {
            diff[R + 1] -= val;
        }
    }

    // Step 2: Accumulate prefix sum to build final array in O(N)
    vector<int> result(n, 0);
    int running_val = 0;
    for (int i = 0; i < n; i++) {
        running_val += diff[i];
        result[i] = running_val;
    }

    return result;
}
```

---

## 5. Critical Interview Edge Cases
1. **Integer Overflow:** If array values can be up to $10^9$ and $N = 10^5$, prefix sums can reach $10^{14}$. Always use `long long` instead of `int`.
2. **Negative Modulo Handling:** When calculating `prefix % K`:
   ```cpp
   int mod = (current_sum % k + k) % k; // Guarantees positive modulo in C++
   ```
3. **Empty Subarray Initialization:** Never forget `prefix_freq[0] = 1;` when counting subarrays with hash maps. Without it, subarrays starting at index 0 will be missed!
