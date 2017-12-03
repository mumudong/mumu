#--coding:utf-8--
import numpy
import matplotlib.pyplot as plot
import matplotlib.mlab as mlab
from scipy import optimize
from scipy import interpolate

mu,sigma = 100,15
x = mu + sigma * numpy.random.randn(15000)
print(numpy.random.normal(0,1,10))
#数据直方图
'''
直方图是用面积表示各组频数的多少，矩形的高度表示每一组的频数或频率，
宽度则表示各组的组距，因此其高度与宽度均有意义。
'''
# bins是表示组距之间的点，n是组距对应的y值
n, bins, patches = plot.hist(x, bins=50, normed = 0,histtype='bar',facecolor='g',alpha=0.5)
x = []
num = 0
pre = 0
for i in bins:
    num = num + 1
    if num > 1:
        x.append(int((pre+i)/2))
    pre = i
print(x)
# y = mlab.normpdf(bins,mu,sigma)
def f1(x,a,b,c):
    return a * x ** 2 + b * x + c

a,b,c = optimize.curve_fit(f1,x,n)[0]
x1 = numpy.arange(1,160)
y1 = a * x1 ** 2 + b * x1 + c
plot.plot(x1,y1,'r--')
print('lenth:',len(x),'---',len(n))
func = interpolate.interp1d(x, n, kind='cubic')
x_new = numpy.arange(x[0],x[len(x)-1],4)

y_new = func(x_new)
plot.plot(x_new,y_new)

plot.xlabel('smart')
plot.ylabel('probability')
plot.title('histogram of IQ')
plot.text(60, .1,r'$\mu=100$, $\sigma_i=15$')
plot.axis([40,160,0,1000]) #前两位横轴坐标，后两位纵轴坐标
plot.grid(True)
plot.show()

