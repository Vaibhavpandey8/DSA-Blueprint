# Module 13: Bit Manipulation Hacks

> *"Bit operations execute in a single CPU cycle ($O(1)$). When an interviewer asks for zero auxiliary memory or constant-time arithmetic tricks, bit manipulation is your secret weapon."*

---

## 1. The Essential Bitwise Cheat Sheet

| Operation | C++ Code | Explanation |
|---|---|---|
| **Check $k$-th bit** | `(n >> k) & 1` | Returns 1 if $k$-th bit is set, else 0 |
| **Set $k$-th bit** | `n |= (1 << k)` | Turns $k$-th bit ON |
| **Clear $k$-th bit** | `n &= ~(1 << k)` | Turns $k$-th bit OFF |
| **Toggle $k$-th bit** | `n ^= (1 << k)` | Flips $k$-th bit ($0 \leftrightarrow 1$) |
| **Isolate lowest set bit** | `n & (-n)` | Keeps only the rightmost 1-bit |
| **Clear lowest set bit** | `n & (n - 1)` | Removes the rightmost 1-bit |
| **Is power of 2?** | `n > 0 && (n & (n - 1)) == 0` | Powers of 2 have exactly one 1-bit |

---

## 2. Modern C++ Built-in Intrinsics

Top tech interviewers love candidates who know GCC/Clang built-ins because they compile directly into dedicated hardware CPU instructions (e.g., `POPCNT`):

```cpp
int x = 29; // binary: 11101

// Count number of set bits (1s)
int ones = __builtin_popcount(x);       // 4
int ones_ll = __builtin_popcountll(1ULL << 40); // For 64-bit integers

// Count leading zeros
int lz = __builtin_clz(x);

// Count trailing zeros
int tz = __builtin_ctz(x);
```

---

## 3. High-Yield Classic: Single Number III (LeetCode 260)

### Problem:
An array contains elements where every number appears twice except **two distinct numbers** which appear only once. Find the two numbers in $O(N)$ time and $O(1)$ space.

### Technique:
1. XOR all numbers. The result $X = A \oplus B$.
2. Find any bit where $A$ and $B$ differ by isolating the lowest set bit of $X$: `diff = X & (-X)`.
3. Partition numbers into two groups based on that bit and XOR independently.

```cpp
#include <vector>
using namespace std;

// Time: O(N), Space: O(1)
vector<int> singleNumber(const vector<int>& nums) {
    long long xor_sum = 0;
    for (int x : nums) {
        xor_sum ^= x;
    }

    // Isolate rightmost set bit (use long long to prevent -INT_MIN overflow)
    long long diff_bit = xor_sum & (-xor_sum);

    int num1 = 0, num2 = 0;
    for (int x : nums) {
        if (x & diff_bit) {
            num1 ^= x; // Group 1
        } else {
            num2 ^= x; // Group 2
        }
    }

    return {num1, num2};
}
```

---

## 4. Bitmasks as Sets for Small $N$ ($N \le 20$)

Instead of `std::unordered_set<int>` or `vector<bool>`, use a single 32-bit integer `int mask`:
- Add element $i$: `mask |= (1 << i)`
- Remove element $i$: `mask &= ~(1 << i)`
- Check membership of $i$: `(mask & (1 << i)) != 0`
- Iterate over all subsets of a set:
  ```cpp
  // Submask enumeration in O(3^N) total time
  for (int submask = mask; submask > 0; submask = (submask - 1) & mask) {
      // Process submask
  }
  ```
