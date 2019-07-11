import numpy as np
import networkx as nx
import cPickle as cp
import random
import ctypes
import os
import sys
import time
from tqdm import tqdm

sys.path.append( '%s/tsp2d_lib' % os.path.dirname(os.path.realpath(__file__)) )
from tsp2d_lib import Tsp2dLib
    
def find_model_file(opt):
    max_n = int(opt['max_n'])
    min_n = int(opt['min_n'])
    log_file = '%s/log-%d-%d.txt' % (opt['save_dir'], min_n, max_n)

    best_r = 10000000
    best_it = -1
    with open(log_file, 'r') as f:
        for line in f:
            if 'average' in line:
                line = line.split(' ')
                it = int(line[1].strip())
                r = float(line[-1].strip())
                if r < best_r:
                    best_r = r
                    best_it = it
    assert best_it >= 0
    print 'using iter=', best_it, 'with r=', best_r
    return '%s/nrange_%d_%d_iter_%d.model' % (opt['save_dir'], min_n, max_n, best_it)

def TestGraph():
    fname = 'survivors.tsp'
    coors = {}
    in_sec = False
    n_nodes = -1
    with open(fname, 'r') as f_tsp:
        for l in f_tsp:
            if 'DIMENSION' in l:
                n_nodes = int(l.split(' ')[-1].strip())
            if in_sec:
                idx, x, y = [float(w.strip()) for w in l.split(' ')]
                coors[idx - 1] = [float(x) / 1000000.0, float(y) / 1000000.0]
                assert len(coors) == idx
            elif 'NODE_COORD_SECTION' in l:
                in_sec = True
    assert len(coors) == n_nodes
    g = nx.Graph()
    g.add_nodes_from(range(n_nodes))
    nx.set_node_attributes(g, coors, 'pos')
    return g

if __name__ == '__main__':
    api = Tsp2dLib(sys.argv)
    opt = {}
    for i in range(1, len(sys.argv), 2):
        opt[sys.argv[i][1:]] = sys.argv[i + 1]

    model_file = find_model_file(opt)
    assert model_file is not None
    print 'loading', model_file
    sys.stdout.flush()
    api.LoadModel(model_file)

    print 'testing'
    sys.stdout.flush()
    g = TestGraph()
    api.InsertGraph(g, is_test=True)
    t1 = time.time()
    tour_len, sol = api.GetSol(0, nx.number_of_nodes(g))
    t2 = time.time()
    print(tour_len*1000000.0)
    print(sol[0])
    for i in range(sol[0]):
        print(' %d' % sol[i + 1]),
    print('\nTime: %.6f\n' % (t2 - t1))