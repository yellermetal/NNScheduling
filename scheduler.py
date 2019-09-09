# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 16:29:58 2019

@author: yellemetal
"""

TRIVIAL = 3000

from scheduler_c import lumos
from configQueue import ConfigQueue

import numpy as np

class Scheduler():
    
    def __init__(self, switchRadix, reconfig_penalty):
        
        self.switchRadix = switchRadix
        self.reconfig_penalty = reconfig_penalty
        
        self.config_queue = ConfigQueue(self.switchRadix)
        self.scheduler = lumos
        
        self.runtimeDelay = 0
        self.schedulingDelay = TRIVIAL
        
    def readyToSchedule(self):
        
        return self.runtimeDelay <= 0 and self.schedulingDelay <= 0
        
        
    def scheduleDemand(self, demandMatrix):
        
        if demandMatrix.any():
        
            self.schedule, self.runtimeDelay = self.scheduler(demandMatrix, self.reconfig_penalty)
            self.schedulingDelay = max(TRIVIAL, self.runtimeDelay)
        
        
    def getNextConfig(self):
        
        if self.config_queue.isEmpty():
            return None
        
        else:
            return self.config_queue.dequeue()
        
    def update(self, clock):
        
        if self.runtimeDelay > 0:
             self.runtimeDelay = self.runtimeDelay - 1
             
             if self.runtimeDelay <= 0:
                 self.config_queue.enqueue(self.schedule)
                 self.schedule = None
                 
        if self.schedulingDelay > 0:
            self.schedulingDelay = self.schedulingDelay - 1
        
        
        
        
    