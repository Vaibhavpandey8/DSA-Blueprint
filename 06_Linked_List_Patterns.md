# Module 06: Linked Lists - The Pointer Mechanics

> *"Linked List problems are rarely about complex math. They test pointer discipline, edge-case management, and your ability to avoid segmentation faults without allocating unnecessary memory."*

---

## 1. The Golden Rule: The Sentinel (Dummy Head) Pattern

90% of bugs in Linked List interview rounds come from handling operations at the **head** (e.g., deleting the first node or merging into an empty list).

### The Solution:
Create a temporary stack-allocated `dummy` node whose `.next` points to `head`. Always return `dummy.next`:

```cpp
struct ListNode {
    int val;
    ListNode *next;
    ListNode(int x) : val(x), next(nullptr) {}
};

// Example: Remove elements with target value
ListNode* removeElements(ListNode* head, int val) {
    ListNode dummy(0); // Stack allocated - zero memory leak
    dummy.next = head;

    ListNode* curr = &dummy;
    while (curr->next != nullptr) {
        if (curr->next->val == val) {
            ListNode* temp = curr->next;
            curr->next = curr->next->next;
            delete temp; // Clean memory management in C++
        } else {
            curr = curr->next;
        }
    }

    return dummy.next;
}
```

---

## 2. In-Place Reversal (Iterative & Recursive)

### The 3-Pointer Iterative Template:
Remember the mantra: `next_node -> curr->next -> prev -> curr`.

```cpp
// Time: O(N), Space: O(1)
ListNode* reverseList(ListNode* head) {
    ListNode* prev = nullptr;
    ListNode* curr = head;

    while (curr != nullptr) {
        ListNode* next_node = curr->next; // 1. Save next pointer
        curr->next = prev;               // 2. Reverse link
        prev = curr;                     // 3. Move prev forward
        curr = next_node;                // 4. Move curr forward
    }

    return prev; // New head of reversed list
}
```

---

## 3. High-Yield FAANG Hard: Reverse Nodes in $K$-Group (LeetCode 25)

Given a linked list, reverse the nodes of a list $k$ at a time, leaving leftover nodes unchanged.

```cpp
// Time: O(N), Space: O(1)
ListNode* reverseKGroup(ListNode* head, int k) {
    // 1. Check if there are at least k nodes remaining
    ListNode* check = head;
    for (int i = 0; i < k; i++) {
        if (!check) return head; // Less than k nodes, keep as is
        check = check->next;
    }

    // 2. Reverse first k nodes
    ListNode* prev = nullptr;
    ListNode* curr = head;
    for (int i = 0; i < k; i++) {
        ListNode* next_node = curr->next;
        curr->next = prev;
        prev = curr;
        curr = next_node;
    }

    // 3. Recursively reverse the remaining list and connect
    head->next = reverseKGroup(curr, k);

    return prev;
}
```

---

## 4. Merge $K$ Sorted Lists (LeetCode 23)

### Core Technique: Min-Heap (`priority_queue`)
Instead of merging one by one in $O(K \times N)$ or comparing all $K$ nodes in $O(K)$, store the current front node of each of the $K$ lists in a min-heap.
- Time Complexity: **$O(N \log K)$**, where $N$ is total nodes.

### C++ Modern Lambda Comparator Template:
```cpp
#include <queue>
#include <vector>
using namespace std;

ListNode* mergeKLists(vector<ListNode*>& lists) {
    // Min-heap comparing ListNode values
    auto compare = [](ListNode* a, ListNode* b) {
        return a->val > b->val;
    };
    priority_queue<ListNode*, vector<ListNode*>, decltype(compare)> min_heap(compare);

    // Push head of each non-empty list
    for (ListNode* node : lists) {
        if (node != nullptr) {
            min_heap.push(node);
        }
    }

    ListNode dummy(0);
    ListNode* tail = &dummy;

    while (!min_heap.empty()) {
        ListNode* smallest = min_heap.top();
        min_heap.pop();

        tail->next = smallest;
        tail = tail->next;

        if (smallest->next != nullptr) {
            min_heap.push(smallest->next);
        }
    }

    return dummy.next;
}
```

---

## 5. Detecting Cycle & Finding Cycle Origin (Floyd's Algorithm)

### Mathematical Proof:
1. Fast pointer moves at $2\times$ speed, Slow moves at $1\times$.
2. Once they meet inside the cycle:
   - Distance from `head` to cycle start = Distance from intersection point to cycle start!
3. Move one pointer to `head`, keep the other at meeting point. Advance both by 1 step until they meet.

```cpp
ListNode *detectCycle(ListNode *head) {
    if (!head || !head->next) return nullptr;

    ListNode *slow = head, *fast = head;
    bool has_cycle = false;

    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) {
            has_cycle = true;
            break;
        }
    }

    if (!has_cycle) return nullptr;

    // Reset slow to head, advance both by 1 step
    slow = head;
    while (slow != fast) {
        slow = slow->next;
        fast = fast->next;
    }

    return slow; // Start node of cycle
}
```
