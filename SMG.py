# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 15:35:37 2019

@author: yellemetal
"""

import numpy as np
from datetime import datetime

def Sparse_Matrix_Generator(size, num_light_flows, num_heavy_flows, light_range, heavy_range):
    
    now = (datetime.now()-datetime(1970,1,1)).total_seconds()
    np.random.seed(int(now))
    
    matrix = np.zeros((size,size))
    rand_idx = np.arange(size)
    
    for num in range(num_light_flows):
        
        np.random.shuffle(rand_idx)
        for i in range(size):
            matrix[i][rand_idx[i]] =  matrix[i][rand_idx[i]] + np.random.randint(light_range[0], light_range[1])
            
    for num in range(num_heavy_flows):
        
        np.random.shuffle(rand_idx)
        for i in range(size):
            matrix[i][rand_idx[i]] =  matrix[i][rand_idx[i]] + np.random.randint(heavy_range[0], heavy_range[1])
            
    return matrix
           
        
           
    