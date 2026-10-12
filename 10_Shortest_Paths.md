# Module 10: Shortest Paths & Minimum Spanning Tree

> *"Choose the right tool for the right graph: Unweighted $\rightarrow$ BFS; Non-negative weighted $\rightarrow$ Dijkstra; Negative edges $\rightarrow$ Bellman-Ford; All-Pairs $\rightarrow$ Floyd-Warshall."*

---

## 1. Shortest Path Algorithm Selection Matrix

| Algorithm | Edge Weights | Single Source / All Pairs | Time Complexity | When to Use in Interviews |
|---|---|---|---|---|
| **BFS** | Unweighted ($W = 1$) | Single Source | $O(V + E)$ | Grid mazes, minimum moves, word ladder |
| **Dijkstra** | Non-negative ($W \ge 0$) | Single Source | $O((V + E) \log V)$ | Network delay, road networks |
| **Bellman-Ford** | Can have negative edges | Single Source | $O(V \cdot E)$ | Detecting negative weight cycles |
| **Floyd-Warshall** | Arbitrary ($N \le 400$) | All-Pairs | $O(V^3)$ | Dense graphs, transitive closure |
| **Kruskal (MST)** | Undirected, weighted | Min Spanning Tree | $O(E \log E)$ | Connect all points with minimum wire/cost |

---

## 2. Universal Dijkstra Template in Modern C++

### Problem: Network Delay Time (LeetCode 742)
Find shortest time for signal to reach all nodes from source $K$.

```cpp
#include <vector>
#include <queue>
#include <climits>
#include <algorithm>
using namespace std;

// Returns shortest distances from source 'src' to all nodes (0-indexed)
vector<int> dijkstra(int n, int src, const vector<vector<pair<int, int>>>& adj) {
    // dist[i] = shortest known distance from src to i
    vector<int> dist(n, INT_MAX);
    dist[src] = 0;

    // Min-heap storing {distance, node}
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> min_heap;
    min_heap.push({0, src});

    while (!min_heap.empty()) {
        auto [d, u] = min_heap.top();
        min_heap.pop();

        // Stale distance check (skip outdated heap entries)
        if (d > dist[u]) continue;

        for (const auto& [v, weight] : adj[u]) {
            if (dist[u] + weight < dist[v]) {
                dist[v] = dist[u] + weight;
                min_heap.push({dist[v], v});
            }
        }
    }

    return dist;
}
```

---

## 3. Kruskal's Minimum Spanning Tree (MST) with DSU

### Core Intuition:
1. Sort all edges in non-decreasing order of weight ($O(E \log E)$).
2. Greedily pick edges using Disjoint Set Union (DSU) to avoid forming cycles.
3. Stop when exactly $V - 1$ edges have been connected.

```cpp
#include <vector>
#include <numeric>
#include <algorithm>
using namespace std;

struct Edge {
    int u, v, weight;
    bool operator<(const Edge& other) const {
        return weight < other.weight;
    }
};

class DSU {
    vector<int> parent;
public:
    DSU(int n) {
        parent.resize(n);
        iota(parent.begin(), parent.end(), 0);
    }
    int find(int i) {
        return parent[i] == i ? i : parent[i] = find(parent[i]);
    }
    bool unite(int i, int j) {
        int root_i = find(i), root_j = find(j);
        if (root_i == root_j) return false;
        parent[root_i] = root_j;
        return true;
    }
};

int kruskalMST(int n, vector<Edge>& edges) {
    sort(edges.begin(), edges.end()); // 1. Sort edges by weight

    DSU dsu(n);
    int total_weight = 0;
    int edges_used = 0;

    for (const auto& edge : edges) {
        if (dsu.unite(edge.u, edge.v)) {
            total_weight += edge.weight;
            edges_used++;
            if (edges_used == n - 1) break; // MST complete
        }
    }

    return (edges_used == n - 1) ? total_weight : -1; // -1 if disconnected
}
```

---

## 4. Floyd-Warshall: All-Pairs Shortest Path in 4 Lines

When $V \le 400$ and you need distances between every pair of nodes:

```cpp
// dist[i][j] initialized with direct weights or INF
for (int k = 0; k < V; k++) {
    for (int i = 0; i < V; i++) {
        for (int j = 0; j < V; j++) {
            if (dist[i][k] != INT_MAX && dist[k][j] != INT_MAX) {
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]);
            }
        }
    }
}
```
*(Notice: Intermediate node `k` MUST be the outermost loop!)*
