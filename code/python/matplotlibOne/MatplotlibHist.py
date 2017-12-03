#--coding:utf-8--
import numpy
import matplotlib.pyplot as plot
import matplotlib.mlab as mlab

mu,sigma = 100,15
x = mu + sigma * numpy.random.randn(15000)
print(numpy.random.normal(0,1,10))
#数据直方图
'''
直方图是用面积表示各组频数的多少，矩形的高度表示每一组的频数或频率，
宽度则表示各组的组距，因此其高度与宽度均有意义。
'''
n, bins, patches = plot.hist(x, bins=50, normed = 0,histtype='bar',facecolor='g',alpha=0.5)
x = []
num = 0
pre = 0
for i in bins:
    num = num + 1
    if num > 1:
        x.append((pre+i)/2)
    pre = i

y = mlab.normpdf(bins,mu,sigma)
plot.plot(x,n,'r--')
plot.xlabel('smart')
plot.ylabel('probability')
plot.title('histogram of IQ')
plot.text(60, .1,r'$\mu=100$, $\sigma_i=15$')
plot.axis([40,160,0,1000]) #前两位横轴坐标，后两位纵轴坐标
plot.grid(True)
plot.show()

