#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 07:56:36 2019

@author: ariell
"""

import pickle
import matplotlib.pyplot as plt
import numpy as np


with open("flow_stats_baseline.pickle", "rb") as f:
    flow_stats = pickle.load(f)
    
FlowCompletionTimes = []
for flow_stat in flow_stats:
    FlowCompletionTimes.append(flow_stat['flowCompletionTime'])
    
    
FCTs = {}
        
for fct in FlowCompletionTimes:
    FCTs[fct] = FCTs.get(fct, 0) + 1  
    
    
fcts = sorted(FCTs.keys())

y,binEdges=np.histogram(fcts,bins=100)
bincenters = 0.5*(binEdges[1:]+binEdges[:-1])
plt.plot(bincenters,y)
plt.xlabel('Flow Completion Times [msec]', fontsize='large')
plt.ylabel('Occurences', fontsize='large')
#plt.legend(loc='upper right', shadow=True)
plt.grid(True)