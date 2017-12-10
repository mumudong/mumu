#--coding:utf-8--
from scipy import stats as st
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt
x = st.norm(loc=1.0,scale=2.0).rvs(10)
# 可以使用fit()方法对随机取样序列x进行拟合，返回的是与随机取样值最吻合的随机变量的参数
y = st.norm.fit(x) # 得到随机序列的期望值和标准差

x,y = np.mgrid[-1:1:.5,-1:1:.5]
pos = np.dstack((x,y))
print(x)
print(y)
print(pos)
rv = st.multivariate_normal([0.5,-0.2],[[2.0, 0.3], [0.3, 0.5]])
print(rv.pdf(pos)) # 接受的参数是三维数据，第三维代表一个数据坐标，1、2维代表网格坐标位置。
C = plt.contour(x, y, rv.pdf(pos), 8, colors = 'b', linewidth = 0.5)
# 绘制等高线数据
plt.clabel(C, inline = True, fontsize = 10)

# 去除坐标轴
# plt.xticks(())
# plt.yticks(())
plt.show()
