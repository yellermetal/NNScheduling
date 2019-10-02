# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 16:29:58 2019

@author: yellemetal
"""

TRIVIAL = 3000

from scheduler_c import lumos
from configQueue import ConfigQueue
from policy import select_action
from torch import Tensor
from Queue import Queue

import numpy as np

class Scheduler():
    
    def __init__(self, switchRadix, reconfig_penalty, policy = None):
        
        self.switchRadix = switchRadix
        self.reconfig_penalty = reconfig_penalty
        
        self.config_queue = ConfigQueue(self.switchRadix)
        self.scheduler = lumos
        
        self.runtimeDelay = 0
        self.schedulingDelay = TRIVIAL
        self.policy = policy
        self.baseline_reward = Queue()
         
    def readyToSchedule(self, demand):
        
        if self.policy is None:
            self.baseline_reward.put(demand.calcReward())
            return self.runtimeDelay <= 0 and self.schedulingDelay <= 0
        
        elif self.runtimeDelay <= 0:
            
            state = Tensor(np.append(demand.getState().flatten(), self.config_queue.getDCT()))
            action = select_action(self.policy, state)
            #print "the action: ", action
            self.policy.rewards.append(demand.calcReward() - self.baseline_reward.get())
            return action
        
        else:
            return False
        
        
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
        
        
        
        
    