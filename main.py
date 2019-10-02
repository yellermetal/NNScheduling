# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 02:48:56 2019

@author: Ariel
"""

from switch import Switch
from policy import Policy, finish_episode
import torch.optim as optim
import numpy as np
import pickle
import os

switchRadix = 64
reconfig_penalty = 25
numEpisodes = 10

timeline_params = { 'switchRadix'     : switchRadix, 
                    'window_num'      : 5,
                    'time_window'     : 1000,
                    'light_flows_num' : 12,
                    'heavy_flows_num' : 4,
                    'light_range'     : [1,16],
                    'heavy_range'     : [16,100] }

input_size = switchRadix*switchRadix + 1
hidden_size = input_size

if os.path.isfile("NN_model.pickle"):
    with open("NN_model.pickle", "rb") as F:
        policy = pickle.load(F)
else:
    policy = Policy(input_size, hidden_size)
optimizer = optim.Adam(policy.parameters(), lr=1)
eps = np.finfo(np.float32).eps.item()


episodeResults = []
for episode in range(numEpisodes):

    print "Running episode #", episode
    
    OCS_switch = Switch(switchRadix, reconfig_penalty, timeline_params)
    Results = {}
    
    clock = 0
    while(not OCS_switch.demand.isEmpty()):
        
        if clock % 1000 == 0:
            print "clock: ", clock, " flowNumber: ", OCS_switch.demand.flowNumber
        
        OCS_switch.demand.update(clock)
        OCS_switch.switch_scheduler.update(clock)
        OCS_switch.update(clock)
        
        clock = clock + 1
        
    assert OCS_switch.demand.flowNumber == 0, "Finished, but flowNumber != 0"
    Results['baseline'] = { 'flow_number' : OCS_switch.demand.flowNumber, 
                            'flow_stats' : OCS_switch.demand.aggregateResults() }
    
    OCS_switch.switch_scheduler.policy = policy
    OCS_switch.demand.reset()
    
    clock = 0
    for i in range(OCS_switch.switch_scheduler.baseline_reward.qsize()):
        
        if clock % 1000 == 0:
            print "clock: ", clock, " flowNumber: ", OCS_switch.demand.flowNumber
        
        OCS_switch.demand.update(clock)
        OCS_switch.switch_scheduler.update(clock)
        OCS_switch.update(clock)
        
        clock = clock + 1
        
    Results['NN'] = { 'flow_number' : OCS_switch.demand.flowNumber, 
                      'flow_stats' : OCS_switch.demand.aggregateResults() }
        
    finish_episode(policy, optimizer, eps)
    episodeResults.append(Results)
    
    
with open("NN_model.pickle", "wb") as F:
    pickle.dump(policy, F)
    
with open("Train_results.pickle", "wb") as F:
    pickle.dump(episodeResults, F)





    

