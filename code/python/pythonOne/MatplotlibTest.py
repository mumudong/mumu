#--coding:utf-8--
import numpy
from numpy import *
import matplotlib as mpl
import matplotlib.pyplot as plt

#通过rcParams设置全局纵横轴字体大小
mpl.rcParams['xtick.labelsize'] = 24
mpl.rcParams['ytick.labelsize'] = 24
random.seed(42)
#x轴采样点
x = linspace(0,5,100)

#y轴数据 俩*是乘方
y = 2 * sin(x) +0.3 * x ** x
y_data = y + random.normal(scale=0.3,size=100)

#指定图表名称
plt.figure('data')

# '.'表明画散点图,每个散点形状是个圆圈
plt.plot(x,y_data,',')

#plot默认画连线图
plt.figure('model')
plt.plot(x,y)

plt.figure('data & model')
# 通过'k'指定线的颜色，lw指定线的宽度
# 第三个参数除了颜色也可以指定线形，比如'r--'表示红色虚线
# 更多属性可以参考官网：http://matplotlib.org/api/pyplot_api.html
plt.plot(x,y,'k',lw=3)

#scatter可以更容易的生成散点图
plt.scatter(x,y_data)

plt.savefig('result.png')

plt.show() #加上这句才会显示在屏幕上