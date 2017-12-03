#--coding:utf-8--
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as optimize
import pylab as pl

def f1(x,a,b):
    return a * x + b
def f2(x,a,b,c):
    return a * x ** 2 + b * x + c
def f3(x,a,b,c,d):
    return a * x ** 3 + b * x ** 2 + c * x + d

plt.figure('拟合',figsize=(8,6))
'''
拟合点
'''
x = [ 1 , 2 , 3 , 4 , 5]
y = [1 , 3 , 8 , 18 , 36]

plt.rcParams['font.sans-serif']='SimHei'
plt.subplot(221)
plt.scatter(x,y,2,'r') # 这个2是点的大小

# 直线拟合
a,b = optimize.curve_fit(f1,x,y)[0]
print('a,b---->',a,b)
x1 = np.arange(0,6,0.1)
y1 = a * x1 + b
plt.plot(x1,y1,'b')

# 二次曲线拟合
plt.subplot(222)
plt.scatter(x,y,2,'r') # 这个2是点的大小

a,b,c = optimize.curve_fit(f2,x,y)[0]
x2 = np.arange(0,6,0.1)
y2 = a * x2 ** 2 + b * x2 + c
plt.plot(x2,y2,'g')
plt.annotate('这是二次曲线拟合',xy=(.5,3),xytext=(1,20),
             arrowprops=dict(facecolor='r',shrink=.1))

# 三次曲线拟合
plt.subplot(223)
plt.scatter(x,y,2,'r') # 这个2是点的大小

a,b,c,d = optimize.curve_fit(f3,x,y)[0]
x3 = np.arange(0,6,0.1)
y3 = a * x3 ** 3 + b * x3 ** 2 + c * x3 + d
plt.plot(x3,y3,'purple')
plt.title("title")
plt.xlabel('x轴')
plt.ylabel('y轴')

# 指数拟合
def f4(x,a,b):
    return x ** a + b
xdata = np.linspace(0,4,50)
y = f4(xdata,2.5,1.3)
ydata = y + 4 * np.random.normal(size=50)
plt.subplot(224)
plt.plot(xdata,ydata,'r')
plt.annotate('红色是原始数据',xy=(0,0),xytext=(0,11),
             arrowprops=dict(facecolor='r',shrink=.1))
a,b = optimize.curve_fit(f4,xdata,ydata)
y4 = [f4(i,a[0],a[1]) for i in xdata]
plt.plot(xdata,y4,'b--')
# pl.plot(xdata,ydata,label=u'真实数据')


plt.show()



