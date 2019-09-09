# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 02:48:56 2019

@author: Ariel
"""

from switch import Switch

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
    
    OCS_switch.demand.update(clock)
    OCS_switch.switch_scheduler.update(clock)
    OCS_switch.update(clock)
    
    clock = clock + 1
    
assert OCS_switch.demand.flowNumber == 0, "Finished, but flowNumber != 0"
flows = OCS_switch.demand.flows()

