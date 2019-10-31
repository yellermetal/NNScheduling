#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 18:00:21 2019

@author: ariellivshits
"""

import pickle
import numpy as np
import matplotlib.pyplot as plt

with open("Train_results.pickle", "rb") as F:
    results = pickle.load(F)
    
baseline_results = results['baseline']['flow_stats']
NN_results = results['NN']['flow_stats'] 

baseline_FCTs = [stats['flowCompletionTime'] for stats in baseline_results]
NN_FCTs = [stats['flowCompletionTime'] for stats in NN_results]

def plot_FCTs(FlowCompletionTimes, label):
    
    FCTs = {}
        
    for fct in FlowCompletionTimes:
        FCTs[fct] = FCTs.get(fct, 0) + 1  
        
        
    fcts = sorted(FCTs.keys())
    
    y,binEdges=np.histogram(fcts,bins=100)
    bincenters = 0.5*(binEdges[1:]+binEdges[:-1])
    plt.plot(bincenters,y, label=label)
    plt.xlabel('Flow Completion Times [msec]', fontsize='large')
    plt.ylabel('Occurences', fontsize='large')
    #plt.legend(loc='upper right', shadow=True)
    plt.grid(True)
    
plot_FCTs(baseline_FCTs, 'Baseline')
plot_FCTs(NN_FCTs, 'Neural Network')
plt.legend()

plt.savefig("NN_results.jpg")

plt.show()