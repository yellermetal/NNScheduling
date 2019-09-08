# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 15:25:46 2019

@author: yellemetal
"""

from SMG import Sparse_Matrix_Generator
from flow import Flow
import numpy as np

WINDOW_NUM = 30

class Timeline():
    
    def __init__(self, timeline_params):
        
        self.switchRadix = timeline_params['switchRadix']
        self.currTime = 0
        self.flowNumber = 0
        self.flows = []
        
        for time in np.arange(WINDOW_NUM)*timeline_params['time_window']:
            
            SMG_mat = Sparse_Matrix_Generator(self.switchRadix, timeline_params['light_flows_num'],
                                                                timeline_params['heavy_flows_num'],
                                                                timeline_params['light_range'],
                                                                timeline_params['heavy_range'])
            
            for src in range(self.switchRadix):
                for dst in range(self.switchRadix):
                    
                    if SMG_mat[src][dst] > 0:
                        timestamp = np.random.randint(time, time + timeline_params['time_window'])
                        self.flows.append(Flow(SMG_mat[src][dst], timestamp, src, dst))
                        self.flowNumber = self.flowNumber + 1
                        
            
    def getDemand(self):
        
        demandMatrix = np.zeros((self.switchRadix, self.switchRadix))
        
        for flow in self.flows:
            
            if flow.markedForScheduling == False and \
               flow.timestamp <= self.currTime and \
               flow.remainingSize > 0:
                   
                                      
                   demandMatrix[flow.src][flow.dst] = demandMatrix[flow.src][flow.dst] + flow.remainingSize
                   flow.markedForScheduling = True
                   
        return demandMatrix
    
    def serveDemand(self, config):
        
        flow_serviced = np.zeros(self.switchRadix)
        
        for flow in self.flows:
            
            if flow.remainingSize > 0 and \
               flow.src == config.permMatrix[flow.dst] and \
               flow.timestamp <= self.currTime and \
               flow_serviced[flow.src] == 0:
                   
                   if flow.service(self.currTime):
                       self.flowNumber = self.flowNumber - 1
                       if self.flowNumber == 0:
                           print "Timeline has been served!"
                           
                   flow_serviced[flow.src] = 1
                   
    def reset(self):
        
        for flow in self.flows:
            
            flow.remainingSize = flow.size
            flow.flowCompletionTime = -1
            flow.markedForScheduling = False
            self.flowNumber = self.flowNumber + 1
            
        self.currTime = 0
        
    def isEmpty(self):
        return self.flowNumber == 0
    
    def update(self, clock):
        self.currTime = clock
        
    
               
        
        
        
        
        
        
        
        
        
        
        
        
                   
            