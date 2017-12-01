#--coding:utf-8--
import numpy
from numpy import *

random.seed(42) # 这样下面的方法都不随机了
print('rand(2,3)------>\n',random.rand(2,3))  #产生一个2x3，[0,1)之间的浮点型随机数
print('randn(10)------->\n',random.randn(10))
print('sample(2,3)------>\n',random.sample((2,3)))
print('ranf(2,3)------>\n',random.ranf((2,3)))
print('rand ------>\n',random.rand())
print('uniform------>\n',random.uniform(1,6,10)) #产生指定范围的随机数
print('randint---->\n',random.randint(1,6,10),'\n并计算标准差---->\n',std(random.randint(1,6,10)))
a = random.normal(0,1,10)
print('normal正态分布样本---->\n',a)
print('均值---->',a.mean())
b = random.binomial(n=10,p=0.5,size=5)
print('二项分布---->',b)
a = arange(1,10,1)
print('随机有放回抽样---->',random.choice(a,4,replace=True))
print('打乱顺序---->',random.permutation(a))
print('a---->',a)
random.shuffle(a) #没返回值
print('还是打乱顺序---->',a)
