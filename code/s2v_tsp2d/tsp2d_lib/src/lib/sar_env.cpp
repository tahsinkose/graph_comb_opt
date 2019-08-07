#include "sar_env.h"
#include "graph.h"
#include <cassert>
#include <random>
#include <iostream>

int sign = 1;

SAREnv::SAREnv(double _norm) : IEnv(_norm)
{

}

void SAREnv::s0(std::pair<std::shared_ptr<Graph>,double> _g)
{
    this->graph = _g.first;
    this->graph_tour_length = _g.second;
    this->partial_set.clear();
    this->action_list.clear();
    this->action_list.push_back(0);
    this->partial_set.insert(0);

    this->state_seq.clear();
    this->act_seq.clear();
    this->reward_seq.clear();
    this->sum_rewards.clear();

    this->battery = 100;
    // Bottleneck is the optimal tour length
    if(this->graph_tour_length < 0) this->battery_depletion = 0.0;
    else this->battery_depletion = this->battery / this->graph_tour_length;
    this->battery_depletion *= 0.95;
    std::cout<<this->battery_depletion<<std::endl;
}

double SAREnv::step(int a)
{
    assert(this->graph);
    assert(this->partial_set.count(a) == 0);
    assert(a > 0 && a < this->graph->num_nodes);

    this->state_seq.push_back(this->action_list);
    this->act_seq.push_back(a);

    double r_t = add_node(a);
    
    this->reward_seq.push_back(r_t);
    this->sum_rewards.push_back(r_t);  

    return r_t;
}

int SAREnv::randomAction()
{
    assert(this->graph);
    this->avail_list.clear();

    for (int i = 0; i < this->graph->num_nodes; ++i)
        if (this->partial_set.count(i) == 0)
            this->avail_list.push_back(i);
    
    assert(this->avail_list.size());
    int idx = rand() % this->avail_list.size();
    return this->avail_list[idx];
}

bool SAREnv::isTerminal()
{
    assert(this->graph);
    return ((int)this->action_list.size() == this->graph->num_nodes);
}

/*
    h(S) is embedded in add_node function.
    inserting the node i in the partial tour at the position 'pos' which increases the tour length the least is a better choice.
*/
double SAREnv::add_node(int new_node)
{
    double cur_dist = 10000000.0;
    double punishment = 10000000.0;
    int pos = -1;
    for (size_t i = 0; i < this->action_list.size(); ++i)
    {
        int adj;
        if (i + 1 == this->action_list.size())
            adj = this->action_list[0];
        else
            adj = this->action_list[i + 1];
        double cost = this->graph->dist[new_node][this->action_list[i]]
                     + this->graph->dist[new_node][adj]
                     - this->graph->dist[this->action_list[i]][adj];
        if (cost < cur_dist)
        {
            cur_dist = cost;
            pos = i;
        }
    }
    assert(pos >= 0);
    assert(cur_dist >= -1e-8);
    this->action_list.insert(this->action_list.begin() + pos + 1, new_node);
    this->partial_set.insert(new_node);

    this->battery -= cur_dist * this->battery_depletion;
    if(this->battery > 0)
        return sign * cur_dist / norm;
    else
        return sign * punishment; //Punishment
}