#--coding:utf-8--
import numpy
from numpy import *
f1 = numpy.zeros((4,4),numpy.int8,'C')

# fo = [1,2,3]
# b = array(fo)
# print(b.mean())
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

for x in numpy.linspace(1,3,10): #等差数列
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
'''
a = arange(24).reshape((2,3,4))
print(a) # 第一维是z轴，第二维是行，第三维是列
print('a[:,2,:]---->\n',a[:,2,:]) # 打印第三行的数据
print('a[...,1]---->\n',a[...,1]) # 打印第二列的数据
print('a[:,1:,1:-1]---->\n',a[:,1:,1:-1]) # 第二行以后，第二列截至最后一列

print('split---->\n',split(arange(9),[2,-3]))  # ary[:2,2:-3,-3:]
'''
l0 = arange(6).reshape((2,3))
l1 = arange(6,12).reshape((2,3))
print('\n列扩展vstack((l0,l1))---->\n',vstack((l0,l1))) #垂直扩展
print('\n行扩展hstack((l0,l1))---->\n',hstack((l0,l1))) #水平扩展
print('\n列扩展concatenate((l0,l1))---->\n',concatenate((l0,l1)))
print('\n行扩展concatenate((l0,l1),axis=1)---->\n',concatenate((l0,l1),axis=1))
print('\nz轴扩展stack((l0,l1))---->\n',stack((l0,l1)))

s = stack((l0,l1))
# print('转置---->\n',s.transpose((2,0,1)))  # 下标转置，由0,1,2转为2,0,1。相当于坐标变换，想象坐标轴变化
# print('转置---->\n',s.transpose())  # 下标转置，由0,1,2转为2,1,0
u = s[0].transpose()
print('转置---------->\n',u) # z轴第一层矩阵转置
print('rot90---------->\n',rot90(u,k=1,axes=(0,1))) # 矩阵元素旋转90度，和空间坐标无关，只是调换矩阵元素位置,由下箭头向右箭头转
print('flip--------->\n',flip(u,0)) #沿纵轴反转
print('roll----->',roll(u,1,axis=0))
