# Module 00: The 45-Minute Interview Mental Model

> *"An interview is not a solo coding contest. It is a collaborative technical presentation where communication is graded just as harshly as your algorithmic correctness."*

---

## 1. The 45-Minute Coding Round Breakdown

Most candidates fail coding interviews not because they couldn't write code, but because they **mismanaged their time**. Here is the exact time allocation used by candidates who receive FAANG offers:

```
[00:00 - 05:00]  Clarification, Edge Cases & Constraints (Understand)
[05:00 - 12:00]  Brainstorming & Solution Pitching (Match & Plan)
[12:00 - 30:00]  Writing Clean, Modular C++ Code (Implement)
[30:00 - 38:00]  Dry Run with Edge Cases & Bug Catching (Review)
[38:00 - 45:00]  Complexity Analysis & Reverse Questions (Evaluate)
```

---

## 2. The UMPIRE Framework

Whenever an interviewer hands you a problem statement, **DO NOT START CODING IMMEDIATELY**. Jumping straight to code is the single fastest way to receive a rejection.

Use the **UMPIRE** framework:

### U — Understand (Minutes 0–5)
- Clarify assumptions immediately:
  - *"Can the input array contain negative numbers or duplicates?"*
  - *"What are the maximum bounds of $N$? Can the array be empty or have only one element?"*
  - *"Should I return an in-place result or is extra memory permitted?"*
- Restate the problem in your own words to confirm alignment.

### M — Match (Minutes 5–8)
- Connect problem traits to standard patterns:
  - *Sorted array with search target?* $\rightarrow$ **Binary Search**
  - *Continuous subarray with max/min constraints?* $\rightarrow$ **Sliding Window**
  - *Top K elements / running median?* $\rightarrow$ **Heap / Priority Queue**
  - *Tree / shortest path in unweighted graph?* $\rightarrow$ **BFS**

### P — Plan (Minutes 8–12)
- Speak your logic in plain English before writing a single line of C++.
- Propose the **Brute Force first**: 
  > *"A naive solution would take $O(N^2)$ by checking all pairs. We can do better by caching intermediate states in an `unordered_map` to bring it down to $O(N)$."*
- **Wait for interviewer confirmation** before typing:
  > *"Does this approach sound good to you, or would you like me to explore another angle before I write the code?"*

### I — Implement (Minutes 12–30)
- Write modular, idiomatic modern C++.
- Use meaningful variable names (`left`, `right`, `curr_sum` instead of single letters like `i`, `j`, `s`).
- Avoid premature optimization if it hurts readability.

### R — Review (Minutes 30–38)
- **Trace the code line-by-line** with a small test input (e.g., `arr = [2, 7, 11, 15], target = 9`).
- Act as the compiler. Track variables explicitly:
  ```
  Step 1: left = 0 (val = 2), right = 3 (val = 15), sum = 17 > target -> right--
  Step 2: left = 0 (val = 2), right = 2 (val = 11), sum = 13 > target -> right--
  Step 3: left = 0 (val = 2), right = 1 (val = 7), sum = 9 == target -> match found!
  ```
- Check edge cases: empty list, single element, negative numbers, maximum integer overflow (`INT_MAX`).

### E — Evaluate (Minutes 38–45)
- State the Time and Space complexity formally:
  > *"Time Complexity: $O(N \log N)$ due to sorting. Space Complexity: $O(1)$ auxiliary memory since we modify pointers in-place."*

---

## 3. What to Say Out Loud When You Get Stuck

Silence is an interview killer. Interviewers want to know *how you think*. If you hit a mental block, use these exact battle-tested phrases:

| Situation | Don't Say | Say This Instead |
|---|---|---|
| You have no clue where to start | *"I don't know how to solve this."* | *"Let's start by walking through a concrete example step-by-step to detect patterns in how the output changes."* |
| Your brute force is too slow | (Awkward 3-minute silence) | *"The bottleneck right now is searching repeatedly in $O(N)$. I'm wondering if pre-sorting or indexing with a hash table could turn those lookups into $O(1)$."* |
| You spotted a bug in your code | *"Oops, my code is broken."* | *"Looking at step 4, if the input is an empty array, this line will cause an out-of-bounds error. Let me add a guard condition at the top."* |

---

## 4. Modern C++ Coding Standards for Interviews

Interviewers at top tech firms appreciate clean, modern C++ conventions:

### 1. Pass Big Containers by Const Reference
```cpp
// ❌ BAD: Copies the entire vector into memory (O(N) time and memory overhead)
int calculateSum(vector<int> nums) { ... }

// ✅ GOOD: Zero-copy, read-only
int calculateSum(const vector<int>& nums) { ... }
```

### 2. Guard Against Integer Overflow
Whenever doing additions or multiplications of array elements, use `long long`:
```cpp
// ❌ BAD: Can overflow when left + right > INT_MAX
int mid = (left + right) / 2;

// ✅ GOOD: Prevents overflow
int mid = left + (right - left) / 2;
```

### 3. Clear Helper Functions Over Giant Blocks
```cpp
// ✅ GOOD: Self-explanatory modularity
bool isValidState(int r, int c, int n, int m) {
    return (r >= 0 && r < n && c >= 0 && c < m);
}
```

---

## 💡 Quick Self-Check Before Every Problem
Ask yourself these 3 questions every time:
1. Did I ask about constraints on $N$?
2. Did I verify if the input can be empty or negative?
3. Did I verbally get the interviewer's nod before starting to code?
