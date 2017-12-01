#--coding:utf-8--
import numpy
import matplotlib.pyplot as plot

mu,sigma = 100,15
x = mu + sigma * numpy.random.randn(10000)

#数据直方图
n, bins, patches = plot.hist(x, 50, normed = 1,facecolor='g',alpha=0.75)
plot.xlabel('smart')
plot.ylabel('probability')
plot.title('histogram of IQ')
plot.text(60, .025,r'$mu=100,sigma=15$')
plot.axis([40,160,0,0.03]) #前两位横轴坐标，后两位纵轴坐标
plot.grid(True)
plot.show()

