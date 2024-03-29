# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 15:12:35 2019

@author: yellemetal
"""

from scheduler import Scheduler
from timeline import Timeline

class Switch():
    
    def __init__(self, switchRadix, reconfig_penalty, timeline_params):
        
        self.switchRadix = switchRadix
        self.reconfig_penalty = reconfig_penalty
        self.switch_scheduler = Scheduler(switchRadix, reconfig_penalty)
        self.demand = Timeline(timeline_params)
        self.reconfig_delay = reconfig_penalty
        self.currConfig = None
        
    def update(self, clock):
        
        if self.switch_scheduler.readyToSchedule(self.demand, clock):
            demandMatrix = self.demand.getDemand()
            self.switch_scheduler.scheduleDemand(demandMatrix)
            
        if self.reconfig_delay > 0:
            self.reconfig_delay = self.reconfig_delay - 1
            return 
        
        if self.currConfig == None:
            self.currConfig = self.switch_scheduler.getNextConfig()
            
        if self.currConfig != None and self.currConfig.timeDuration > 0:
            self.demand.serveDemand(self.currConfig)
            self.currConfig.service()
            
            if self.currConfig.timeDuration == 0:
                
                self.currConfig = None
                self.reconfig_delay = self.reconfig_penalty
                
