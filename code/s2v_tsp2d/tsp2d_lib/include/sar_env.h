#ifndef SAR_ENV_H
#define SAR_ENV_H

#include "i_env.h"

extern int sign;

class SAREnv : public IEnv
{
public:

    SAREnv(double _norm);

    virtual void s0(std::pair<std::shared_ptr<Graph>,double>  _g) override;

    virtual double step(int a) override;

    virtual int randomAction() override;

    virtual bool isTerminal() override;

    double add_node(int new_node);
    double getBatteryDepletion();
    std::set<int> partial_set;
    std::vector<int> avail_list;
private:
	double battery;
	double battery_depletion; // for each meter.
    double graph_tour_length;
};

#endif