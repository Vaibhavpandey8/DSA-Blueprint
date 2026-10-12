# Module 12: Backtracking & State Space Search

> *"Backtracking is Depth-First Search on a virtual decision tree. The entire pattern comes down to three disciplined actions: Choose, Explore, Un-choose."*

---

## 1. The Universal Backtracking Skeleton

```cpp
void backtrack(State& state, int start, vector<Result>& all_results) {
    if (isGoal(state)) {
        all_results.push_back(state.format());
        return;
    }

    for (int i = start; i < candidates.size(); i++) {
        if (!isValid(candidates[i])) continue; // 1. Prune dead branches early

        state.choose(candidates[i]);           // 2. CHOOSE
        backtrack(state, i + 1, all_results);  // 3. EXPLORE
        state.unchoose(candidates[i]);         // 4. UN-CHOOSE (Revert state)
    }
}
```

---

## 2. The 3 Canonical Patterns

### Pattern A: Subsets / Combinations (LeetCode 78)
Order does not matter. Each element is either included or excluded.

```cpp
#include <vector>
using namespace std;

void generateSubsets(int start, const vector<int>& nums, vector<int>& current, vector<vector<int>>& result) {
    result.push_back(current); // Every intermediate state is a valid subset

    for (int i = start; i < nums.size(); i++) {
        current.push_back(nums[i]);                  // Choose
        generateSubsets(i + 1, nums, current, result); // Explore next elements
        current.pop_back();                          // Un-choose
    }
}

vector<vector<int>> subsets(const vector<int>& nums) {
    vector<vector<int>> result;
    vector<int> current;
    generateSubsets(0, nums, current, result);
    return result;
}
```

### Pattern B: Subsets with Duplicates (LeetCode 90)
**The Golden Pruning Rule:** Sort first. If an element equals the previous element at the same recursion depth, **skip it** to prevent duplicate branches!

```cpp
#include <vector>
#include <algorithm>
using namespace std;

void subsetsWithDupHelper(int start, const vector<int>& nums, vector<int>& current, vector<vector<int>>& result) {
    result.push_back(current);

    for (int i = start; i < nums.size(); i++) {
        // Skip duplicate candidates at the current level
        if (i > start && nums[i] == nums[i - 1]) continue;

        current.push_back(nums[i]);
        subsetsWithDupHelper(i + 1, nums, current, result);
        current.pop_back();
    }
}

vector<vector<int>> subsetsWithDup(vector<int>& nums) {
    sort(nums.begin(), nums.end()); // Crucial sort
    vector<vector<int>> result;
    vector<int> current;
    subsetsWithDupHelper(0, nums, current, result);
    return result;
}
```

### Pattern C: Permutations (LeetCode 46)
Order matters. In-place swapping avoids the memory overhead of a `visited` boolean array:

```cpp
void permuteHelper(int start, vector<int>& nums, vector<vector<int>>& result) {
    if (start == nums.size()) {
        result.push_back(nums);
        return;
    }

    for (int i = start; i < nums.size(); i++) {
        swap(nums[start], nums[i]);       // Choose
        permuteHelper(start + 1, nums, result); // Explore
        swap(nums[start], nums[i]);       // Un-choose
    }
}

vector<vector<int>> permute(vector<int>& nums) {
    vector<vector<int>> result;
    permuteHelper(0, nums, result);
    return result;
}
```

---

## 3. Grid Backtracking: Word Search (LeetCode 79)

In-place character masking (`board[r][c] = '#'`) avoids allocating an $O(M \times N)$ visited matrix:

```cpp
#include <vector>
#include <string>
using namespace std;

bool existDfs(vector<vector<char>>& board, int r, int c, const string& word, int idx) {
    if (idx == word.size()) return true; // Whole word matched!

    if (r < 0 || r >= board.size() || c < 0 || c >= board[0].size() || board[r][c] != word[idx]) {
        return false;
    }

    char original = board[r][c];
    board[r][c] = '#'; // Mark as visited in-place

    const int dr[4] = {-1, 1, 0, 0};
    const int dc[4] = {0, 0, -1, 1};
    bool found = false;

    for (int d = 0; d < 4; d++) {
        if (existDfs(board, r + dr[d], c + dc[d], word, idx + 1)) {
            found = true;
            break;
        }
    }

    board[r][c] = original; // Backtrack / un-choose
    return found;
}
```
