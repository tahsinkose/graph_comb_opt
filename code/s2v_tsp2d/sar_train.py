import numpy as np
import networkx as nx
import cPickle as cp
import random
import ctypes
import os
import sys
from tqdm import tqdm

sys.path.append( '%s/tsp2d_lib' % os.path.dirname(os.path.realpath(__file__)) )
from tsp2d_lib import Tsp2dLib

n_valid = 100

def find_model_file(opt):
    max_n = int(opt['max_n'])
    min_n = int(opt['min_n'])
    log_file = None
    if max_n < 100:
        return None
    if min_n == 100 and max_n == 200:
        n1 = 50
        n2 = 100
    else:
        n1 = min_n - 100
        n2 = max_n - 100

    log_file = '%s/log-%d-%d.txt' % (opt['load_dir'], n1, n2)
    if not os.path.isfile(log_file):
        return None
    best_r = 1000000
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
    if best_it < 0:
        return None
    return '%s/nrange_%d_%d_iter_%d.model' % (opt['load_dir'], n1, n2, best_it)

def PrepareGraphs(api,isValid):
    if isValid:
        n_graphs = 100
        prefix = 'validation_tsp2d'
    else:
        n_graphs = 10000
        prefix = 'train_tsp2d'
    folder = '%s/%s/tsp_min-n=%s_max-n=%s_num-graph=%d_type=%s' % (opt['data_root'], prefix, opt['min_n'], opt['max_n'], n_graphs, opt['g_type'])

    with open('%s/paths.txt' % folder, 'r') as f:
        graphs_with_optimal_tour_lens = []
        for line in tqdm(f):
            fname = '%s/%s' % (folder, line.split('/')[-1].strip())
            coors = {}
            in_sec = False
            n_nodes = -1
            with open(fname, 'r') as f_tsp:
                for l in f_tsp:
                    if 'DIMENSION' in l:
                        n_nodes = int(l.split(' ')[-1].strip())
                    if in_sec:
                        idx, x, y = [int(w.strip()) for w in l.split(' ')]
                        coors[idx - 1] = [float(x) / 1000000.0, float(y) / 1000000.0]
                        assert len(coors) == idx
                    elif 'NODE_COORD_SECTION' in l:
                        in_sec = True
            assert len(coors) == n_nodes
            g = nx.Graph()
            g.add_nodes_from(range(n_nodes))
            nx.set_node_attributes(g, coors, 'pos')
            api.InsertGraph(g,is_test=True)
            optimal_tour_len,_ = tsp_solver_api.GetSol(0,nx.number_of_nodes(g))
            graphs_with_optimal_tour_lens.append((g,optimal_tour_len))
        
        return graphs_with_optimal_tour_lens

if __name__ == '__main__':
    tsp_solver_api = Tsp2dLib(sys.argv)
    opt = {}
    for i in range(1, len(sys.argv), 2):
        opt[sys.argv[i][1:]] = sys.argv[i + 1]

    model_file = find_model_file(opt)
    
    if model_file is not None:
        print 'loading', model_file
        sys.stdout.flush()
        tsp_solver_api.LoadModel(model_file)
    print "TSP solver is loaded"
    prepared_validation_data = PrepareGraphs(tsp_solver_api,isValid=True)
    prepared_train_data = PrepareGraphs(tsp_solver_api,isValid=False)

    sar_api = tsp_solver_api
    sar_api.ResetModel()
    for vd in prepared_validation_data:
        sar_api.InsertGraph(vd[0], is_test=True,tour_length=vd[1])
    
    for td in prepared_train_data:
        sar_api.InsertGraph(td[0], is_test=False,tour_length=td[1])
    
    # startup    
    for i in range(10):
        sar_api.lib.PlayGame(100, ctypes.c_double(1.0))
    sar_api.TakeSnapshot()

    eps_start = 1.0
    eps_end = 1.0

    eps_step = 10000.0
    sar_api.lib.SetSign(1)

    lr = float(opt['learning_rate'])
    for iter in range(int(opt['max_iter'])):
        eps = eps_end + max(0., (eps_start - eps_end) * (eps_step - iter) / eps_step)
        if iter % 10 == 0:
            sar_api.lib.PlayGame(10, ctypes.c_double(eps))

        if iter % 100 == 0:
            frac = 0.0
            for idx in range(n_valid):
                frac += sar_api.lib.Test(idx)
            print 'iter', iter, 'lr', lr, 'eps', eps, 'average tour length: ', frac / n_valid
            sys.stdout.flush()
            model_path = '%s/nrange_%d_%d_iter_%d.model' % (opt['save_dir'], int(opt['min_n']), int(opt['max_n']), iter)
            sar_api.SaveModel(model_path)

        if iter % 1000 == 0:
            sar_api.TakeSnapshot()
            lr = lr * 0.95

        sar_api.lib.Fit(ctypes.c_double(lr))
