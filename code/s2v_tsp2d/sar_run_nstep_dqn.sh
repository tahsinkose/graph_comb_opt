#!/bin/bash

g_type=clustered

result_root=results

# max belief propagation iteration
max_bp_iter=4

# embedding size
embed_dim=64

# gpu card id
dev_id=1

# max batch size for training/testing
batch_size=128

net_type=QNet
decay=0.1

# set reg_hidden=0 to make a linear regression
reg_hidden=32

# learning rate
learning_rate=0.0001

# init weights with rand normal(0, w_scale)
w_scale=0.01

# nstep
n_step=1

knn=10

min_n=15
max_n=20

num_env=1
mem_size=5000

max_iter=10000

# folder to save the trained SAR models on the fly
save_dir=$result_root/sar_solvers

# folder to load the trained TSP solvers for bottleneck creation.
load_dir=$result_root/tsp_solvers

if [ ! -e $save_dir ];
then
    mkdir -p $save_dir
fi

python sar_train.py \
    -net_type $net_type \
    -n_step $n_step \
    -data_root ../../data/tsp2d \
    -decay $decay \
    -knn $knn \
    -min_n $min_n \
    -max_n $max_n \
    -num_env $num_env \
    -max_iter $max_iter \
    -mem_size $mem_size \
    -g_type $g_type \
    -learning_rate $learning_rate \
    -max_bp_iter $max_bp_iter \
    -net_type $net_type \
    -max_iter $max_iter \
    -save_dir $save_dir \
    -load_dir $load_dir \
    -embed_dim $embed_dim \
    -batch_size $batch_size \
    -reg_hidden $reg_hidden \
    -momentum 0.9 \
    -l2 0.00 \
    -w_scale $w_scale \
    2>&1 | tee $save_dir/log-$min_n-${max_n}.txt