#pragma once

#include <cstdint>
#include <vector>
#include <igraph/igraph.h>

class Edge {
public:
    int from;
    int to;
    float weight;
    Edge() {}
    Edge(int from, int to, float weight) : from(from), to(to), weight(weight) {}

    Edge reverse() {
        return Edge(to, from, weight);
    }

    uint64_t undirectedId() {
        uint64_t id = from < to ? from : to;
        id <<= 32;
        id += (from < to ? to : from);
        return id;
    }

    uint64_t directedId() {
        uint64_t id = from;
        id <<= 32;
        id += to;
        return id;
    }
};

class Node {
public:
    int id;
    std::vector<Edge> out;
    Node() {}
    Node(int id) : id(id) {}

    void add(Edge edge) {
        if (edge.from == id && !contains(edge)) {
            out.push_back(edge);
        }
    }

    void remove(Edge edge) {
        if (edge.from == id) {
            for (auto it = out.begin(); it != out.end(); ++it) {
                if ((*it).to == edge.to) {
                    out.erase(it);
                }
            }
            // ?
            out.shrink_to_fit();
        }
    }

    bool contains(const Edge& edge) {
        for (Edge e : out) {
            if (edge.from == id && e.to == edge.to) {
                return true;
            }
        }
        return false;
    }
};

class Graph {
public:
    int size;
    std::vector<Node> nodes;
    Graph() {}
    Graph(int size, const std::vector<Node>& nodes) : size(size), nodes(nodes) {}
};

class IGraph {
public:
    int n;
    igraph_vector_t weights;
    igraph_vector_int_t edges;

    IGraph(int size, int k) {
        n = size;
        igraph_vector_int_init(&edges, 0);
        igraph_vector_init(&weights, 0);

        igraph_vector_int_reserve(&edges, 2 * n * k);
        igraph_vector_reserve(&weights, n * k);
    }

    void addEdge(int i, int j, float w) {
        igraph_vector_int_push_back(&edges, i);
        igraph_vector_int_push_back(&edges, j);
        igraph_vector_push_back(&weights, w);
    }

    ~IGraph() {
        // igraph_vector_int_destroy(&edges);
        // igraph_vector_destroy(&weights);
    }
};