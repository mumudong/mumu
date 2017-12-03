#--coding:utf-8--
import numpy
from numpy import *

#######----矩阵操作----#######
# m = numpy.mat([1,2,3])
# print(m)
# print(m[0,1]) #取第一行第二个数据
# list = [4,5,6]
# n = numpy.mat(list) # list转矩阵
# print(n)

# m1 = numpy.mat([1,2,3])
# m2 = numpy.mat([4,7,5])
# print('矩阵相乘:\n',m1*m2.T) # .T转置
# print('矩阵点乘:\n',numpy.multiply(m1,m2))
# print('计算夹角余弦:\n', m1*m2.T /(linalg.norm(m1)*linalg.norm(m2)))   # m1*m2=|m1|*|m2|*cosm1m2



m = numpy.mat([[2,1,1],[1,1,1],[1,2,2]])
m.sort() #对每行排序
print('排序:\n',m)

print(linalg.norm(m))  # 元素平方和再开平方
print(linalg.norm(m,1)) # 1范数，列向量绝对值之和的最大值 axis=0表示列
print(linalg.norm(m,2)) #元素平方和再开平方
print(linalg.norm(m,'fro')) #元素平方和再开平方
print(linalg.norm(m,ord=inf)) # axis=1，表示行

print('行列式------------------->\n',linalg.det(m))
print('矩阵的迹------------------->\n',trace(m)) #主对角线元素之和，特征值之和？
print('矩阵的秩------------------->\n',linalg.matrix_rank(m))

print('eig特征值分解------------------->\n',linalg.eig(m)) #按虚数特征值分解
print('eigh特征分解------------------->\n',linalg.eigh(m))  #按实数特征值分解

print('SVD奇异值分解-------------\n\n')
m = numpy.mat([[2,1,1],[1,1,1]])
print(m)
U, s, V = linalg.svd(m, full_matrices=True) # full_matrices确定返回值是 N*N,K,M*M,还是M*K,K,K*N
print('U-------------------->\n',U,'\ns-------------------->\n',s,'\nV-------------------->\n',V)
print(U.shape,s.shape,V.shape)
print('diag(s)-------------------->\n',diag(s))
S = zeros((2, 3), dtype=complex)
S[:2,:2]=diag(s)
print('dot(U,dot(S,V))------------------->\n',dot(U,dot(S,V)))
print(allclose(m,dot(U,dot(S,V))))
