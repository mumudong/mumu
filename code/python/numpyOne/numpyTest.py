#--coding:utf-8--
import numpy as np

a = np.array(([2,2],[6,4]))

a_mean = a.mean(axis=0) # [ 4.  3.]
a_std = a.std(axis=0)   # [ 2.  1.]
'''
[[-1. -1.]
 [ 1.  1.]]
'''
a_norm = (a-a_mean)/a_std
print(a)
print(a_mean)
print(a_std)
print(a_norm)