# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 15:17:18 2019

@author: yellemetal
"""

from itertools import count

class Flow():
    _ids = count(0)
    
    def __init__(self, size, timestamp, src, dst):
        
        self.size = size
        self.remainingSize = size
        self.timestamp = timestamp
        self.src = src
        self.dst = dst
        self.flowCompletionTime = -1
        self.id = next(self._ids)
        self.markedForScheduling = False
        
    def service(self, curr_timestamp):
        
        self.remainingSize = self.remainingSize -1
        if self.remainingSize == 0 and self.flowCompletionTime == -1:
            self.flowCompletionTime = curr_timestamp - self.timestamp
            return True
	
    	return False
    
    def getTimeWaiting(self, curr_timestamp):
        
        return curr_timestamp - self.timestamp
        
        
        