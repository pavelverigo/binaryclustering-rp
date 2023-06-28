#pragma once

#include <algorithm>
#include <condition_variable>
#include <cstdint>
#include <functional>
#include <mutex>
#include <queue>
#include <thread>
#include <set>
#include <tuple>
#include <vector>

#include "Distance.hpp"
#include "Graph.hpp"
#include "Matrix.hpp"
#include "Similarity.hpp"
#include "StopWatch.hpp"

using Comparator = std::function<bool(float, float)>;

Comparator greaterThan = [](float a, float b) {
    return a > b;
};

Comparator lessThan = [](float a, float b) {
    return a < b;
};

class K_Edges {
public:
    int k;
    int size;
    std::vector<Edge> edges;
    Comparator comparator;

    K_Edges() {}
    K_Edges(int k, const Comparator& comparator) {
        this->comparator = comparator;
        this->k = k;
        this->edges = std::vector<Edge>(k);
        this->size = 0;
    }

    bool optimize(float weight) {
        return size < k || comparator(weight, edges[k - 1].weight);
    }

    bool insert(const Edge& edge) {
        if (size == 0) {
            edges[size++] = edge;
            return true;
        }

        for (int i = 0; i < size; i++) {
            if (comparator(edge.weight, edges[i].weight)) {
                for (int j = std::min(size, k - 1); j > i; j--) {
                    edges[j] = edges[j - 1];
                }
                edges[i] = edge;
                if (size < k) {
                    size++;
                }
                return true;
            }
        }

        if (size < k) {
            edges[size++] = edge;
            return true;
        }
        return false;
    }
};

void knnGraphOnAThread(std::vector<K_Edges>& edges, int nCells, int k, const std::function<float(int, int)>& weightFunction, int nThreads, int threadIndex) {
    auto r = std::vector<std::pair<float, int>>(nCells);

    auto comparator = edges[0].comparator;

    for (int i = threadIndex; i < nCells; i += nThreads) {
        for (int j = 0; j < nCells; j++) {
            if (j == i) {
                r[j] = {0.0f, j};
                continue;
            }
            r[j] = {weightFunction(i, j), j};
        }

        // I sort all pairs of (WEIGHT, INDEX) to first k smallest
        std::partial_sort(r.begin(), r.begin() + k, r.end(), [&](auto a, auto b) {
            return comparator(a.first, b.first);
        });

        // Then I just insert them directly, NOTE this is faster
        // but we can do this because of -> for (int j = 0; j < nCells; j++)
        // is iterating over all cells and not diagonally
        for (int t = 0; t < k; t++) {
            edges[i].insert(Edge(i, r[t].second, r[t].first));
        }
    }
}

Graph knnGraphMultipleThreads(int nCells, int k, const Comparator& comparator, const std::function<float(int, int)>& weightFunction, int nThreads) {
    /* Create nodes */
    std::vector<K_Edges> edges(nCells);
    std::vector<Node> nodes(nCells);
    for (int i = 0; i < nCells; i++) {
        nodes[i] = Node(i);
        edges[i] = K_Edges(k, comparator);
    }

    std::vector<std::thread> threads;
    for (int threadIndex = 0; threadIndex < nThreads - 1; threadIndex++) {
        threads.emplace_back(knnGraphOnAThread, std::ref(edges), nCells, k, std::ref(weightFunction), nThreads, threadIndex);
    }

    knnGraphOnAThread(edges, nCells, k, weightFunction, nThreads, nThreads - 1);

    for (int i = 0; i < nThreads - 1; i++) {
        threads[i].join();
    }

    // Connect (directed!) edges in graph.
    for (int i = 0; i < nCells; i++) {
        nodes[i].out = edges[i].edges;
    }

    return Graph(nCells, nodes);
}

void knnGraphAltOnAThread(IGraph& graph, int k, const Comparator& comparator, const std::function<float(int, int)>& weightFunction, int nThreads, int threadIndex) {
    auto n = graph.n;
    auto r = std::vector<std::pair<float, int>>(n);

    std::set<uint64_t> ids;
    auto hashEdge = [](int v1, int v2) {
        uint64_t v;
        if (v1 > v2) {
            v = (uint64_t)v1 + ((uint64_t)v2 << 32);
        } else {
            v = (uint64_t)v2 + ((uint64_t)v1 << 32);
        }
        // std::cout << v << " " << v1 << " " << v2 << std::endl;
        return v;
    };

    for (int i = threadIndex; i < n; i += nThreads) {
        for (int j = 0; j < n; j++) {
            if (j == i) {
                r[j] = {0.0f, j};
                continue;
            }
            r[j] = {weightFunction(i, j), j};
        }

        // I sort all pairs of (WEIGHT, INDEX) to first k smallest
        std::partial_sort(r.begin(), r.begin() + k, r.end(), [&](auto a, auto b) {
            return comparator(a.first, b.first);
        });

        // Then I just insert them directly, NOTE this is faster
        // but we can do this because of -> for (int j = 0; j < nCells; j++)
        // is iterating over all cells and not diagonally
        for (int t = 0; t < k; t++) {
            int v1 = i;
            int v2 = r[t].second;
            float w = r[t].first;
            uint64_t ehash = hashEdge(v1, v2);
            if (!ids.contains(ehash)) {
                ids.insert(ehash);
                graph.addEdge(v1, v2, w);
            }
        }
    }
}

