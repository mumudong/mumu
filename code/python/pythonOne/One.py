#--coding:utf-8--
import numpy
from numpy import *
f1 = numpy.zeros((4,4),numpy.int8,'C')

'''
f2 = numpy.eye(4)
print(f2)
print('f2的维数',f2.ndim)
print('f2每一维的大小',f2.shape)
print('f2的元素数',f2.size)
print('f2元素类型',f2.dtype,'\n')

f3 = numpy.array([[1,2,3],[4,5,6]])
print(f3)
print('f3维数',f3.ndim)
print('f3每一维的大小',f3.shape)
print('f3元素数',f3.size)
print('f3元素类型',f3.dtype,'\n')

for x in numpy.linspace(1,3,10):
    print(x)
#####################
a = numpy.ones((2,2))
b = numpy.eye(2)
d = numpy.full((2,2),8)
print(d)
print('a=',a,'\nb=',b)
print('a>2=',a>2) #每个元素比较
print('a+b=',a+b) #矩阵相加
print('b*2 = ',b*2)
print('b+1 = ',b+1)
print('(a+1)*(b+1) = ',(a+1)*(b+1)) #不是矩阵相乘，只是对应的元素相乘
print('numpy.dot((a+1),(b+1)=\n',numpy.dot(a+1,b+1)) #矩阵相乘
print('a.sum=',a.sum())
print('###############################')
print('垂直合并数组:\n',numpy.vstack((a,b)))
print('水平合并数组:\n',numpy.hstack((a,b)))
'''
####################
'''
c = numpy.array([[1,2,3],[4,5,6]])
print(c.ndim) #只是2维，axis只能是0,1
print(c.sum(axis=0))  #每一列的和
print(c.sum(axis=1)) #每一行的和
'''
#######----矩阵操作----#######
# m = numpy.mat([1,2,3])
# print(m)
# print(m[0,1]) #取第一行第二个数据
# list = [4,5,6]
# n = numpy.mat(list) # list转矩阵
# print(n)

m1 = numpy.mat([1,2,3])
m2 = numpy.mat([4,7,5])
print('矩阵相乘:\n',m1*m2.T) # .T转置
print('矩阵点乘:\n',numpy.multiply(m1,m2))
print('计算夹角余弦:\n', m1*m2.T /(linalg.norm(m1)*linalg.norm(m2)))   # m1*m2=|m1|*|m2|*cosm1m2



m = numpy.mat([[1,1,1],[1,1,1]])
m.sort() #对每行排序
print('排序:\n',m)

print(linalg.norm(m))  # 元素平方和再开平方
print(linalg.norm(m,1)) # 1范数，列向量绝对值之和的最大值 axis=0表示列
print(linalg.norm(m,2)) #元素平方和再开平方
print(linalg.norm(m,'fro')) #元素平方和再开平方
print(linalg.norm(m,ord=inf)) # axis=1，表示行



