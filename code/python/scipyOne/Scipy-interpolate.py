# -*- coding: utf-8 -*-

# 调用模块
# 调用数组模块
import numpy as np
# 实现插值的模块
from scipy import interpolate
# 画图的模块
import matplotlib.pyplot as plt
# 生成随机数的模块
import random

# random.randint(0, 10) 生成0-10范围内的一个整型数
# y是一个数组里面有10个随机数，表示y轴的值
y = np.array([random.randint(0, 10) for _ in range(10)])
# x是一个数组，表示x轴的值
x = np.array([num for num in range(10)])
print(np.arange(0,10,0.1))
# 插值法之后的x轴值，表示从0到10间距为0.5的20个数
xnew = np.arange(0,9.1, 0.1)

"""
kind方法：
nearest、zero、slinear、quadratic、cubic
实现函数func
"""
func = interpolate.interp1d(x, y, kind='cubic')
# 利用xnew和func函数生成ynew，xnew的数量等于ynew数量
ynew = func(xnew)
plt.rcParams['font.sans-serif'] = 'SimHei'
# 画图部分
# 原图
plt.plot(x, y, 'r.',label='原图')
# 拟合之后的平滑曲线图
plt.plot(xnew, ynew,'g',label='插值')
plt.legend()
plt.show()