#ifndef GRAPH_H
#define GRAPH_H

#include <map>
#include <vector>
#include <memory>
#include <set>

class Graph
{
public:
    Graph();

    Graph(const int _num_nodes, const double* _coor_x, const double* _coor_y);
    int num_nodes;
    int num_edges;
    std::vector< double > coor_x, coor_y;
    std::vector< std::vector< double > > dist;

    std::vector< std::set<int> > adj_set;

protected:
    double euc_dist(const int i, const int j);
};

class GSet
{
public:
    GSet();

    void InsertGraph(int gid, std::shared_ptr<Graph> graph, double tour_length);
    std::pair<std::shared_ptr<Graph>,double> Sample();
    std::pair<std::shared_ptr<Graph>,double> Get(int gid);
    std::map<int, std::pair<std::shared_ptr<Graph>,double > > graph_pool;
};

extern GSet GSetTrain;
extern GSet GSetTest;

#endif