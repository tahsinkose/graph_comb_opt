## Initial Note
I'm using this project as a basis for my own project. Therefore, this fork focuses on the TSP solutions and this README is adapted accordingly.

# graph_comb_opt 
Implementation of "Learning Combinatorial Optimization Algorithms over Graphs" (https://arxiv.org/abs/1704.01665)

Solution graphs on TSP instances.
![demo1](https://github.com/tahsinkose/graph_comb_opt/blob/master/visualize/sltn1.png)
![demo2](https://github.com/tahsinkose/graph_comb_opt/blob/master/visualize/sltn2.png)

# 1. build

**** Below shows an example of MVC. For all the problems, you can follow the similar pipeline ****

Get the source code, and install all the dependencies. 

    git clone --recursive https://github.com/tahsinkose/graph_comb_opt
    
    build the graphnn library with the instructions here:
      https://github.com/tahsinkose/graphnn
    
For TSP task, build the dynamic library.

    cd code/s2v_tsp2d/tsp2d_lib/
    
    customize Makefile if necessary
    ( add CXXFLAGS += -DGPU_MODE in the Makefile if you want to run it in GPU mode)
    
    make -j
    
Now you are all set with the C++ backend. 

### Training with n-step Q-learning

Navigate to the TSP folder and run the training script. Modify the script to change the parameters. 

    cd code/s2v_tsp2d
    ./run_nstep_dqn.sh
    
By default it will save all the model files, the logs under currentfolder/results. Note that the code will generate the data on the fly, including the validation dataset. So the training code itself doesn't rely on the data generator. 

### Test the performance

Navigate to the TSP folder and run the evaluation script. Modify the script to change the parameters. Make sure the parameters are consistent with your training script. 

    cd code/s2v_tsp2d
    ./run_eval.sh

# 2. Experiments on real-world data

For TSP we test on part of the tsplib instances;

All the data can be found through the dropbox link below. Code folders that start with 'realworld' are for this set of experiments. 

# Reproducing the results that reported in the paper

Here is the link to the dataset that was used in the paper:

https://www.dropbox.com/sh/r39596h8e26nhsp/AADRm5mb82xn7h3BB4KXgETsa?dl=0


# Reference

Please cite our work if you find our code/paper is useful to your work. 

    @article{dai2017learning,
      title={Learning Combinatorial Optimization Algorithms over Graphs},
      author={Dai, Hanjun and Khalil, Elias B and Zhang, Yuyu and Dilkina, Bistra and Song, Le},
      journal={arXiv preprint arXiv:1704.01665},
      year={2017}
    }
