# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 16:43:50 2019

@author: yellemetal
"""

from Queue import Queue
from config import Config

class ConfigQueue():
    
    def __init__(self, switchRadix):
    
        self.switchRadix = switchRadix
        self.queue = Queue()
        
    def enqueue(self, schedule):
        
        if schedule == []:
            return
        
        for time_duration, perm_mat in schedule:
            
            self.queue.put(Config(self.switchRadix, time_duration, perm_mat))
            
    def dequeue(self):
        
        assert not self.queue.empty(), "ConfigQueue Error, dequeue when empty"
        return self.queue.get()
    
    def isEmpty(self):
        
        return self.queue.empty()
    
    def getDCT(self):
        
        sumDCT = 0
        new_queue = Queue()
        
        while(not self.queue.empty()):
        
            config = self.queue.get()
            sumDCT = sumDCT + config.timeDuration
            new_queue.put(config)
            
        self.queue = new_queue
            
        
        
        
        