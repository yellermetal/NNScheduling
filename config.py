# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 16:04:18 2019

@author: yellemetal
"""

import numpy as np

class Config():
    
    def __init__(self, switchRadix, time_duration, perm_mat):
        
        self.switchRadix = switchRadix
        self.timeDuration = time_duration
        self.permMatrix = perm_mat
        
        taken_rows = np.zeros(switchRadix)
        taken_cols = np.zeros(switchRadix)
        
        if np.sum(self.permMatrix) != self.switchRadix:
        
            for row,col in np.where(self.permMatrix == 1):
                taken_rows[row] = 1
                taken_cols[col] = 1
                
            for row,col in np.where(self.permMatrix == 0):
                if taken_rows[row] == 0 and taken_cols[col] == 0:
                    self.permMatrix[row][col] = 1
                    taken_rows[row] = 1
                    taken_cols[col] = 1
                    
            assert np.sum(self.permMatrix) == self.switchRadix, "np.sum(self.permMatrix) != self.switchRadix"
                
               
    def service(self):
        self.timeDuration = self.timeDuration - 1