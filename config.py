# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 16:04:18 2019

@author: yellemetal
"""

class Config():
    
    def __init__(self, switchRadix, time_duration, perm_mat):
        
        self.switchRadix = switchRadix
        self.timeDuration = time_duration
        self.permMatrix = perm_mat
        
        for elem in range(self.switchRadix):
            
            in_list = False
            empty_slot = -1
            
            for i in range(self.switchRadix):
                if self.permMatrix[i] == elem:
                    in_list = True
                if self.permMatrix[i] == -1:
                    empty_slot = i
                    
            if in_list == False:
                assert empty_slot != -1, "Config Error, empty_slot == -1"
                self.permMatrix[empty_slot] = elem
               
    def service(self):
        self.timeDuration = self.timeDuration - 1