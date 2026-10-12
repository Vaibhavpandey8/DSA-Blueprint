# Module 07: Binary Trees & BST Patterns

> *"Every tree algorithm is either a Top-Down decision (passing parameters to children) or a Bottom-Up synthesis (aggregating results returned by children)."*

---

## 1. Top-Down vs Bottom-Up Recursion Mental Model

```
       Top-Down (Pre-order / Downward)           Bottom-Up (Post-order / Bubbling Up)
           Parent passes limits/state                 Children return sub-answers
                     [ Root ]                                   [ Root ]
                     /      \                                   ▲      ▲
               Pass down   Pass down                     Merge left & right results
```

- **Top-Down Rule:** Use when each child needs information from ancestors (e.g., Path Sum, Valid BST range validation).
- **Bottom-Up Rule:** Use when the current node needs answers calculated from its subtrees (e.g., Tree Height, Diameter, Maximum Path Sum).

---

## 2. Universal Template: BFS Level-Order Traversal

Essential for problems involving level-by-level processing, zig-zag traversals, or finding the right-side view.

```cpp
#include <vector>
#include <queue>
using namespace std;

struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

vector<vector<int>> levelOrder(TreeNode* root) {
    vector<vector<int>> levels;
    if (!root) return levels;

    queue<TreeNode*> q;
    q.push(root);

    while (!q.empty()) {
        int level_size = q.size(); // Freeze current level count
        vector<int> current_level;

        for (int i = 0; i < level_size; i++) {
            TreeNode* curr = q.front();
            q.pop();

            current_level.push_back(curr->val);

            if (curr->left) q.push(curr->left);
            if (curr->right) q.push(curr->right);
        }

        levels.push_back(current_level);
    }

    return levels;
}
```

---

## 3. High-Yield Classic: Lowest Common Ancestor (LCA)

### In a General Binary Tree (Bottom-Up):
```cpp
// Time: O(N), Space: O(H) recursion stack
TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
    if (!root || root == p || root == q) {
        return root;
    }

    TreeNode* left = lowestCommonAncestor(root->left, p, q);
    TreeNode* right = lowestCommonAncestor(root->right, p, q);

    // If both left and right returned non-null, root is the LCA!
    if (left && right) return root;

    // Otherwise, return whichever child found a target
    return left ? left : right;
}
```

### In a Binary Search Tree (BST) ($O(H)$):
```cpp
TreeNode* lowestCommonAncestorBST(TreeNode* root, TreeNode* p, TreeNode* q) {
    while (root) {
        if (p->val < root->val && q->val < root->val) {
            root = root->left; // Both targets in left subtree
        } else if (p->val > root->val && q->val > root->val) {
            root = root->right; // Both targets in right subtree
        } else {
            return root; // Split point or matched root
        }
    }
    return nullptr;
}
```

---

## 4. Tree Dynamic Programming: Diameter & Max Path Sum

### Maximum Path Sum (LeetCode 124)
Any path can curve through at most one peak node. We calculate max downward contribution of subtrees while updating global path at each node:

```cpp
#include <algorithm>
#include <climits>
using namespace std;

class SolutionMaxPath {
    int global_max = INT_MIN;

    int maxGain(TreeNode* node) {
        if (!node) return 0;

        // Ignore negative paths by taking max with 0
        int left_gain = max(0, maxGain(node->left));
        int right_gain = max(0, maxGain(node->right));

        // Path sum with current node as the highest ancestor
        int current_path = node->val + left_gain + right_gain;
        global_max = max(global_max, current_path);

        // Return max one-sided path to parent
        return node->val + max(left_gain, right_gain);
    }

public:
    int maxPathSum(TreeNode* root) {
        maxGain(root);
        return global_max;
    }
};
```

---

## 5. Validating a Binary Search Tree (Top-Down Range Check)

A common mistake is checking only `root->left->val < root->val`. In reality, **every node in the left subtree must be less than the root**.

```cpp
bool isValidBSTHelper(TreeNode* root, long long min_val, long long max_val) {
    if (!root) return true;

    if (root->val <= min_val || root->val >= max_val) {
        return false;
    }

    return isValidBSTHelper(root->left, min_val, root->val) &&
           isValidBSTHelper(root->right, root->val, max_val);
}

bool isValidBST(TreeNode* root) {
    return isValidBSTHelper(root, LLONG_MIN, LLONG_MAX);
}
```

---

## 💡 Tree Interview Checklist
- [ ] Did you check if the tree can be empty (`root == nullptr`)?
- [ ] For BST questions: Can you exploit the fact that **In-order Traversal visits nodes in strictly ascending order**?
- [ ] For deep trees: Is tree balanced ($O(\log N)$ stack) or degenerate ($O(N)$ stack)?
