#--coding:utf-8--
import numpy as np

x = np.array([1,2])
print(x)
print(x.shape) # 1维时，相当于元素的个数

y = np.expand_dims(x,axis=0)
print(y)
print(y.shape,y.ndim) # 2维时，相当于矩阵的形状

z = np.expand_dims(x,axis=1)
print(z)
print(z.shape)


d = np.array([1,2,3,4,5,6,7,8,9])
d = d.reshape((3,3))
print(d.shape)
print(d.sum(axis=0))  # (3,3) axis=0之后，第一个表示行的三被去除，只剩下列了
print(np.expand_dims(d,axis=2).shape)
print(d)
print(np.expand_dims(d,axis=3)) # 到底是怎么增维的？


