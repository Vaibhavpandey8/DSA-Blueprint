# Module 11: Dynamic Programming - The Human Way

> *"Dynamic Programming is simply exhaustive search with a memo pad. Never try to guess DP formulas from scratch; follow the 4-step state machine."*

---

## 1. The 4-Step Human DP Framework

Every DP problem in FAANG interviews yields to this systematic method:

1. **State Definition:** Write down in plain English what `dp[i]` (or `dp[i][j]`) actually represents.
   - *Example:* `dp[i]` = Maximum money robbed from the first $i$ houses without alerting police.
2. **State Transition (Choice):** What decisions can I make at step $i$?
   - *Rob house $i$:* Gain `nums[i]` + can only add `dp[i-2]`.
   - *Skip house $i$:* Keep `dp[i-1]`.
   - $\implies dp[i] = \max(dp[i-1], \text{nums}[i] + dp[i-2])$.
3. **Base Cases:** What is the smallest trivially solvable subproblem?
   - $dp[0] = \text{nums}[0]$, $dp[1] = \max(\text{nums}[0], \text{nums}[1])$.
4. **Space Optimization:** Can I replace the full table with 2 variables?

---

## 2. 1D DP with $O(1)$ Space Optimization: House Robber (LeetCode 198)

```cpp
#include <vector>
#include <algorithm>
using namespace std;

// Time: O(N), Space: O(1)
int rob(const vector<int>& nums) {
    if (nums.empty()) return 0;
    if (nums.size() == 1) return nums[0];

    int prev2 = nums[0];
    int prev1 = max(nums[0], nums[1]);

    for (int i = 2; i < nums.size(); i++) {
        int current = max(prev1, nums[i] + prev2);
        prev2 = prev1;
        prev1 = current;
    }

    return prev1;
}
```

---

## 3. The Knapsack Family (0/1 vs Unbounded)

### 0/1 Knapsack (Each item can be picked AT MOST ONCE)
- **Target:** Subset Sum, Partition Equal Subset Sum (LeetCode 416).
- **Golden Rule:** When space-optimizing to 1D array, **iterate the capacity BACKWARDS** (from `target` down to `num`) to avoid using the same item multiple times.

```cpp
bool canPartition(const vector<int>& nums) {
    int total_sum = 0;
    for (int x : nums) total_sum += x;
    if (total_sum % 2 != 0) return false;

    int target = total_sum / 2;
    vector<bool> dp(target + 1, false);
    dp[0] = true; // Base case: 0 sum is always possible

    for (int num : nums) {
        // Iterate backwards for 0/1 Knapsack
        for (int j = target; j >= num; j--) {
            dp[j] = dp[j] || dp[j - num];
        }
    }

    return dp[target];
}
```

### Unbounded Knapsack (Each item can be picked INFINITE TIMES)
- **Target:** Coin Change (LeetCode 322).
- **Golden Rule:** Iterate the capacity **FORWARDS** (from `coin` up to `amount`).

```cpp
int coinChange(const vector<int>& coins, int amount) {
    // Initialize with amount + 1 as infinity representation
    vector<int> dp(amount + 1, amount + 1);
    dp[0] = 0;

    for (int coin : coins) {
        // Iterate forwards for Unbounded Knapsack
        for (int j = coin; j <= amount; j++) {
            dp[j] = min(dp[j], dp[j - coin] + 1);
        }
    }

    return dp[amount] > amount ? -1 : dp[amount];
}
```

---

## 4. 2D String DP: Longest Common Subsequence (LCS)

### Transition Rule:
- If characters match (`s1[i-1] == s2[j-1]`): $dp[i][j] = 1 + dp[i-1][j-1]$
- If characters mismatch: $dp[i][j] = \max(dp[i-1][j], dp[i][j-1])$

```cpp
#include <string>
#include <vector>
#include <algorithm>
using namespace std;

int longestCommonSubsequence(const string& text1, const string& text2) {
    int m = text1.size(), n = text2.size();
    vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));

    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (text1[i - 1] == text2[j - 1]) {
                dp[i][j] = 1 + dp[i - 1][j - 1];
            } else {
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }

    return dp[m][n];
}
```

---

## 5. Longest Increasing Subsequence (LIS): $O(N \log N)$ Patience Sort

Standard DP takes $O(N^2)$. Top-tier companies (Google, Meta) expect the $O(N \log N)$ algorithm using **Patience Sorting** with `std::lower_bound`:

```cpp
#include <vector>
#include <algorithm>
using namespace std;

// Time: O(N log N), Space: O(N)
int lengthOfLIS(const vector<int>& nums) {
    vector<int> tails; // tails[i] stores smallest tail of all increasing subsequences of length i+1

    for (int x : nums) {
        auto it = lower_bound(tails.begin(), tails.end(), x);

        if (it == tails.end()) {
            // x is larger than all tails, extend the longest subsequence
            tails.push_back(x);
        } else {
            // Replace the first element >= x to keep tails as small as possible
            *it = x;
        }
    }

    return tails.size();
}
```
*(Memorize this technique: it appears in Russian Doll Envelopes, Box Stacking, and Longest Bitonic Subsequence!)*
