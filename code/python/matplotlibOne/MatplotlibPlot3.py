#--coding:utf-8--
import numpy
import matplotlib.pyplot as plot
from random import *

x = numpy.arange(1,20,0.2)

y = (x - 10) ** 2

#figsize设置画布大小
plot.figure(figsize = (8,8),dpi = 80)
# 将figure设置的画布大小分成几个部分，参数‘221’表示2(row)x2(colu),即将画布分成2x2，
# 两行两列的4块区域，1表示选择图形输出的区域在第一块，图形输出区域参数必须在“行x列”范围
plot.subplot(221)
plot.plot(x,-y)
plot.subplot(222)
plot.plot(x,-y)
plot.subplot(223)
# plot.plot(x,y*2)
plot.subplot(212)
plot.plot(x,y-2*x)
plot.plot(x,y)
plot.show()