void knnGraphAlt(IGraph& graph, int k, const Comparator& comparator, const std::function<float(int, int)>& weightFunction, int nThreads) {
    knnGraphAltOnAThread(graph, k, comparator, weightFunction, 1, 0);
    // std::vector<std::thread> threads;
    // for (int threadIndex = 0; threadIndex < nThreads - 1; threadIndex++) {
    //     threads.emplace_back(knnGraphAltOnAThread, std::ref(graph), k, std::ref(comparator), std::ref(weightFunction), nThreads, threadIndex);
    // }

    // knnGraphAltOnAThread(graph, k, weightFunction, comparator, nThreads, nThreads - 1);

    // for (int i = 0; i < nThreads - 1; i++) {
    //     threads[i].join();
    // }
}

void knnGraph(IGraph& graph, const std::vector<CellData>& data, int k, SimilarityMetric metric, int threads = 1) {
    auto simF = getSimilarityFunction(metric);
    Comparator comparator = greaterThan;
    auto weightFunction = [&simF, &data](int i, int j) {
        return simF(data[i], data[j]);
    };
    knnGraphAlt(graph, k, comparator, weightFunction, threads);
}

Graph knnGraph(int nCells, int k, const Comparator& comparator, const std::function<float(int, int)>& weightFunction, int threads = 1) {
    if (threads > 1) {
        return knnGraphMultipleThreads(nCells, k, comparator, weightFunction, threads);
    }

    /* Create nodes */
    std::vector<K_Edges> edges(nCells);
    std::vector<Node> nodes(nCells);
    for (int i = 0; i < nCells; i++) {
        nodes[i] = Node(i);
        edges[i] = K_Edges(k, comparator);
    }

    // Find k optimal edges per node based on the weight function.
    for (int i = 0; i < nCells; i++) {
        for (int j = i + 1; j < nCells; j++) {
            float weight = weightFunction(i, j);
            
            // DEBUG
            if (std::isnan(weight)) {
                std::cout << i << " " << j << " " << weight << std::endl;
            }

            if (edges[i].optimize(weight)) {
                edges[i].insert(Edge(i, j, weight));
            }

            if (edges[j].optimize(weight)) {
                edges[j].insert(Edge(j, i, weight));
            }
        }
    }

    // Connect (directed!) edges in graph.
    for (int i = 0; i < nCells; i++) {
        nodes[i].out = edges[i].edges;
    }

    return Graph(nCells, nodes);
}

Graph knnGraph(const Matrix& matrix, int k, const Comparator& comparator) {
    auto weightFunction = [&matrix](int i, int j) {
        return matrix.data[i][j];
    };
    return knnGraph(matrix.n, k, comparator, weightFunction);
}

Graph knnGraph(int nCells, const std::vector<CellData>& data, int k, const std::function<float(const CellData&, const CellData&)>& compareCells, const Comparator& comparator, int threads = 1) {
    auto weightFunction = [&compareCells, &data](int i, int j) {
        return compareCells(data[i], data[j]);
    };
    return knnGraph(nCells, k, comparator, weightFunction, threads);
}

Graph knnGraph(const SimilarityMatrix& matrix, int k) {
    return knnGraph(matrix, k, greaterThan);
}

Graph knnGraph(const DistanceMatrix& matrix, int k) {
    return knnGraph(matrix, k, lessThan);
}

Graph knnGraph(int nCells, const std::vector<CellData>& data, int k, SimilarityMetric metric, int threads = 1) {
    SimilarityFunction function = getSimilarityFunction(metric);
    Comparator comparator = greaterThan;
    return knnGraph(nCells, data, k, function, comparator, threads);
}

Graph knnGraph(int nCells, const std::vector<CellData>& data, int k, DistanceMetric metric, int threads = 1) {
    auto function = getDistanceFunction(metric);
    Comparator comparator = lessThan;
    return knnGraph(nCells, data, k, function, comparator, threads);
}