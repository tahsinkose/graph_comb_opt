import numpy as np
import networkx as nx
import cPickle as cp
import pickle
import random
import ctypes
import os
import sys
from tqdm import tqdm

sys.path.append( '%s/tsp2d_lib' % os.path.dirname(os.path.realpath(__file__)) )
from tsp2d_lib import Tsp2dLib
n_valid = 100

if __name__ == '__main__':

    sar_api = Tsp2dLib(sys.argv)
    opt = {}
    for i in range(1, len(sys.argv), 2):
        opt[sys.argv[i][1:]] = sys.argv[i + 1]

    with open("prepared_valid_data", 'rb') as f:
   	 prepared_validation_data = pickle.load(f)

    with open("prepared_train_data", 'rb') as f:
        prepared_train_data = pickle.load(f)
    with open("train_opt_tours", 'rb') as f:
        train_opt_tours = pickle.load(f)

    for vd in prepared_validation_data:
        sar_api.InsertGraph(vd[0], is_test=True,tour_length=vd[1])

    for td in prepared_train_data:
        sar_api.InsertGraph(td[0], is_test=False,tour_length=td[1])
        #print "Tour length of ",td[0], ": ",td[1]
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
            print "-----------------------------------"
            for idx in range(n_valid):
                path_length = sar_api.lib.Test(idx)
                frac += path_length
                print "IDX: ",idx, " path length: ",path_length
            print 'iter', iter, 'lr', lr, 'eps', eps, 'average tour length: ', frac / n_valid
            sys.stdout.flush()
            model_path = '%s/nrange_%d_%d_iter_%d.model' % (opt['save_dir'], int(opt['min_n']), int(opt['max_n']), iter)
            sar_api.SaveModel(model_path)

        if iter % 1000 == 0:
            sar_api.TakeSnapshot()
            lr = lr * 0.95

        sar_api.lib.Fit(ctypes.c_double(lr))