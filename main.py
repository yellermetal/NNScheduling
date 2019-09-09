# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 02:48:56 2019

@author: Ariel
"""

from switch import Switch
import pickle

switchRadix = 64
reconfig_penalty = 25

timeline_params = { 'switchRadix'     : switchRadix, 
                    'time_window'     : 1000,
                    'light_flows_num' : 12,
                    'heavy_flows_num' : 4,
                    'light_range'     : [1,16],
                    'heavy_range'     : [16,100] }

OCS_switch = Switch(switchRadix, reconfig_penalty, timeline_params)

clock = 0
while(not OCS_switch.demand.isEmpty()):
    
    if clock % 1000 == 0:
        print "clock: ", clock, " flowNumber: ", OCS_switch.demand.flowNumber
    
    OCS_switch.demand.update(clock)
    OCS_switch.switch_scheduler.update(clock)
    OCS_switch.update(clock)
    
    clock = clock + 1
    
assert OCS_switch.demand.flowNumber == 0, "Finished, but flowNumber != 0"

flow_stats = []
for flow in OCS_switch.demand.flows:
    flow_stats.append(flow.getStats())
    
with open("flow_stats_baseline.pickle", "wb") as f:
    pickle.dump(flow_stats, f)
    
    

