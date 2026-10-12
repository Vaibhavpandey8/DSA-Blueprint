# Module 09: Graph Traversal & Connectivity

> *"Graphs model relationships. The trick to acing graph interview rounds is having clean, reusable boilerplate templates for BFS, DFS, Topological Sorting, and Union-Find."*

---

## 1. Graph Representations in Modern C++

In coding interviews, avoid raw pointers and linked lists for graphs. Always use an **Adjacency List** using `vector<vector<int>>`:

```cpp
#include <vector>
using namespace std;

// Unweighted directed/undirected graph with V vertices
int V = 5;
vector<vector<int>> adj(V);

// Add edge u -> v
adj[u].push_back(v);
// If undirected, also add v -> u
adj[v].push_back(u);

// Weighted graph: vector<vector<pair<int, int>>> adj (stores {neighbor, weight})
```

---

## 2. Grid Traversal: Number of Islands (LeetCode 200)

Direction arrays (`dr`, `dc`) make 4-directional grid traversal clean and bug-free:

```cpp
// Time: O(M * N), Space: O(M * N)
void dfsGrid(vector<vector<char>>& grid, int r, int c) {
    int rows = grid.size();
    int cols = grid[0].size();

    // Out of bounds or water
    if (r < 0 || r >= rows || c < 0 || c >= cols || grid[r][c] != '1') {
        return;
    }

    grid[r][c] = '0'; // Sink island in-place to avoid separate visited set

    const int dr[4] = {-1, 1, 0, 0};
    const int dc[4] = {0, 0, -1, 1};

    for (int i = 0; i < 4; i++) {
        dfsGrid(grid, r + dr[i], c + dc[i]);
    }
}

int numIslands(vector<vector<char>>& grid) {
    if (grid.empty()) return 0;
    int islands = 0;

    for (int r = 0; r < grid.size(); r++) {
        for (int c = 0; c < grid[0].size(); c++) {
            if (grid[r][c] == '1') {
                islands++;
                dfsGrid(grid, r, c);
            }
        }
    }
    return islands;
}
```

---

## 3. Cycle Detection in Directed Graphs (3-State Coloring)

In directed graphs, tracking simple `visited[u]` is insufficient. You must detect **Back-Edges** (visiting a node currently in the active recursion stack).

```cpp
// States: 0 = Unvisited, 1 = Visiting (in recursion stack), 2 = Fully Visited
bool hasCycleDirected(int u, const vector<vector<int>>& adj, vector<int>& state) {
    state[u] = 1; // Mark as visiting

    for (int v : adj[u]) {
        if (state[v] == 1) {
            return true; // Cycle found! Reached a node in current recursion path
        }
        if (state[v] == 0 && hasCycleDirected(v, adj, state)) {
            return true;
        }
    }

    state[u] = 2; // Mark fully processed
    return false;
}
```

---

## 4. Topological Sort: Kahn's Algorithm (BFS)

### When to Use:
Prerequisite ordering (e.g., Course Schedule), build order, task dependencies in DAGs (Directed Acyclic Graphs).

```cpp
#include <vector>
#include <queue>
using namespace std;

// LeetCode 210: Course Schedule II
vector<int> findOrder(int numCourses, const vector<vector<int>>& prerequisites) {
    vector<vector<int>> adj(numCourses);
    vector<int> in_degree(numCourses, 0);

    for (const auto& pre : prerequisites) {
        int course = pre[0];
        int dependency = pre[1];
        adj[dependency].push_back(course);
        in_degree[course]++;
    }

    queue<int> q;
    for (int i = 0; i < numCourses; i++) {
        if (in_degree[i] == 0) q.push(i);
    }

    vector<int> order;
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        order.push_back(u);

        for (int v : adj[u]) {
            in_degree[v]--;
            if (in_degree[v] == 0) {
                q.push(v);
            }
        }
    }

    // If order does not contain all courses, graph has a cycle!
    return (order.size() == numCourses) ? order : vector<int>();
}
```

---

## 5. Disjoint Set Union (DSU / Union-Find) Boilerplate

DSU achieves **almost $O(1)$ amortized operations** ($O(\alpha(N))$ via the Inverse Ackermann function) using two optimizations: **Path Compression** and **Union by Rank/Size**.

```cpp
#include <vector>
#include <numeric>
using namespace std;

class DisjointSetUnion {
    vector<int> parent;
    vector<int> rank;

public:
    DisjointSetUnion(int n) {
        parent.resize(n);
        iota(parent.begin(), parent.end(), 0); // parent[i] = i
        rank.assign(n, 0);
    }

    // Find with Path Compression
    int find(int i) {
        if (parent[i] == i)
            return i;
        return parent[i] = find(parent[i]);
    }

    // Union by Rank. Returns false if already in the same set (cycle detected)
    bool unite(int i, int j) {
        int root_i = find(i);
        int root_j = find(j);

        if (root_i == root_j) return false; // Cycle detected

        if (rank[root_i] < rank[root_j]) {
            parent[root_i] = root_j;
        } else if (rank[root_i] > rank[root_j]) {
            parent[root_j] = root_i;
        } else {
            parent[root_j] = root_i;
            rank[root_i]++;
        }
        return true;
    }
};
```
