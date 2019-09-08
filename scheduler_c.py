
import numpy as np
import ctypes as ct

def to_perm_mat(matching, size):
    
    res = np.zeros((size,size))
    
    for col in range(size):
        res[matching[col]][col] = 1
        
    return res
    

def scheduler(sched_name, matrix, reconfig_penalty):

    if (matrix.shape[0] != matrix.shape[1]):
        raise Exception('Input matrix must be square.')
        
    if ((matrix >= 0).all() == False):
        raise Exception('Input matrix must be non-negative.')

    lib = ct.cdll.LoadLibrary('./schedulerLIB.so')
    scheduler = lib.scheduler
    
    size = len(matrix)
    matrix_data = (ct.c_double*size*size)()
    for i in range(size):
        for j in range(size):
            matrix_data[i][j] = matrix[i][j] 
    
    c_reconfig_penalty = ct.c_double(reconfig_penalty)
    name = ct.c_char_p(sched_name.encode('utf-8'))
    c_size = ct.c_int(size)
    runtime = ct.c_double()
    times = ct.POINTER(ct.c_int)()
    matchings = ct.POINTER(ct.POINTER(ct.c_int))()
    config_num = ct.c_int()
    
    
    scheduler(name, c_size, c_reconfig_penalty, matrix_data, ct.byref(runtime), ct.byref(times), ct.byref(matchings), ct.byref(config_num))
    
    runtime = runtime.value
    
    decomp = []
    
    for i in range(config_num.value):
        decomp.append((times[i], to_perm_mat(matchings[i], size)))
        
    return decomp, runtime
    


def lumos(matrix, reconfig_penalty):
    return scheduler("Lumos", matrix, reconfig_penalty)
    
def solstice(matrix):
    return scheduler("Solstice", matrix, 20)

    
